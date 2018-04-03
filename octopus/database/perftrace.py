# -*- coding:utf-8 -*-
from octopus.database import db
from datetime import datetime
from octopus.common.logger import rootLogger


# ######################################################################################################################
# Database metadata
# ######################################################################################################################
def _init_inner_db():
    """Init the inner database"""
    db.create_all(bind="octopus_db")


#
#
# def _drop_inner_db():
#     """Drop the inner database"""
#     db.drop_all(bind="octopus_db")


class Perftrace(db.Model):
    '''环境变量
    为Node存储`Informatica`环境变量, environment name and value
    '''
    __tablename__ = "perftrace"
    __bind_key__ = "octopus_db"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    cmd = db.Column(db.String(1000), nullable=False, unique=False)
    retcode = db.Column(db.SmallInteger, nullable=False, unique=False)
    executing_date = db.Column(db.TIMESTAMP, nullable=False, unique=False)
    cost = db.Column(db.DECIMAL(20, 10), nullable=False, unique=False)
    comments = db.Column(db.String(100), nullable=True, unique=False)

    def insert(self, cmd: str, cost, retcode: int, executing_date=datetime.now(), comments=None):
        perf_trace = self.__class__(cmd=cmd, executing_date=executing_date, cost=cost, retcode=retcode,
                                    comments=comments)
        db.session.add(perf_trace)
        db.session.commit()
        rootLogger.debug("{0} is inserted successfully.".format(perf_trace))
        return perf_trace

    def __repr__(self):
        return "cmd: {0}; cost: {1}; executing_date: {2}; comments: {3}".format(self.cmd, self.cost,
                                                                                self.executing_date, self.comments)
