# -*- coding:utf-8 -*-
from octopus.database.metadata import _drop_inner_db, _init_inner_db
from flask_script import Manager
from octopus import app
from octopus.common.logger import rootLogger

manager = Manager(app)


@manager.command
def init_innerdb():
    """Init the inner database"""
    rootLogger.info("Now Init the inner database")
    _init_inner_db()
    rootLogger.info("Complete to Init the inner database")


@manager.command
def drop_innerdb():
    """Drop the inner database"""
    _drop_inner_db()


if __name__ == '__main__':
    manager.run()