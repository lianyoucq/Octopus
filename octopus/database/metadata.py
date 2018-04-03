# -*- coding:utf-8 -*-
import copy

from octopus.common.logger import mainLogger
from octopus.database import db
from octopus.exceptions import ParameterTypeIsInvalidatedException


# ######################################################################################################################
# Database metadata
# ######################################################################################################################
def _init_inner_db():
    """Init the inner database"""
    db.create_all(bind="octopus_inner")


def _drop_inner_db():
    """Drop the inner database"""
    db.drop_all(bind="octopus_inner")


class INFA_ENV(db.Model):
    '''环境变量
    为Node存储`Informatica`环境变量, environment name and value
    '''
    __tablename__ = "infa_env"
    __bind_key__ = "octopus_inner"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    value = db.Column(db.String(1000), nullable=False)
    node_id = db.Column(db.Integer, db.ForeignKey("node.id"), nullable=False)
    node = db.relationship("Node", backref="envs")

    def __repr__(self) -> str:
        return "id={0}, node_id={1}, name={2}, value={3}".format(self.id, self.node_id, self.name, self.value)

    def __init__(self, name=None, value=None, node_id=None):
        super().__init__()
        self.name = name
        self.value = value
        self.node_id = node_id

    def insert_env(self, node_id: int, env: dict):
        """插入一条环境变量信息
        :param node_id: node id
        :param env: 环境变量字典
        :return: 如果成功为None，否者，抛出异常
        :rtype: None|ParameterTypeIsInvalidatedException
        """
        if isinstance(env, dict):
            tmp_env = copy.deepcopy(env)
            name, value = tmp_env.popitem()
            new_env = self.__class__(name=name, value=value, node_id=node_id)
            db.session.add(new_env)
            db.session.commit()
            mainLogger.debug("Insert the {0} into infa_env".format(new_env))
            return new_env
        else:
            errmsg = "{0} should be dict".format(env)
            mainLogger.error(errmsg)
            raise ParameterTypeIsInvalidatedException(errmsg)

    def insert_envs(self, node_id: int, envs: dict) -> None:
        """插入多条环境变量信息
        :param node_id: node id
        :param envs: 环境变量字典
        :return: None
        :exception: ParameterTypeIsInvalidatedException
        """
        if isinstance(envs, dict):
            for name, value in envs.items():
                db.session.add(self.__class__(name=name, value=value, node_id=node_id))
            db.session.commit()
            mainLogger.debug("insert {0} into infa_env".format(envs))
        else:
            errmsg = "{0} should be dict".format(envs)
            mainLogger.error(errmsg)
            raise ParameterTypeIsInvalidatedException(errmsg)

    def update_env(self, node_id: int, env) -> None:
        """更新一个环境变量
        :param node_id: node id
        :param env: 新的环境变量字典
        :return: None
        :exception: ParameterTypeIsInvalidatedException
        """
        if isinstance(env, dict):
            temp_env = copy.deepcopy(env)
            name, value = temp_env.popitem()
            upd_env = self.query.filter(self.__class__.name == name,
                                        self.__class__.node_id == node_id).first()
            mainLogger.debug("INFA_ENV: Old value is {0}".format(upd_env))
            upd_env.value = value
            db.session.commit()
            mainLogger.debug("INFA_ENV: New value is {0}".format(upd_env))
        elif isinstance(env, self.__class__):
            upd_env = self.query.filter(self.__class__.node_id == env.node_id,
                                        self.__class__.name == env.name).first()
            upd_env.value = env.value
            db.session.commit()
        else:
            errmsg = "{0} should be dict or instance of {1}".format(env, self.__class__)
            mainLogger.error(errmsg)
            raise ParameterTypeIsInvalidatedException(errmsg)

    def delele_env(self, node_id: int, env) -> None:
        """
        删除一个环境变量
        :param node_id: node_id
        :param env: 环境变量字典
        :type env: str | dict
        :return: None
        :exception: ParameterTypeIsInvalidatedException
        """
        if isinstance(env, dict):
            temp_env = copy.deepcopy(env)
            name, value = temp_env.popitem()
        else:
            name = env
        del_env = self.query.filter(self.__class__.name == name,
                                    self.__class__.node_id == node_id).first()
        mainLogger.debug("{0} This will be deleted".format(del_env))
        db.session.delete(del_env)
        db.session.commit()

    def get_env(self, node_id: int, env_name: str) -> dict:
        """
        获取一个环境变量值
        :param node_id: node id
        :param env: 环境变量名
        :return: 环境变量字典|None
        """

        my_env = self.query.filter(self.__class__.name == env_name,
                                   self.__class__.node_id == node_id).first()
        mainLogger.debug(my_env)
        out_dict = dict()
        if my_env is not None:
            out_dict.setdefault(my_env.name, my_env.value)
        return out_dict

    def get_envs(self, node_id: int) -> dict:
        """
        获取节点所有环境变量设置
        :param node_id: node id
        :return: 环境变量字典
        """
        my_envs = self.query.filter(self.__class__.node_id == node_id).all()
        envs_dict = dict()
        for env in my_envs:  # type: self.__class__
            envs_dict.setdefault(env.name, env.value)
        mainLogger.debug(envs_dict)
        return envs_dict


class Domain(db.Model):
    """Domain
    """
    __tablename__ = 'domain'
    __bind_key__ = "octopus_inner"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False, unique=True)

    # domain database configuration
    db_connectionstring = db.Column(db.String(200), nullable=True)
    db_encryptedpassword = db.Column(db.String(100), nullable=True)
    db_host = db.Column(db.String(100), nullable=True)
    db_service_name = db.Column(db.String(150), nullable=True)
    db_port = db.Column(db.Integer, nullable=True)
    db_type = db.Column(db.String(50), nullable=True)
    db_username = db.Column(db.String(200), nullable=True)
    db_schema = db.Column(db.String(200), nullable=True)
    db_tablespace = db.Column(db.String(200), nullable=True)
    db_tls_enabled = db.Column(db.Boolean, nullable=True)
    db_truststore_location = db.Column(db.String(200), nullable=True)
    db_trustedconnection = db.Column(db.Boolean, nullable=True)
    db_truststorepassword = db.Column(db.String(200), nullable=True)

    # relations： domain has many nodes
    nodes = db.relationship("Node", backref="domain", lazy=True)

    def __init__(self, name=None, db_connectionstring=None, db_encryptedpassword=None, db_host=None,
                 db_service_name=None, db_port=None, db_type=None, db_username=None, db_schema=None, db_tablespace=None,
                 db_tls_enabled=None, db_truststore_location=None, db_trustedconnection=None,
                 db_truststorepassword=None):
        super().__init__()
        self.name = name
        self.db_connectionstring = db_connectionstring
        self.db_encryptedpassword = db_encryptedpassword
        self.db_host = db_host
        self.db_service_name = db_service_name
        self.db_port = db_port
        self.db_type = db_type
        self.db_username = db_username
        self.db_schema = db_schema
        self.db_tablespace = db_tablespace
        self.db_tls_enabled = db_tls_enabled
        self.db_truststore_location = db_truststore_location
        self.db_trustedconnection = db_trustedconnection
        self.db_truststorepassword = db_truststorepassword

    def insert_domain(self, domain) -> None:
        """
        新加入一条Domain
        :param domain: dict或者Domain的实例
        :return:
        """
        if isinstance(domain, dict):
            my_domain = self.__class__()
            for key, value in domain.items():
                if hasattr(my_domain, key):
                    setattr(my_domain, key, value)
                else:
                    mainLogger.warn("the {0}={1} is not for Domain".format(key, value))
        elif isinstance(domain, self.__class__):
            my_domain = domain
        db.session.add(my_domain)
        db.session.commit()


    def update_domain(self, domain: dict) -> None:
        my_domain = self.query.get(1)
        if isinstance(domain, dict):
            for key, value in domain.items():
                if hasattr(my_domain, key):
                    setattr(my_domain, key, value)
                else:
                    mainLogger.warn("the {0}={1} is not for Domain".format(key, value))
        elif isinstance(domain, self.__class__):
            my_domain = domain
            # only one record
            my_domain.id = 1
        db.session.commit()

    def delete_domain(self) -> None:
        del_domain = self.query.get(1)
        db.session.delete(del_domain)
        db.session.commit()

    def get_domain(self):
        return self.query.get(1)


class Node(db.Model):
    '''Node'''
    __tablename__ = 'node'
    __bind_key__ = "octopus_inner"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=True)

    nd_host = db.Column(db.String(200), nullable=False)
    nd_port = db.Column(db.Integer, nullable=False)
    nd_httpport = db.Column(db.Integer, nullable=False)
    nd_logservicedir = db.Column(db.String(200), nullable=True)
    nd_options = db.Column(db.String(200), nullable=True)
    nd_resethostport = db.Column(db.Integer, nullable=True)
    nd_systemlogdir = db.Column(db.String(200), nullable=True)
    nd_tlsenabled = db.Column(db.Boolean, nullable=True)

    sc_secretkeysdirectory = db.Column(db.String(200), nullable=True)
    sc_sitekeyhashvalue = db.Column(db.String(200), nullable=True)
    sc_kerberosenabled = db.Column(db.Boolean, nullable=True)
    sc_keystore = db.Column(db.String(200), nullable=True)
    sc_keystorepassword = db.Column(db.String(200), nullable=True)
    sc_servicerealmname = db.Column(db.String(200), nullable=True)
    sc_ciphers = db.Column(db.String(200), nullable=True)
    sc_nodesamlconfig = db.Column(db.String(200), nullable=True)
    sc_truststore = db.Column(db.String(200), nullable=True)
    sc_truststorepassword = db.Column(db.String(200), nullable=True)
    sc_nodeuseraccount = db.Column(db.String(200), nullable=True)
    sc_userrealmname = db.Column(db.String(200), nullable=True)

    samlenabled = db.Column(db.Boolean, nullable=True, default=False)
    samltruststore = db.Column(db.String(200), nullable=True)
    samltruststorepassword = db.Column(db.String(200), nullable=True)

    # Only gateway node has these two properties
    adminconsoleport = db.Column(db.Integer, nullable=True)
    adminconsoleshutdownport = db.Column(db.Integer, nullable=True)

    # only worker has these three propteries
    username = db.Column(db.String(200), nullable=True)
    securitydomain = db.Column(db.String(200), nullable=True)
    encryptedpassword = db.Column(db.String(200), nullable=True)

    # is gateway node or worker node?
    is_gateway = db.Column(db.Boolean, nullable=False)
    # is running?
    is_available = db.Column(db.Boolean, nullable=True)
    # is current node
    is_current_node = db.Column(db.Boolean, nullable=False)

    domain_id = db.Column(db.Integer, db.ForeignKey("domain.id"), nullable=False)

    def insert_node(self, node: dict) -> None:
        if isinstance(node, dict):
            new_node = Node()
            for key, value in node.items():
                if hasattr(new_node, key):
                    setattr(new_node, key, value)
                else:
                    mainLogger.warn("During the insert, the {0}={1} is not for Node".format(key, value))
        elif isinstance(node, self.__class__):
            new_node = node
        else:
            mainLogger.error("the node {0} is not supported".format(node))
        db.session.add(new_node)
        db.session.commit()

    def update_node(self, node: dict) -> None:
        upd_node = self.query.filter(self.__class__.id == node.get("id")).first()
        for key, value in node.items():
            if hasattr(upd_node, key):
                setattr(upd_node, key, value)
            else:
                mainLogger.warn("During the update, the {0}={1} is not for Node".format(key, value))
        db.session.update(upd_node)
        db.session.commit()
        mainLogger.info("Updated the node: {0}".format(upd_node))

    def delete_node(self, node: dict) -> None:
        del_node = self.query.filter(self.__class__.id == node.get("id")).first()
        if del_node is not None:
            db.session.delete(del_node)
            db.session.commit()
            mainLogger.info("Delete the node: {0} successful".format(del_node))
        else:
            mainLogger.warn("this node {0} is not existing, so couldn't delete it".format(node))

    def get_current_node(self):
        return self.query.filter(self.__class__.is_current_node == True).first()

    def get_nodes(self):
        return self.query.all()


class KeyFiles(db.Model):
    '''核心文件或者目录的sha1sum
    '''
    __tablename__ = 'key_files'
    __bind_key__ = 'octopus_inner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # domains.infa
    domains_infa_sha1sum = db.Column(db.String(50), nullable=False)
    domains_infa = db.Column(db.Text, nullable=False)
    # nodemeta.xml
    nodemeta_xml_sha1sum = db.Column(db.String(50), nullable=False)
    nodemeta_xml = db.Column(db.Text, nullable=False)
    # siteKey
    sitekey_sha1sum = db.Column(db.String(50), nullable=False)
    sitekey = db.Column(db.Binary, nullable=False)

    def __repr__(self):
        return "id={0}, domains_infa_sha1sum={1}, nodemeta_xml_sha1sum={2}," \
               " sitekey_sha1sum={3}".format(self.id,
                                             self.domains_infa_sha1sum,
                                             self.nodemeta_xml_sha1sum,
                                             self.sitekey_sha1sum)


def get_current_domain():
    domain = Domain()
    return domain.get_domain()


def get_current_node() -> Node:
    node = Node()
    return  node.get_current_node()  # type: Node


def get_current_node_infa_envs(env_name: str=None):
    current_node = get_current_node()
    infa_env = INFA_ENV()
    if env_name:
        env_value = infa_env.get_env(current_node.id, env_name=env_name)
        return env_value
    else:
        infa_envs = infa_env.get_envs(current_node.id)
        return infa_envs
