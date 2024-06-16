# Copyright (c) 2016 Universidade Federal Fluminense (UFF)
# Copyright (c) 2016 Polytechnic Institute of New York University.
# This file is part of noWorkflow.
# Please, consult the license terms in the LICENSE file.
"""Lightweight Module"""
from __future__ import (absolute_import, print_function,
                        division, unicode_literals)

from ..models import Module
from .base import BaseLW, define_attrs


class ModuleLW(BaseLW):
    """Module lightweight object"""

    __slots__, attributes = define_attrs(
        ["trial_id", "id", "name", "path", "version", "code_block_id", 
         "transformed", "fullpath"],
    )
    nullable = set()
    model = Module

    def __init__(
        self, id_, trial_id, name, version, path, code_block_id,
        transformed, fullpath
    ):                                                                           # pylint: disable=too-many-arguments
        self.trial_id = trial_id
        self.id = id_                                                            # pylint: disable=invalid-name
        self.name = name
        self.version = version
        self.path = path
        self.code_block_id = code_block_id
        self.transformed = transformed
        self.fullpath = fullpath

    def is_complete(self):                                                       # pylint: disable=no-self-use
        """Module can always be removed from object store"""
        return True

    def __repr__(self):
        return ("Module(id={}, name={}, version={})").format(
            self.id, self.name, self.version)

    def __json__(self):
        return {
            'trial_id': self.trial_id,
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'path': self.path,
            'code_block_id': self.code_block_id,
            'transformed': self.transformed,
            'fullpath': self.fullpath
        }