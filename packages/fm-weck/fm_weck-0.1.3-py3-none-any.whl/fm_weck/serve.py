# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
import shutil
from pathlib import Path
from typing import Optional, Tuple

from fm_tools import FmData
from fm_tools.benchexec_helper import DataModel

from fm_weck.config import Config, parse_fm_data

from .engine import Engine


def setup_fm_tool(
    fm_tool: Path, version: Optional[str], configuration: Config, skip_download: bool = False
) -> Tuple[FmData, Path]:
    fm_data = parse_fm_data(fm_tool, version)

    shelve_space = configuration.get_shelve_space_for(fm_data)
    logging.debug("Using shelve space %s", shelve_space)

    if not skip_download:
        fm_data.download_and_install_into(shelve_space)
    fm_data.get_toolinfo_module().make_available()

    return fm_data, shelve_space


def run_guided(
    fm_tool: Path,
    version: Optional[str],
    configuration: Config,
    prop: Optional[Path],
    program_files: list[Path],
    additional_args: list[str],
    data_model: Optional[DataModel] = None,
    skip_download: bool = False,
):
    property_path = None
    if prop is not None:
        try:
            # the source path might not be mounted in the contianer, so we
            # copy the property to the weck_cache which should be mounted
            source_property_path = prop
            property_path = configuration.get_shelve_path_for_property(source_property_path)
            shutil.copyfile(source_property_path, property_path)
        except KeyError:
            logging.error("Unknown property %s", prop)
            return 1

    fm_data, shelve_space = setup_fm_tool(fm_tool, version, configuration, skip_download)
    engine = Engine.from_config(fm_data, configuration)

    command = fm_data.command_line(
        shelve_space,
        input_files=program_files,
        working_dir=engine.get_workdir(),
        property=property_path,
        data_model=data_model,
        options=additional_args,
        add_options_from_fm_data=True,
    )

    logging.debug("Assembled command from fm-tools:", command)

    engine.run(*command)


def run_manual(
    fm_tool: Path, version: Optional[str], configuration: Config, command: list[str], skip_download: bool = False
):
    fm_data, shelve_space = setup_fm_tool(fm_tool, version, configuration, skip_download)
    engine = Engine.from_config(fm_data, configuration)

    executable = fm_data.get_executable_path(shelve_space)
    logging.debug("Using executable %s", executable)
    logging.debug("Assembled command %s", [executable, *command])
    engine.run(executable, *command)
