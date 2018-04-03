from flask_testing import TestCase
import os
from octopus import app
from config import Config
from octopus.common.logger import rootLogger
from octopus.common.path_utils import get_work_dir
from octopus.database.metadata import Domain, INFA_ENV, Node
from octopus.infa.infacmd.oie import deployApplication


# -*- coding:utf-8 -*-
class Test_INFA_INFACMD_OIE(TestCase):
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
        rootLogger.debug(os.environ.get("LD_LIBRARY_PATH"))
        os.environ.update({
            "LD_LIBRARY_PATH": '/home/arthur/opt/google/protobuf-3.5.1/lib:/idp1011/OperationsAPI/OperationsAPI_Java/lib:/opt/infa/pwc/1020/server/bin:/opt/infa/pwc/1020/services/shared/bin:/opt/infa/pwc/1020/ODBC7.1/lib:/opt/infa/pwc/1020/DataTransformation/bin:/lib:/usr/lib:/lib64:/usr/lib64:/lib:/home/arthur/opt/infa/10.2.0/PowerCenter/server/bin:/home/arthur/opt/10.2.0/shared/bin:/lib64:/usr/lib64:/lib:/usr/lib'})

        rootLogger.debug(os.environ.get("LD_LIBRARY_PATH"))


    def test_deployApplication(self):
        res = deployApplication(RepositoryService="M102_INFA210",
                                ApplicationPath="PRJ_DEV/app_wf_cuttlefish_hive2hive_failure",
                                OutputDirectory="/tmp")
        rootLogger.info(res)
