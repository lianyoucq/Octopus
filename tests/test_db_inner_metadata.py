from flask_testing import TestCase
from octopus.database.metadata import _drop_inner_db, _init_inner_db
from octopus import app, db
from config import Config
from octopus.common.path_utils import get_work_dir, get_test_resources_dir
from octopus.common.logger import rootLogger as debugLogger
import copy
from octopus.utils.loadNodeMeta import load_metadata

# -*- coding:utf-8 -*-
class TestLoad_metadata(TestCase):
    node_name = "N_INFA210"
    env_name = "INFA_HOME"
    env = {env_name :"/opt/infa/pwc/9"}
    new_env = {env_name:"/opt/infa/pwc/1020"}

    mul_envs = {"ICMD_JAVA_OPTS":"-Xmx1024g",
            "INFA_DEFAULT_DOMAIN_USER":"admin",
            "INFA_DEFAULT_SECURITY_DOMAIN": "Native"}

    nodemeta_xml_file =get_test_resources_dir() + "/nodemeta_arthur-jellyfish.xml"
    # nodemeta_xml_file =get_test_resources_dir() + "/nodemeta_210_6405.xml"
    # nodemeta_xml_file =get_test_resources_dir() + "/nodemeta_gw_130.xml"
    # nodemeta_xml_file = get_test_resources_dir() + "/nodemeta_wk_deu.xml"

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
        # super().setUp()
        # _drop_inner_db()
        _init_inner_db()
        self.now_all_envs = copy.deepcopy(self.mul_envs)
        for name, value in self.env.items():
            self.now_all_envs.setdefault(name, value)


    def tearDown(self):
        # super().tearDown()
        # it doesn't work as I expected. so it will be replaced by the test_9999_my_own_tearDown()
        pass

    def test_9999_my_own_tearDown(self):
        # _drop_inner_db()
        pass
    #
    def test_1_load_metadata(self):
        import  os
        print(self.nodemeta_xml_file)
        print(os.path.isfile(self.nodemeta_xml_file))
        if os.path.isfile(self.nodemeta_xml_file):
            load_metadata(nodemeta_xml_file=self.nodemeta_xml_file)


