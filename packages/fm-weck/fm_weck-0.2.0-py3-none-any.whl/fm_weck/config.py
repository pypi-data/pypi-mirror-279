# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0
import shutil
from functools import cache
from pathlib import Path
from typing import Any, Optional

import yaml
from fm_tools.fmdata import FmData

from fm_weck.resources import RUN_WITH_OVERLAY

try:
    import tomllib as toml
except ImportError:
    import tomli as toml

_SEARCH_ORDER: tuple[Path, ...] = (
    Path.cwd() / ".weck",
    Path.home() / ".weck",
    Path.home() / ".config" / "weck",
    Path.home() / ".config" / "weck" / "config.toml",
)
BASE_CONFIG = """
[logging]
level = "INFO"

[defaults]
image = "ubuntu:latest"
cache_location = ".weck_cache"
"""


class Config(object):
    """
    The config singleton holds the configuration for the weck tool.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._config = None
        return cls._instance

    def load(self, config: Optional[Path] = None) -> dict[str, Any]:
        if self._config:
            return self._config

        if config:
            if not config.exists() or not config.is_file():
                raise FileNotFoundError(f"config file {config} does not exist")

            with config.open("rb") as f:
                self._config = toml.load(f)
                return self._config

        for path in _SEARCH_ORDER:
            if not path.exists():
                continue

            # Configuration is in TOML format
            with path.open("rb") as f:
                self._config = toml.load(f)
                return self._config

        return toml.loads(BASE_CONFIG)

    def __getitem__(self, key: str) -> Any:
        return self._config[key]

    def get(self, key: str, default: Any = None) -> Any:
        if self._config is not None:
            return self._config.get(key, default)

        return default

    def defaults(self) -> dict[str, Any]:
        return self.get("defaults", {})

    def from_defaults_or_none(self, key: str) -> Any:
        return self.defaults().get(key, None)

    @property
    def cache_location(self) -> Path:
        return Path(self.defaults().get("cache_location", Path.cwd() / ".weck_cache"))

    def get_shelve_space_for(self, fm_data: FmData) -> Path:
        shelve = self.cache_location
        tool_name = fm_data.get_actor_name()  # safe to use in filesystem
        return shelve / tool_name

    def get_shelve_path_for_property(self, path: Path) -> Path:
        shelve = self.cache_location / ".properties"
        shelve.mkdir(parents=True, exist_ok=True)
        property_name = path.name
        return shelve / property_name

    def make_script_available(self) -> Path:
        script_dir = self.cache_location / ".scripts"
        run_script = script_dir / "run_with_overlay.sh"
        if run_script.exists() and run_script.is_file():
            return run_script

        script_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(RUN_WITH_OVERLAY, run_script)
        return run_script


@cache
def parse_fm_data(fm_data: Path, version: Optional[str]) -> FmData:
    if not fm_data.exists() or not fm_data.is_file():
        raise FileNotFoundError(f"fm data file {fm_data} does not exist")

    with fm_data.open("rb") as f:
        data = yaml.safe_load(f)

    return FmData(data, version)
