from flask_testing import TestCase
from octopus.database.perftrace import _init_inner_db, Perftrace
from octopus import app, db
from config import Config
from octopus.common.path_utils import get_work_dir
from octopus.common.logger import rootLogger


# -*- coding:utf-8 -*-
class TestPerftrace(TestCase):
    def create_app(self):
        self.app = app
        self.app.config.from_object(Config)
        self.app.config.update(SQLALCHEMY_BINDS={
            'octopus_db': Config.SQLALCHEMY_DATABASE_URI,
            'octopus_inner': "sqlite:///{0}/config.db".format(get_work_dir())
        })

        return self.app

    def setUp(self):
        # super().setUp()
        # _drop_inner_db()
        _init_inner_db()

    def tearDown(self):
        # super().tearDown()
        # it doesn't work as I expected. so it will be replaced by the test_9999_my_own_tearDown()
        pass

    def test_insert(self):
        # a = Perftrace()
        # a.insert(cmd="Test command", cost=1.232)
        pass

