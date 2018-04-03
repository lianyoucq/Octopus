# -*- coding:utf-8 -*-
import os
from pprint import pprint
from flask_testing import TestCase
from config import Config
from octopus import app
from octopus.common.path_utils import get_work_dir
from octopus.database.metadata import Domain, Node, INFA_ENV
from octopus.common.logger import rootLogger
from octopus.infa.infacmd import listApplications, startApplication, listApplicationObjects, stopBlazeService, \
    listServices, listConnections, servicetype_namedtuple, connectiontype_namedtupe, backupApplication, stopApplication


class Test_infa_infacmd_dis(TestCase):
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

    def test_1_listApplications(self):
        res = listApplications(domainname=self.domain.name, servicename=self.dis_name)
        rootLogger.info(res)
        rootLogger.warning(res.stderr)
        self.applications = res.stdout
        self.assertEqual(res.retcode, 0, "the listApplications command executed with failure: {0}".format(res.stderr))

    def test_2_startApplication(self):
        # res = startApplication( =self.domain.name, servicename=self.dis_name,
        #                        application=self.application)
        res = startApplication(ServiceName=self.dis_name, Application=self.application, DomainName=self.domain.name)

        rootLogger.info(res)

    def test_3_listApplicationObjects(self):
        res = listApplicationObjects(self.dis_name, self.application, domainname=self.domain.name,
                                     listobjecttype=True)

        rootLogger.info(res)
        objects = res.stdout
        if isinstance(objects, list):
            for obj in objects:
                rootLogger.info(obj)

    def test_4_stopBlazeService(self):
        servicesResult = listServices(ServiceType=servicetype_namedtuple.Data_Integration_Service)
        self.assertEqual(servicesResult.retcode, 0, servicesResult.stderr)
        connectionsResult = listConnections(ConnectionType=connectiontype_namedtupe.HADOOP)
        self.assertEqual(connectionsResult.retcode, 0, connectionsResult.stderr)

        services = servicesResult.stdout
        connections = connectionsResult.stdout.get(connectiontype_namedtupe.HADOOP)
        rootLogger.info("########## {0}".format(connections))
        for service in services:
            for connDict in connections:  # type: dict
                k, v = connDict.popitem()
                res = stopBlazeService(ServiceName=service, HadoopConnection=v)
                rootLogger.info(res)
                self.assertEqual(res.retcode, 0, res.stderr)

    def test_5_backupApplication(self):
        stopA = stopApplication(ServiceName=self.dis_name, Application=self.application)
        self.assertEqual(stopA.retcode, 0, stopA.stderr)
        res = backupApplication(ServiceName=self.dis_name, Application=self.application,
                                FileName="{0}.xml".format(self.application))
        self.assertEqual(res.retcode, 0, res.stderr)

        startA = startApplication(ServiceName=self.dis_name, Application=self.application)
        self.assertEqual(startA.retcode, 0, startA.stderr)
        rootLogger.info(res.stdout)
