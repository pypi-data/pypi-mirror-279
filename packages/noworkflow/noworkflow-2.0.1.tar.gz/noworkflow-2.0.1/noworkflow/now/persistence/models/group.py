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
class Group(AlchemyProxy):
    __tablename__ = "group"
    id = Column( 
        String, unique=True, primary_key=True
    )
    name = Column(String, unique=True)
    
    @classmethod  # query
    def create(cls, grp, session=None):
        
        # pylint: disable=too-many-arguments
        session = session or relational.session

        grop = cls.t
        id=uuid_gen()
        result = session.execute(
            grop.insert(),
            {"id": id, "name": grp.name})

        session.commit()
        grp.id=id
        return grp
    @classmethod  # query
    def delete(cls, grpId, session=None):

        # pylint: disable=too-many-arguments
        session = session or relational.session

        model=cls.m
        session = session or relational.session

        session.query(model).filter(model.id==grpId).delete()
        session.commit()