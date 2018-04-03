import os
from datetime import datetime
from unittest.mock import create_autospec
from collections import namedtuple

from flask_testing import TestCase

# from unittest import TestCase
from config import Config
from octopus import app
from octopus.common.logger import rootLogger
from octopus.common.path_utils import get_work_dir
from octopus.database.metadata import Domain, Node, INFA_ENV
from octopus.infa.infacmd import listServices, servicetype_namedtuple
from octopus.infa.infacmd.mrs import backupContents, listBackupFiles


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

    def test_listBackupFiles(self):
        listBackupFilesResult =namedtuple("ListBackupFilesResult", ['retcode', 'stdout', 'stderr'])
        listBackupFilesResult.stdout = """MRS_Jellyfish_Apr_2_2018.mrep
MRS_Jellyfish_Apr_2_2018_No2.mrep
SUCCESS: Backup files are listed.
Command ran successfully.
"""
        listBackupFilesResult.retcode = 0
        listBackupFilesResult.stderr = None

        listBackupFiles_mock = create_autospec(spec = listBackupFiles, return_value=listBackupFilesResult)
        mock_res  = listBackupFiles_mock(ServiceName="MRS_Jellyfish")
        print(",mock result is {0}".format(mock_res.stdout))
        # listBackupFiles_mock.assert_called_with(ServiceName="MRS_Jellyfish")

        # listBackupFiles_mock = Mock(spec=listBackupFiles(), return_value="hello")
        # print(listBackupFiles_mock())