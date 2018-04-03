# -*- coding:utf-8 -*-
import os
from pprint import pprint
from flask_testing import TestCase
from config import Config
from octopus import app
from octopus.common.path_utils import get_work_dir
from octopus.database.metadata import Domain, INFA_ENV, Node
from octopus.infa.infacmd import startWorkflow, listWorkflows, listTasks, listActiveWorkflowInstances, listWorkflowParams, \
    listServices, servicetype_namedtuple, listApplications
from octopus.common.logger import rootLogger


class TestInfacmdWfs(TestCase):
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
        # self.application = "app_wf_cuttlefish_hive2hive_failure"
        self.application = "app_wf_cuttlefish_single2triple_test"
        self.workflow_name = "wf_cuttlefish_single_triple_20180116"

        self.application2 = "app_wf_cuttlefish_hive2hive_failure"

    def test_10_startWorkflow(self):
        self.skipTest("it will last a long time")
        rootLogger.info("start workflow with wait")
        res = startWorkflow(self.domain.name, self.dis_name, self.application, self.workflow_name, True)
        rootLogger.info(res)
        self.assertEqual(res.retcode, 0, res.stderr)
        rootLogger.warning(res.stderr)

    def test_11_startWorkflow(self):
        rootLogger.info("start workflow without wait")
        res = startWorkflow(self.domain.name, self.dis_name, self.application, self.workflow_name)
        rootLogger.info(res)
        self.assertEqual(res.retcode, 0, res.stderr)
        rootLogger.warning(res.stderr)

    def test_20_listWorkflows(self):
        res = listWorkflows(self.domain.name, self.dis_name, self.application2)
        rootLogger.info(res)
        self.assertEqual(res.retcode, 0, res.stderr)

    def test_30_listTasks(self):
        res = listTasks(self.domain.name, self.dis_name)
        rootLogger.info(res)
        self.assertEqual(res.retcode, 0, res.stderr)

    def test_40_listActiveWorkflowInstances(self):
        res = listActiveWorkflowInstances(self.domain.name, self.dis_name)
        rootLogger.info(res)
        self.assertEqual(res.retcode, 0, res.stderr)
        activeWkfInst = res.stdout
        for wkfInst in activeWkfInst:
            rootLogger.info(wkfInst)

    def test_50_listWorkflowParams(self):
        servicesResult = listServices(ServiceType=servicetype_namedtuple.Data_Integration_Service)
        self.assertEqual(servicesResult.retcode, 0, servicesResult.stderr)
        services = servicesResult.stdout
        for service in services:
            applicationsResult = listApplications(servicename=service)
            self.assertEqual(applicationsResult.retcode, 0, applicationsResult.stderr)
            applications = applicationsResult.stdout
            for application in applications:
                wkfResults = listWorkflows(DomainName=self.domain.name, ServiceName=service, Application=application)
                self.assertEqual(wkfResults.retcode, 0, wkfResults.stderr)
                wkfs = wkfResults.stdout
                for wkf in wkfs:
                    res = listWorkflowParams(ServiceName=service, Application=application, Workflow=wkf)
                    self.assertEqual(res.retcode, 0, res.stderr)
                    rootLogger.info(res)
                    print()
                    pprint(res.stdout)
