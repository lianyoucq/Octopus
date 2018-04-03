import os
from pprint import pprint

from flask_testing import TestCase

from config import Config
from octopus import app
from octopus.common.logger import rootLogger
from octopus.common.path_utils import get_work_dir
from octopus.database.metadata import Domain, INFA_ENV, Node
from octopus.infa.infacmd import listMappings, runMapping, getMappingStatus, getRequestLog, listMappingParams
from octopus.infa.infacmd import servicetype_namedtuple, listServices, listApplications, listWorkflows


# -*- coding:utf-8 -*-
class TestInfacmdMS(TestCase):
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

        servicesResult = listServices(self.domain.name, ServiceType=servicetype_namedtuple.Data_Integration_Service)
        self.assertEqual(servicesResult.retcode, 0, servicesResult.stderr)
        if len(servicesResult.stdout) > 0:
            self.DIS_SERVICE = servicesResult.stdout[0]
        else:
            self.fail("There's no DIS services in the Domain {0}".format(self.domain.name))

        appResults = listApplications(servicename=self.DIS_SERVICE)
        self.assertEqual(appResults.retcode, 0, appResults.stderr)
        if len(appResults.stdout) > 0:
            self.APPLICATION = appResults.stdout[0]
        else:
            self.fail("There's no Applications under the services {0}".format(self.DIS_SERVICE))

        wkfResult = listWorkflows(DomainName=self.domain.name, ServiceName=self.DIS_SERVICE,
                                  Application=self.APPLICATION)
        self.assertEqual(wkfResult.retcode, 0, wkfResult.stderr)
        if len(wkfResult.stdout) > 0:
            self.WKF = wkfResult.stdout[0]
        else:
            self.fail("There's no workflow under the application {0}".format(self.APPLICATION))

    def test_1_listMappings(self):
        res = listMappings(DomainName=self.domain.name, ServiceName=self.DIS_SERVICE, Application=self.APPLICATION)
        rootLogger.info(res)
        self.assertEqual(res.retcode, 0, res.stderr)
        return res.stdout

    def test_2_runMapping(self):
        mappingsResult = listMappings(DomainName=self.domain.name, ServiceName=self.DIS_SERVICE,
                                      Application=self.APPLICATION)
        self.assertEqual(mappingsResult.retcode, 0, mappingsResult.stderr)
        mappings = mappingsResult.stdout
        if mappings is not None and len(mappings) != 0:
            res = runMapping(DomainName=self.domain.name, ServiceName=self.DIS_SERVICE, Application=self.APPLICATION,
                             Mapping=mappings[0])
            rootLogger.info(res)
            self.assertEqual(res.retcode, 0, res.stderr)
            return res.stdout
        else:
            rootLogger.warning("no mapping in the application {0}".format(self.APPLICATION))
            self.fail("no mapping in the application {0}".format(self.APPLICATION))

    def test_3_getMappingStatus(self):
        mapping_status = self.test_2_runMapping()
        if mapping_status is not None:
            res = getMappingStatus(DomainName=self.domain.name, ServiceName=mapping_status.ServiceName,
                                   JobId=mapping_status.JobId)
            rootLogger.info(res)
            self.assertEqual(res.retcode, 0, res.stderr)

    def test_4_getRequestLog(self):
        mapping_info = self.test_2_runMapping()
        if mapping_info is not None:
            logFileName = "/tmp/{0}.log".format(mapping_info.JobId)
            res = getRequestLog(DomainName=self.domain.name, ServiceName=mapping_info.ServiceName,
                                RequestId=mapping_info.JobId, FileName=logFileName)
            rootLogger.info(res)
            self.assertEqual(res.retcode, 0, res.stderr)

    def test_listMappingParams(self):
        mappingsResult = listMappings(ServiceName=self.DIS_SERVICE, Application=self.APPLICATION)
        self.assertEqual(mappingsResult.retcode, 0, mappingsResult.stdout)
        if len(mappingsResult.stdout) < 0:
            self.fail("There's no mapping under the application {0}".format(self.APPLICATION))
        for mapping in mappingsResult.stdout:
            res = listMappingParams(ServiceName=self.DIS_SERVICE, Application=self.APPLICATION, Mapping=mapping)
            # self.assertEqual(res.retcode, 0, res.stdout)
            rootLogger.info("###### {0}".format(res))
            print("###" * 20)
            print()
            pprint(res.stdout)
            print("###" * 20)
            print(res.stdout)
