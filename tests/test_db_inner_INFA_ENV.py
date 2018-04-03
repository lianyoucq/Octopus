from flask_testing import TestCase
from octopus.database.metadata import INFA_ENV, Domain, Node
from octopus import app, db
from config import Config
from octopus.common.path_utils import get_work_dir
from octopus.common.logger import rootLogger as debugLogger
import copy


class TestINFA_ENV(TestCase):
    infa_env = INFA_ENV()
    node_name = "N_INFA210"
    env_name = "INFA_HOME"
    env = {env_name :"/opt/infa/pwc/9"}
    new_env = {env_name:"/opt/infa/pwc/1020"}

    mul_envs = {"ICMD_JAVA_OPTS":"-Xmx1024g",
            "INFA_DEFAULT_DOMAIN_USER":"admin",
            "INFA_DEFAULT_SECURITY_DOMAIN": "Native"}


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
        # _init_inner_db()
        debugLogger.info("before- the envs is {0}".format(self.mul_envs))
        self.now_all_envs = copy.deepcopy(self.mul_envs)
        for name, value in self.env.items():
            self.now_all_envs.setdefault(name, value)
        debugLogger.info("the now_all_envs is {0}".format(self.now_all_envs))
        debugLogger.info("the envs is {0}".format(self.mul_envs))
        debugLogger.info("")

        domain = Domain()
        self.current_domain = domain.get_domain()

        node = Node()
        self.current_node = node.get_current_node() # type: Node
        print("current node is {0}".format(self.current_node))
        if not self.current_node.is_gateway:
            self.assertWarns("the node {0} is not gateway, some operations are limited")

    # def test_0_my_own_setUp(self):
    #     _init_inner_db()
    #     self.now_all_envs = self.envs
    #     for name, value in self.env.items():
    #         self.now_all_envs.setdefault(name, value)

    def tearDown(self):
        # super().tearDown()
        # it doesn't work as I expected. so it will be replaced by the test_9999_my_own_tearDown()
        pass

    def test_9999_my_own_tearDown(self):
        # _drop_inner_db()
        pass


    def test_1_insert_env(self):
        self.infa_env.insert_env(self.current_node.id, env=self.env)

    def test_2_insert_envs(self):
        print(self.mul_envs)
        self.infa_env.insert_envs(self.current_node.id, envs=self.mul_envs)

    def test_50_update_env(self):
        self.infa_env.update_env(self.current_node.id, self.new_env)

    def test_90_delele_env(self):
        self.infa_env.delele_env(self.current_node.id, self.new_env)
        # del self.env
        # self.test_4_get_envs()
        out_envs = self.infa_env.get_envs(self.current_node.id)
        self.assertEqual(len(self.now_all_envs) -1, len(out_envs), "The {0} is already deleted".format(self.new_env))

    def test_3_get_env(self):
        my_env = self.infa_env.get_env(self.current_node.id, self.env_name)
        debugLogger.info("#### the test_get_env is {0} \n".format(my_env))
        self.assertTrue(my_env.__eq__(self.env), "the env in the db is same as the data")

    def test_4_get_envs(self):
        # self.skipTest("test it later")
        all_envs = self.infa_env.get_envs(self.current_node.id)
        debugLogger.info("the db is {0} \n".format(all_envs))

        debugLogger.info("existing is {0}".format(self.now_all_envs))
        self.assertEqual(len(all_envs), len(self.now_all_envs), "the number of envs is not equaled")
