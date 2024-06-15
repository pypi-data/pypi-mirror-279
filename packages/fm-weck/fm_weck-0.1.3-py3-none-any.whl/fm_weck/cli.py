# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any, Optional, Tuple, Union

from fm_tools.benchexec_helper import DataModel

from fm_weck import Config
from fm_weck.resources import iter_fm_data, iter_properties

from . import __version__
from .engine import Engine
from .serve import run_guided, run_manual


@dataclass
class ToolQualifier:
    tool: Union[str, Path]
    version: Optional[str]

    def __init__(self, qualifier: str):
        """
        The string is of the form <tool>[:<version>]. Tool might be a path.
        """

        self.tool = qualifier.split(":")[0]

        self.version = None
        try:
            self.version = qualifier.split(":")[1]
        except IndexError:
            # No version given
            return


def add_shared_arguments(
        parser: argparse.ArgumentParser, require_manual=False
) -> Tuple[argparse.ArgumentParser, argparse.ArgumentParser]:
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--config",
        action="store",
        type=Path,
        help="Path to the configuration file.",
        default=None,
    )

    parser.add_argument(
        "--loglevel",
        choices=["debug", "info", "warning", "error", "critical"],
        action="store",
        default=None,
        help="Set the log level.",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all fm-tools that can be called by name.",
        required=False,
        default=False,
    )

    subparsers = parser.add_subparsers()
    run = subparsers.add_parser("run", help="Run a verifier inside a container.")

    run.add_argument(
        "-m",
        "--manual",
        action="store_true",
        required=require_manual,
        help="Enable manual mode. All args past <tool>:<version> are passed verbatim to the tool.",
    )

    run.add_argument(
        "--skip-download",
        action="store_true",
        help="Do not download the fm-tool, even if it is not available in the cache.",
    )

    run.add_argument(
        "TOOL",
        help="The tool to use. Can be the form <tool>:<version>. "
             "The TOOL is either the name of a bundled tool (c.f. fm-weck --list) or "
             "the path to a fm-tools yaml file.",
        type=ToolQualifier,
    )

    return parser, run


class MayFailParserError(Exception):
    pass


class MayFailParser(argparse.ArgumentParser):
    def error(self, message):
        raise MayFailParserError

    def format_help(self):
        raise MayFailParserError


def parse(raw_args: list[str]) -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    manual_parser = MayFailParser(description="fm-weck", exit_on_error=False)
    normal_parser = argparse.ArgumentParser(description="fm-weck")

    manual_parser, run = add_shared_arguments(manual_parser, require_manual=True)
    # manual mode
    run.add_argument("argument_list", metavar="args", nargs="*", help="Arguments for the fm-tool")

    normal_parser, run = add_shared_arguments(normal_parser)

    # guided mode
    run.add_argument(
        "-p",
        "--property",
        "--spec",
        action="store",
        help=(
            "Property to that is forwarded to the fm-tool."
            " Either a path to a property file or a property name from SV-COMP or Test-Comp."
            " Use fm-weck serve --list to see all properties that can be called by name."
        ),
        required=False,
        default=None,
    )

    run.add_argument(
        "-d",
        "--data-model",
        action="store",
        choices=list(DataModel),
        help="The data model that shall be used.",
        required=False,
        type=lambda dm: DataModel[dm],
        default=DataModel.LP64,
    )

    run.add_argument(
        "-w",
        "--witness",
        action="store",
        help="A witness that shall be passed to the tool.",
        required=False,
        default=None,
    )

    run.add_argument("files", metavar="FILES", nargs="+", help="Files to pass to the tool")
    run.add_argument(
        "argument_list",
        metavar="args",
        nargs="*",
        help="Additional arguments for the fm-tool." " To add them, separate them with '--' from the files.",
    )

    try:
        first_pass, remain = manual_parser.parse_known_args(raw_args)
        if remain:
            i = raw_args.index(remain[0])
            args = raw_args.copy()
            args.insert(i, "--")
            # retry parsing
            return manual_parser, manual_parser.parse_args(args)
        else:
            return manual_parser, first_pass
    except MayFailParserError:
        return normal_parser, normal_parser.parse_args(raw_args)


@cache
def fm_tools_choice_map():
    ignore = {
        "schema.yml",
    }

    actors = {actor_def.stem: actor_def for actor_def in iter_fm_data() if (actor_def.name not in ignore)}

    return actors


@cache
def property_choice_map():
    return {spec_path.stem: spec_path for spec_path in iter_properties() if spec_path.suffix != ".license"}


def list_known_tools():
    return fm_tools_choice_map().keys()


def list_known_properties():
    return property_choice_map().keys()


def resolve_tool(tool: ToolQualifier) -> Path:
    tool_name = tool.tool
    if (as_path := Path(tool_name)).exists() and as_path.is_file():
        return as_path

    return fm_tools_choice_map()[tool_name]


def resolve_property(prop_name: str) -> Path:
    if (as_path := Path(prop_name)).exists() and as_path.is_file():
        return as_path

    return property_choice_map()[prop_name]


def set_log_level(loglevel: Optional[str], config: dict[str, Any]):
    level = "WARNING"
    level = loglevel.upper() if loglevel else config.get("logging", {}).get("level", level)
    logging.basicConfig(level=level)


def main_serve(args: argparse.Namespace):
    if not args.TOOL:
        logging.error("No fm-tool given. Aborting...")
        return 1
    try:
        fm_data = resolve_tool(args.TOOL)
    except KeyError:
        logging.error("Unknown tool %s", args.TOOL)
        return 1

    try:
        property_path = resolve_property(args.property) if args.property else None
    except KeyError:
        logging.error("Unknown property %s", args.property)
        return 1

    run_guided(
        fm_tool=fm_data,
        version=args.TOOL.version,
        configuration=Config(),
        prop=property_path,
        program_files=args.files,
        additional_args=args.argument_list,
        data_model=args.data_model,
        skip_download=args.skip_download,
    )


def main_run(args: argparse.Namespace):
    if not args.fm_data:
        engine = Engine.from_config(Config())
    else:
        try:
            fm_data = resolve_tool(args.fm_data)
        except KeyError:
            logging.error("Unknown tool %s", fm_data)
            return 1
        engine = Engine.from_config(fm_data, args.version, Config())
    engine.run(args.command, *args.args)


def main_manual(args: argparse.Namespace):
    if not args.TOOL:
        logging.error("No fm-tool given. Aborting...")
        return 1
    try:
        fm_data = resolve_tool(args.TOOL)
    except KeyError:
        logging.error("Unknown tool %s", args.TOOL)
        return 1

    run_manual(
        fm_tool=fm_data,
        version=args.TOOL.version,
        configuration=Config(),
        command=args.argument_list,
        skip_download=args.skip_download,
    )


def main_shell(args: argparse.Namespace):
    if not args.fm_data:
        engine = Engine.from_config(Config())
    else:
        try:
            fm_data = resolve_tool(args.fm_data)
        except KeyError:
            logging.error("Unknown tool %s", fm_data)
            return 1
        engine = Engine.from_config(fm_data, args.version, Config())
    engine.interactive = True
    engine.run("/bin/bash")


def cli(raw_args: list[str]):
    parser, args = parse(raw_args)
    configuration = Config().load(args.config)
    set_log_level(args.loglevel, configuration)

    if args.list:
        print("List of fm-tools callable by name:")
        for tool in sorted(list_known_tools()):
            print(f"  - {tool}")
        print("\nList of properties callable by name:")
        for prop in sorted(list_known_properties()):
            print(f"  - {prop}")
        return

    if not hasattr(args, "TOOL"):
        return parser.print_help()

    if args.manual:
        return main_manual(args)

    main_serve(args)
