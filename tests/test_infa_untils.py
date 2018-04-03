import os
from flask_testing import TestCase
from octopus.infa.utils import pmpasswd
from octopus.database.metadata import INFA_ENV, Domain, Node
from octopus import app
from config import Config
from octopus.common.path_utils import get_work_dir
from octopus.common.logger import rootLogger


# -*- coding:utf-8 -*-
class TestInfaUntils(TestCase):
    def create_app(self):
        self.app = app
        self.app.config.from_object(Config)
        self.app.config.update(SQLALCHEMY_BINDS={
            'octopus_db': Config.SQLALCHEMY_DATABASE_URI,
            'octopus_inner': "sqlite:///{0}/config.db".format(get_work_dir())
        })

        return self.app

    def setUp(self):
        domain_inst = Domain()
        self.domain = domain_inst.get_domain()
        node_inst = Node()
        self.node = node_inst.get_current_node()
        infa_env_inst = INFA_ENV()
        self.envs = infa_env_inst.get_envs(self.node.id)
        os.environ.update(self.envs)

    def test_pmpasswd(self):
        pmpasswdResult = pmpasswd("/opt/infa/pwc/1020", "CRYPT_DATA")
        self.assertEqual(pmpasswdResult.retcode, 0, pmpasswdResult.stdout)
        rootLogger.debug(pmpasswdResult.stdout)
