# Copyright (c) 2016 Universidade Federal Fluminense (UFF)
# Copyright (c) 2016 Polytechnic Institute of New York University.
# This file is part of noWorkflow.
# Please, consult the license terms in the LICENSE file.
"""Tag Model"""
from __future__ import (absolute_import, print_function,
                        division, unicode_literals)

from datetime import datetime

import uuid
from future.utils import lmap
from future.builtins import map as cvmap
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy import ForeignKeyConstraint, select, bindparam

from ...utils.prolog import PrologDescription, PrologTrial
from ...utils.prolog import PrologRepr, PrologTimestamp

from .. import relational

from .base import AlchemyProxy, proxy_class


def uuid_gen():
    return str(uuid.uuid4())
@proxy_class
class User(AlchemyProxy):
    __tablename__ = "user"
    id = Column( 
        String, unique=True, primary_key=True
    )
    userLogin = Column(String, unique=True)
    

    
    @classmethod  # query
    def create(cls, id,login, session=None):
        
        # pylint: disable=too-many-arguments
        session = session or relational.session

        user = cls.t
        result = session.execute(
            user.insert(),
            {"id": id, "userLogin": login})

        session.commit()
        return user
    @classmethod
    def list_members_Of_Group(cls,groupId,session=None):
        from .memberOfGroup import MemberOfGroup  # avoid circular import
        session = session or relational.session
        return (
            session.query(cls.m)
            .outerjoin(MemberOfGroup.m)
            .filter((MemberOfGroup.m.groupId == groupId))
        ).all()

    @classmethod
    def get_user(cls,userId,session=None):
        session = session or relational.session
        model=cls.m
        return (
            session.query(model)
            .filter(model.id == userId).first() 
        )