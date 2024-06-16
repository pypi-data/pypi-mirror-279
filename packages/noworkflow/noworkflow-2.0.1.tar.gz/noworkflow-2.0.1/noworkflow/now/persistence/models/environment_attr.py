# Copyright (c) 2016 Universidade Federal Fluminense (UFF)
# Copyright (c) 2016 Polytechnic Institute of New York University.
# This file is part of noWorkflow.
# Please, consult the license terms in the LICENSE file.
"""Environment Attribute Model"""
from __future__ import (absolute_import, print_function,
                        division, unicode_literals)

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint

from ...utils.prolog import PrologDescription, PrologTrial, PrologRepr

from .base import AlchemyProxy, proxy_class


@proxy_class
class EnvironmentAttr(AlchemyProxy):
    """Represent an environment attribute


    Doctest:
    >>> from noworkflow.tests.helpers.models import erase_db, new_trial
    >>> from noworkflow.tests.helpers.models import environment_attrs
    >>> erase_db()
    >>> trial_id = new_trial()
    >>> id_ = environment_attrs.add(trial_id, "attr_name", "attr_value")
    >>> environment_attrs.do_store()

    Load EnvironmentAttr object by (trial_id, id):
    >>> environment = EnvironmentAttr((trial_id, id_))
    >>> environment  # doctest: +ELLIPSIS
    environment(..., 'attr_name', 'attr_value').

    Load EnvironmentAttr trial:
    >>> trial = environment.trial
    >>> trial.id == trial_id
    True
    """

    __tablename__ = "environment_attr"
    __table_args__ = (
        PrimaryKeyConstraint("trial_id", "id"),
        ForeignKeyConstraint(["trial_id"], ["trial.id"], ondelete="CASCADE"),
    )
    trial_id = Column(String, index=True)
    id = Column(Integer, index=True)                                             # pylint: disable=invalid-name
    name = Column(Text)
    value = Column(Text)

    # Relationship attributes (see relationships.py):
    #   trial: 1 Trial

    prolog_description = PrologDescription("environment", (
        PrologTrial("trial_id", link="trial.id"),
        PrologRepr("name"),
        PrologRepr("value"),
    ), description=(
        "informs that in a given trial (*TrialId*),\n"
        "a environment attribute (*Name*)\n"
        "was defined with *Value*."
    ))

    def __hash__(self):
        return hash((self.name, self.value))

    def __eq__(self, other):
        return self.name == other.name

    @property
    def brief(self):
        """Brief description of environment attribute


        Doctest:
        >>> from noworkflow.tests.helpers.models import erase_db, new_trial
        >>> from noworkflow.tests.helpers.models import environment_attrs
        >>> erase_db()
        >>> trial_id = new_trial()
        >>> id_ = environment_attrs.add(trial_id, "attr_name", "attr_value")
        >>> environment_attrs.do_store()
        >>> env = EnvironmentAttr((trial_id, id_))

        Show name as brief description
        >>> env.brief == 'attr_name'
        True
        """
        return self.name

    def show(self, print_=lambda x, offset=0: print(x)):
        """Show object

        Keyword arguments:
        print_ -- custom print function (default=print)


        Doctest:
        >>> from textwrap import dedent
        >>> from noworkflow.tests.helpers.models import erase_db, new_trial
        >>> from noworkflow.tests.helpers.models import environment_attrs
        >>> erase_db()
        >>> trial_id = new_trial()
        >>> id_ = environment_attrs.add(trial_id, "attr_name", "attr_value")
        >>> environment_attrs.do_store()
        >>> env = EnvironmentAttr((trial_id, id_))


        Show environment attribute:
        >>> env.show(
        ...     print_=lambda x: print(dedent(x))) #doctest: +ELLIPSIS
        attr_name: attr_value
        """
        print_("{0.name}: {0.value}".format(self))
    
    @staticmethod
    def get_os_userstring(model, session):
        os_name = session.query(model).filter(model.name == "OS_NAME").first().value.strip()
        if os_name == "Windows": return "USERNAME"
        elif (os_name == "Linux") or (os_name == "Darwin"): return "USER"
        
        return None
        
    @classmethod
    def get_userName(cls,trialId,session=None):
        session = session or relational.session
        model=cls.m
        return (
            session.query(model)
            .filter((model.trial_id == trialId) & (model.name == cls.get_os_userstring(model, session))).first()
        ).value
    
    @classmethod
    def get_userDomain(cls,trialId,session=None):
        session = session or relational.session
        model=cls.m
        return (
            session.query(model)
            .filter((model.trial_id == trialId) & (model.name == "HOSTNAME")).first()
        ).value