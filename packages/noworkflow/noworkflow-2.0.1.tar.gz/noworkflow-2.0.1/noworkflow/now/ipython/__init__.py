# Copyright (c) 2016 Universidade Federal Fluminense (UFF)
# Copyright (c) 2016 Polytechnic Institute of New York University.
# This file is part of noWorkflow.
# Please, consult the license terms in the LICENSE file.
"""IPython Module"""
from __future__ import (absolute_import, print_function,
                        division)

from .defaults import set_default
from ..persistence.models import *                                               # pylint: disable=wildcard-import
from ..persistence import persistence_config, relational, content
from ..models.history import History
from ..models.diff import Diff
from ... import patterns


def init(path=None, ipython=None):
    """Initiate noWorkflow extension.
    Load D3, IPython magics, and connect to database


    Keyword Arguments:
    path -- database path (default=current directory)
    ipython -- IPython object (default=None)
    """

    import os
    from .magics import register_magics
    from .dotmagic import load_ipython_extension as load_dot
    load_dot(ipython)
    register_magics(ipython)

    if path is None:
        path = os.getcwd()
    persistence_config.connect(path)

    return u"ok"
