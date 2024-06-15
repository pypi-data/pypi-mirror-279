# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import subprocess
import sys
import uuid
from abc import ABC, abstractmethod
from functools import singledispatchmethod
from pathlib import Path
from threading import Thread
from typing import IO, Union

from fm_tools.fmdata import FmData, FmImageConfig

from fm_weck.config import Config, parse_fm_data
from fm_weck.image_mgr import ImageMgr


class Engine(ABC):
    interactive: bool = False

    @abstractmethod
    def assemble_command(self, command: tuple[str, ...]) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def mount(src: str, target: str):
        raise NotImplementedError

    @staticmethod
    def extract_image(fm: Union[str, Path], version: str, config: dict) -> str:
        image = config.get("defaults", {}).get("image", None)

        return parse_fm_data(fm, version).get_images().with_fallback(image)

    @singledispatchmethod
    @staticmethod
    def from_config(config: Config) -> "Engine":
        engine = Podman(config.from_defaults_or_none("image"))
        return Engine._prepare_engine(engine, config)

    @from_config.register
    @staticmethod
    def _(fm: Path, version: str, config: Config):
        image = Engine.extract_image(fm, version, config)
        engine = Podman(image)
        return Engine._prepare_engine(engine, config)

    @from_config.register
    @staticmethod
    def _(fm: str, version: str, config: Config):
        image = Engine.extract_image(fm, version, config)
        engine = Podman(image)
        return Engine._prepare_engine(engine, config)

    @from_config.register
    @staticmethod
    def _(fm: FmData, config: Config):
        image = fm.get_images().with_fallback(config.from_defaults_or_none("image"))
        engine = Podman(image)
        return Engine._prepare_engine(engine, config)

    @staticmethod
    def _prepare_engine(engine, config: dict) -> "Engine":
        for src, target in config.get("mount", {}).items():
            if not Path(src).exists():
                logging.warn("Mount source %s does not exist. Ignoring it...", src)
                continue
            engine.mount(src, target)

        return engine

    @abstractmethod
    def image_from(self, containerfile: Path) -> "BuildCommand": ...

    class BuildCommand(ABC):
        @abstractmethod
        def base_image(self, image: str): ...

        @abstractmethod
        def packages(self, packages: list[str]): ...

        @abstractmethod
        def build(self): ...

    def _read_output(self, stream: IO[bytes], to: IO[bytes] = sys.stdout.buffer):
        for c in iter(lambda: stream.read(1), b""):
            to.write(c)

    def _run_process_with_live_output(self, command: tuple[str]):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout_reader = Thread(target=self._read_output, args=(process.stdout,))
        stderr_reader = Thread(target=self._read_output, args=(process.stderr, sys.stderr.buffer))
        stdout_reader.start()
        stderr_reader.start()
        stdout_reader.join()
        stderr_reader.join()
        process.wait()

    def _run_process_blocking(self, command: str):
        try:
            res = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            os.write(1, res.stdout)
            os.write(2, res.stderr)
        except subprocess.CalledProcessError as e:
            print(e.stderr.decode("utf-8"))

    def run(self, *command: str) -> None:
        command = self.assemble_command(command)
        logging.info("Running: %s", command)
        self._run_process_with_live_output(command)

    def get_workdir(self):
        return Path.cwd().absolute()


class Podman(Engine):
    def __init__(self, image: Union[str, FmImageConfig]):
        self._engine = "podman"
        self.image = self._initialize_image(image)
        self.extra_args = {}

    @singledispatchmethod
    def _initialize_image(self, image: str) -> str:
        return image

    @_initialize_image.register
    def _from_fm_config(self, fm_config: FmImageConfig) -> str:
        return ImageMgr().prepare_image(self, fm_config)

    def mount_benchexec(self, benchexec_dir: str):
        self.extra_args["benchexec"] = [
            "-v",
            f"{benchexec_dir.absolute()}:/benchexec",
        ]

    def mount(self, source: str, target: str):
        self.extra_args["mounts"] = self.extra_args.get("mounts", []) + [
            "-v",
            f"{source}:{target}",
        ]

    class PodmanBuildCommand(Engine.BuildCommand):
        def __init__(self, containerfile: Path):
            self.containerfile = containerfile
            self.build_args = {}

        def base_image(self, image: str):
            self.build_args["--build-arg"] = f"BASE_IMAGE={image}"
            return self

        def packages(self, packages: list[str]):
            self.build_args["--build-arg"] = f"REQUIRED_PACKAGES=\"{' '.join(packages)}\""
            return self

        def build(self):
            tag_id = uuid.uuid4().hex
            tag = f"fmweck/{tag_id}"

            ret = subprocess.run(
                [
                    "podman",
                    "build",
                    "-t",
                    tag,
                    "-f",
                    self.containerfile,
                    *self.build_args,
                    ".",
                ],
                check=True,
            )

            logging.debug("Build output: %s", ret.stdout)
            logging.info("Built image %s", tag)

            return tag

    def image_from(self, containerfile: Path):
        return self.PodmanBuildCommand(containerfile)

    def get_workdir(self):
        return Path("/home/cwd")

    def assemble_command(self, command: tuple[str, ...]) -> list[str]:
        base = [
            "podman",
            "run",
            "--annotation",
            "run.oci.keep_original_groups=1",
            "--security-opt",
            "unmask=/proc/*",
            "--security-opt",
            "seccomp=unconfined",
            "-v",
            "/sys/fs/cgroup:/sys/fs/cgroup",
            "-v",
            f"{Path.cwd().absolute()}:/home/cwd",
            "--workdir",
            str(self.get_workdir()),
            "--rm",
        ]

        if self.interactive:
            base += ["-it"]

        for value in self.extra_args.values():
            if isinstance(value, list) and not isinstance(value, str):
                base += value
            else:
                base.append(value)
        _command = self._prep_command(command)
        return base + [self.image, *_command]

    def _prep_command(self, command: tuple[str, ...]) -> tuple[str]:
        """We want to map absolute paths of the current working directory to the
        working directory of the container."""

        abs_cwd = str(Path.cwd().absolute())

        def _map_path(p: Union[str, Path]) -> str:
            if isinstance(p, Path):
                if p.is_relative_to(Path.cwd()):
                    relative = p.relative_to(Path.cwd())
                    return self.get_workdir() / relative
                else:
                    return p
            return p.replace(abs_cwd, str(self.get_workdir()))

        return tuple(map(_map_path, command))
