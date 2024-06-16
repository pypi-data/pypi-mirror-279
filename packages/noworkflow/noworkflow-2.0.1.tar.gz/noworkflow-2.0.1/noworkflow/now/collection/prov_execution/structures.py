# Copyright (c) 2016 Universidade Federal Fluminense (UFF)
# Copyright (c) 2016 Polytechnic Institute of New York University.
# This file is part of noWorkflow.
# Please, consult the license terms in the LICENSE file.
"""Data Structures"""
from __future__ import (absolute_import, print_function,
                        division, unicode_literals)

from copy import copy
from collections import namedtuple, defaultdict


FakeEvaluation = namedtuple(
    "FakeEvaluation", "activation_id id")
FAKE = FakeEvaluation(None, None)


AssignAccess = namedtuple(
    "AssignAccess", "value dependency addr value_dep checkpoint")


class FutureActivation(object):

    def __init__(self, name, code_id, activation, func, dependency_type):
        self.name = name
        self.code_id = code_id
        self.activation = activation
        self.func = func
        self.dependency_type = dependency_type
        self.dependencies = []
        self.bound_dependency = None
        self.func_evaluation = None


class Assign(namedtuple("Assign", "checkpoint value dependency")):
    """Represent an assignment for further processing"""

    def __new__(cls, *args, **kwargs):
        self = super(Assign, cls).__new__(cls, *args, **kwargs)
        self.accesses = {}
        self.generators = defaultdict(list)
        self.index = -1
        return self

    def sub(self, value, dependency):
        """Create a new Assign with the same access for propagation in
        multiple assignments"""
        assign = Assign(self.checkpoint, value, dependency)
        assign.index = self.index
        assign.accesses = self.accesses
        return assign

    def combine(self, other):
        """Combine assignents"""
        for code_id, access in other.accesses.items():
            self.accesses[code_id] = access

        for obj_id, generator in other.generators.items():
            self.generators[obj_id] = generator


class ConditionExceptions(object):
    """Exception factory for handling ifs transformed into tries"""
    # pylint: disable=too-few-public-methods
    def __init__(self):
        self.exceptions = {}

    def __getitem__(self, item):
        if item not in self.exceptions:
            class ConditionException(Exception):
                """If body Exception"""
                pass
            self.exceptions[item] = ConditionException
        return self.exceptions[item]


class DependencyAware(object):
    """Store dependencies of an element"""

    def __init__(self, active=True, exc_handler=-1, code_id=None, maybe_activation=None):
        self.dependencies = []
        self.extra_dependencies = []
        self.exc_handler = exc_handler
        self.code_id = code_id
        self.maybe_activation = maybe_activation or set()

        self.active = active

    def replace(self, other):
        """Replace by other dependency aware"""
        self.dependencies = other.dependencies
        self.extra_dependencies = other.extra_dependencies
        self.exc_handler = other.exc_handler
        self.code_id = other.code_id
        self.maybe_activation = other.maybe_activation

    def add(self, dependency):
        """Add dependency"""
        if self.active:
            self.dependencies.append(dependency)

    def add_extra(self, dependency):
        """Add extra dependency"""
        if self.active:
            self.extra_dependencies.append(dependency)

    def __bool__(self):
        return bool(self.dependencies) or bool(self.extra_dependencies)

    def clone(self, extra_only=False, **kwargs):
        """Clone dependency aware and replace mode"""
        new_depa = DependencyAware()
        if not extra_only:
            for dep in self.dependencies:
                new_dep = copy(dep)
                for key, value in kwargs.items():
                    setattr(new_dep, key, value)
                #new_dep.mode = mode or new_dep.mode
                new_depa.add(new_dep)
        for dep in self.extra_dependencies:
            new_dep = copy(dep)
            for key, value in kwargs.items():
                setattr(new_dep, key, value)
            new_depa.add_extra(new_dep)
        new_depa.exc_handler = self.exc_handler
        new_depa.code_id = self.code_id
        return new_depa

    @classmethod
    def join(cls, depa_list):
        """Join list of DependencyAwares"""
        new_depa = cls(exc_handler=float('inf'))
        for e_depa in depa_list:
            new_depa.code_id = e_depa.code_id
            new_depa.exc_handler = min(
                new_depa.exc_handler,
                e_depa.exc_handler
            )

            for dep in e_depa.dependencies:
                new_depa.add(dep)
            for dep in e_depa.extra_dependencies:
                new_depa.add_extra(dep)
        return new_depa

    def swap(self):
        """Swap dependencies and extra_dependencies"""
        self.dependencies, self.extra_dependencies = (
            self.extra_dependencies, self.dependencies
        )

    def __repr__(self):
        return "{} - {}".format(self.dependencies, self.extra_dependencies)

class Generator(object):
    """Represent a generator"""
    def __init__(self):
        self.value = None
        self.evaluation = None
        self.dependency = None

class Dependency(object):
    """Represent a dependency"""

    def __init__(self, evaluation, value, mode, collection=FAKE, addr=None):
        self.activation_id = evaluation.activation_id
        self.evaluation_id = evaluation.id
        self.code_id = evaluation.code_component_id

        self.collection = collection
        self.addr = addr
        self.evaluation = evaluation
        self.value = value
        self.mode = mode

        self.reference = False
        # Kind: extra information about dependency
        self.kind = None
        self.arg = None
        self.sub_dependencies = []

    def __repr__(self):
        # pylint: disable=undefined-variable
        evaluation = __noworkflow__.evaluations[self.evaluation_id]
        code_component = __noworkflow__.code_components[
            evaluation.code_component_id]
        return "{}({})".format(code_component.name, self.mode)


class Parameter(object):

    def __init__(self, name, code_id, value, is_vararg=False):
        self.name = name
        self.code_id = code_id
        self.is_vararg = is_vararg
        self.filled = False
        self.default = None
        self.value = value

    def __repr__(self):
        return "{}".format(self.name)


class MemberDependencyAware(DependencyAware):
    """Store dependencies of a member element"""

    def __init__(self, active=True, exc_handler=-1, code_id=None):
        super(MemberDependencyAware, self).__init__(
            active=active,
            exc_handler=exc_handler,
            code_id=code_id,
        )
        self.key = None
        self.value = None


class CollectionDependencyAware(DependencyAware):
    """Store dependencies of a collection element"""

    def __init__(self, active=True, exc_handler=-1, code_id=None):
        super(CollectionDependencyAware, self).__init__(
            active=active,
            exc_handler=exc_handler,
            code_id=code_id,
        )
        # list of tuples representing (item name, evaluation_id, time)
        self.items = []


class WithContext(object):

    def __init__(self, now, context, activation, exc_handler):
        self.noworkflow = now
        self.context = context
        self.activation = activation
        self.exc_handler = exc_handler

    def __enter__(self):
        return self.context.__enter__()

    def __exit__(self, *exc):
        result = self.context.__exit__(*exc)
        if result: # suppressed exception:
            self.noworkflow.collect_exception(self.activation, self.exc_handler)
        return result
