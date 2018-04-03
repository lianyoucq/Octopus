import os
from datetime import datetime
from pprint import pprint
from flask_testing import TestCase
from config import Config
from octopus import app
from octopus.common.path_utils import get_work_dir
from octopus.database.metadata import Domain, Node, INFA_ENV
from octopus.common.logger import rootLogger
from octopus.infa.infacmd.mrs import backupContents, listBackupFiles
from octopus.infa.infacmd import listServices, servicetype_namedtuple


class Test_infa_infacmd_mrs(TestCase):
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

    def tearDown(self):
        # super().tearDown()
        # it doesn't work as I expected. so it will be replaced by the test_9999_my_own_tearDown()
        pass

    def test_backupContents(self):
        servicesResult = listServices(ServiceType=servicetype_namedtuple.Model_Repository_Service)
        self.assertEqual(servicesResult.retcode, 0, servicesResult.stderr)

        services = servicesResult.stdout
        for service in services:
            outputfilename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%s")
            res = backupContents(ServiceName=service, OutputFileName=outputfilename)
            rootLogger.info(res)

