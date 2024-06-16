# Copyright (c) 2016 Universidade Federal Fluminense (UFF)
# Copyright (c) 2016 Polytechnic Institute of New York University.
# This file is part of noWorkflow.
# Please, consult the license terms in the LICENSE file.
"""Commands and argument parsers for 'now'"""
from __future__ import (absolute_import, print_function,
                        division)

import argparse
import sys
import sqlalchemy

from .command import Command, SmartFormatter
from .cmd_run import Run
from .cmd_debug import Debug
from .cmd_import import Import
from .cmd_push import Push
from .cmd_pull import Pull
from .cmd_list import List
from .cmd_show import Show
from .cmd_diff import Diff
from .cmd_dataflow import Dataflow
from .cmd_export import Export
from .cmd_restore import Restore
from .cmd_vis import Vis
from .cmd_demo import Demo
from .cmd_helper import Helper
from .cmd_history import History
from .cmd_prov import Prov
from .cmd_schema import Schema
from .cmd_kernel import Kernel
from .cmd_gc import GC
from .cmd_evaluation import Evaluation
from .cmd_clean import Clean
from ..utils.io import print_msg


def main():
    """Main function"""
    from ..utils.functions import version
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=SmartFormatter, usage="")
    parser.add_argument("-v", "--version", action="version",
                        version="noWorkflow {}".format(version()))
    subparsers = parser.add_subparsers(metavar="")
    commands = [
        Run(),
        Debug(),
        List(),
        Show(),
        Diff(),
        Dataflow(),
        Export(),
        Import(),
        Push(),
        Pull(),
        Restore(),
        Vis(),
        Demo(),
        Helper(),
        History(),
        Prov(),
        Schema(),
        Kernel(),
        GC(),
        Evaluation(),
        Clean()

    ]
    for cmd in commands:
        cmd.create_parser(subparsers)

    if len(sys.argv) == 1:
        sys.argv.append("-h")

    try:
        args, _ = parser.parse_known_args()
        args.func(args)
    except RuntimeError as exc:
        print_msg(exc, True)
    except sqlalchemy.exc.OperationalError as exc:
        print_msg("invalid noWorkflow database", True)
        print_msg("it is probably outdated", True)


__all__ = [
    "Command",
    "Run",
    "Debug",
    "List",
    "Show",
    "Diff",
    "Dataflow",
    "Export",
    "Restore",
    "Vis",
    "Demo",
    "Helper",
    "History",
    "Prov",
    "Kernel",
    "GC",
    "main",
    "Push",
    "Pull",
    "Import",
]
