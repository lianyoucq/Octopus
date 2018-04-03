import os
from flask_testing import TestCase
from octopus import app
from config import Config
from octopus.common.path_utils import get_work_dir
from octopus.database.metadata import Domain, Node, INFA_ENV
from octopus.infa.infasetup import backupDomain
from octopus.common.logger import rootLogger


class TestInfaSetupCommand(TestCase):
    def create_app(self):
        self.app = app
        self.app.config.from_object(Config)
        self.app.config.update(SQLALCHEMY_BINDS={
            'octopus_db': Config.SQLALCHEMY_DATABASE_URI,
            'octopus_inner': "sqlite:///{0}/config.db".format(get_work_dir())
        })

        # json 正确显示中文，而不是unicode
        self.app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
        return self.app

    def setUp(self):
        domain_inst = Domain()
        self.domain = domain_inst.get_domain()
        node_inst = Node()
        self.node = node_inst.get_current_node()
        infa_env_inst = INFA_ENV()
        self.envs = infa_env_inst.get_envs(self.node.id)
        os.environ.update(self.envs)
        self.dis_name = "D102_INFA210"
        self.application = "app_wf_cuttlefish_hive2hive_failure"
        # self.application = "app_wf_cuttlefish_single2triple_test"

    def tearDown(self):
        # super().tearDown()
        # it doesn't work as I expected. so it will be replaced by the test_9999_my_own_tearDown()
        pass

    def test_10_backup_domain(self):
        res = backupDomain(domainname=self.domain.name,
                           databasetype=self.domain.db_type,
                           databaseaddress="{0}:{1}".format(self.domain.db_host.rstrip(),
                                                                       self.domain.db_port),
                           databaseusername=self.domain.db_username,
                           databaseservicename=self.domain.db_service_name,
                           backupfile=None,
                           force=False,
                           tablespace=self.domain.db_tablespace,
                           schemaname=self.domain.db_schema,
                           databasetlsenabled=self.domain.db_tls_enabled,
                           databasetruststorepassword=self.domain.db_truststorepassword,
                           trustedconnection=self.domain.db_trustedconnection,
                           encryptionkeylocation=self.node.sc_secretkeysdirectory,
                           databasetruststorelocation=self.domain.db_truststore_location
                           )

        rootLogger.info(res)
        self.assertEqual(res.retcode, 0, res.stdout)
        # a.nodes