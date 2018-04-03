# -*- coding:utf-8 -*-
import os
import json
from tests.infaCliResponse_pb2 import InfaCliResponse
from requests import  get, post
from config import Config
from flask_testing import TestCase
from octopus import app
from octopus.common.path_utils import get_work_dir
from octopus.database.metadata import Domain, Node, INFA_ENV
from octopus.common.logger import rootLogger


class Test_api_infacmd_isp(TestCase):
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
        self.workflow_name = "wf_cuttlefish_single_triple_20180116"

        self.URL = "http://localhost"

        if Config.PORT:
            self.URL += ":{0}".format(Config.PORT)
        else:
            self.URL += ":{0}".format("5000")

        self.URL += "/api/infacmd/isp/"

    def __test_server_is_running(self, res, code=200):
        self.assertEqual(res.status_code, code, "the octopus server is not running")

    def __test_api_ret_status(self, retcode, failureMsg=None):
        self.assertEqual(retcode, 0, failureMsg)

    def test_ping_get(self):
        res = get(self.URL + "ping")
        rootLogger.info(res.content)
        self.__test_server_is_running(res)

    def __test_ping_post(self, args = {"ServiceName": "_adminconsole"}):
        res = post(self.URL + "ping", data=args)
        rootLogger.info(res)
        rootLogger.info(res.content)
        self.__test_server_is_running(res)
        if args.get("RT"):
            content = InfaCliResponse()
            content.ParseFromString(res.content)
            rootLogger.info("protobuf {0}".format(content))
            self.__test_api_ret_status(content.retcode, failureMsg=content.stdout)
        else:
            content = json.loads(res.content.decode())  # type: dict
            rootLogger.info(content.get("retcode"))
            self.__test_api_ret_status(content.get("retcode"), failureMsg=content.get("stdout"))

    def test_ping_post_json(self):
        self.__test_ping_post()

    def test_ping_post_proto(self):
        args = {"ServiceName": "_adminconsole", "RT":"PROTOBUF"}
        self.__test_ping_post(args)
