# # -*- coding:utf-8 -*-
# from octopus.database import db
# from octopus.exceptions import ParameterTypeIsInvalidatedException
# from octopus.mgt.logger import mainLogger, DEBUG, ERROR, WARNING, INFO
#
#
# class INFA_ENV_1(db.Model):
#     '''环境变量
#     为每个Domain存储`Informatica`环境变量, environment name and value
#     '''
#     __tablename__ = "infa_env_1"
#     __bind_key__ = "migpie_inner"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(150), nullable=False, unique=True)
#     value = db.Column(db.String(1000), nullable=False)
#     node_domain_name = db.Column(db.String(20), db.ForeignKey("node.domain_name"), nullable=False)
#     node = db.relationship("Node", backref="envs")
#
#     def __repr__(self):
#         return "id={0}, node_id={1}, name={2}, value={3}".format(self.id, self.node_domain_name, self.name, self.value)
#
#
# class Domain_1(db.Model):
#     '''Domain信息
#     主要从`domains.infa`和`nodemeta.xml`获取，一个domain至少有一个节点
#     '''
#     __tablename__ = 'domain_1'
#     __bind_key__ = "migpie_inner"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(150), nullable=False, unique=True)
#     db_connectionstring = db.Column(db.String(200), nullable=True)
#     db_encryptedpassword = db.Column(db.String(100), nullable=True)
#     db_host = db.Column(db.String(100), nullable=True)
#     db_service_name = db.Column(db.String(150), nullable=True)
#     db_port = db.Column(db.Integer, nullable=True)
#     db_type = db.Column(db.String(50), nullable=True)
#     db_username = db.Column(db.String(200), nullable=True)
#     db_schema = db.Column(db.String(200), nullable=True)
#     db_tablespace = db.Column(db.String(200), nullable=True)
#     db_tls_enabled = db.Column(db.Boolean, nullable=True)
#     db_truststore_location = db.Column(db.String(200), nullable=True)
#     db_trustedConnection = db.Column(db.Boolean, nullable=True)
#     db_truststorePassword = db.Column(db.String(200), nullable=True)
#     sc_secretKeysDirectory = db.Column(db.String(200), nullable=True)
#     tls_enabled = db.Column(db.Boolean, nullable=False, default=False)
#     kerberos_enabled = db.Column(db.Boolean, nullable=False, default=False)
#     saml_enabled = db.Column(db.Boolean, nullable=False, default=False)
#
#     # relations： domain has many nodes
#     nodes = db.relationship("Node", backref="domain", lazy=True)
#
#     def __repr__(self):
#         return "id={0}, name={1}, db_encryptedpassword={2}, db_host={3}, db_service_name={4}, db_port={5}, " \
#                "db_type={6}, db_username={7}, db_tablespace={8}, tls_enabled={9}, kerberos_enabled={10}, " \
#                "saml_enabled={11}".format(self.id, self.name, self.db_encryptedpassword, self.db_host,
#                                           self.db_service_name, self.db_port, self.db_type, self.db_username,
#                                           self.db_schema, self.db_tablespace, self.tls_enabled, self.kerberos_enabled,
#                                           self.saml_enabled)
#
#
# class Node_1(db.Model):
#     '''节点信息
#     全部从`nodemeta.xml`获取
#     '''
#     __tablename__ = 'node_1'
#     __bind_key__ = "migpie_inner"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # 如果worker节点是获取不到gateway nodename的
#     name = db.Column(db.String(150), nullable=True)
#     host = db.Column(db.String(150), nullable=False)
#     is_gateway = db.Column(db.Boolean, nullable=False)
#     ac_port = db.Column(db.Integer, nullable=True)
#     ac_shutdown_port = db.Column(db.Integer, nullable=True)
#     http_port = db.Column(db.Integer, nullable=True)
#     node_port = db.Column(db.Integer, nullable=True)
#     is_current_node = db.Column(db.Boolean, nullable=False)
#     domain_name = db.Column(db.Integer, db.ForeignKey("domain.name"), nullable=False)
#     # domain = db.relationship("Domain", back_populates="nodes")
#     # envs = db.relationship("INFA_ENV", backref="node")
#
#     def __repr__(self):
#         return "id={0}, name={1}, host={2}, is_gateway={3}, ac_port={4}, ac_shutdown_port={5}, " \
#                 "http_port={6}, node_port={7}, domain_name={8}, is_current_node={9}".format(self.id, self.name,
#                 self.host, self.is_gateway, self.ac_port, self.ac_shutdown_port, self.http_port, self.node_port,
#                 self.domain_name, self.is_current_node)
#
# class KeyFiles_1(db.Model):
#     '''核心文件或者目录的sha1sum
#     '''
#     __tablename__ = 'key_files_1'
#     __bind_key__ = 'migpie_inner'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # domains.infa
#     domains_infa_sha1sum = db.Column(db.String(50), nullable=False)
#     domains_infa = db.Column(db.Text, nullable=False)
#     # nodemeta.xml
#     nodemeta_xml_sha1sum = db.Column(db.String(50), nullable=False)
#     nodemeta_xml = db.Column(db.Text, nullable=False)
#     # siteKey
#     sitekey_sha1sum = db.Column(db.String(50), nullable=False)
#     sitekey = db.Column(db.Binary, nullable=False)
#
#     def __repr__(self):
#         return "id={0}, domains_infa_sha1sum={1}, nodemeta_xml_sha1sum={2}, sitekey_sha1sum={3}".format(self.id,
#                 self.domains_infa_sha1sum, self.nodemeta_xml_sha1sum, self.sitekey_sha1sum)
#
#
#
# # ######################################################################################################################
# # INFA environment variables
# # ######################################################################################################################
# def insert_an_new_env(node_id: str, env: dict):
#     """插入一条环境变量信息
#     :param node_id: node id
#     :param env: 环境变量字典
#     :return: 如果成功为None，否者，抛出异常
#     :rtype: None|ParameterTypeIsInvalidatedException
#     """
#     if isinstance(env, dict):
#         new_env = INFA_ENV(name=env.get('name'), value=env.get('value'), node_domain_name=node_id)
#         db.session.add(new_env)
#         db.session.commit()
#         mainLogger.log(DEBUG, "Insert the {0} into infa_env".format(new_env))
#     else:
#         errmsg = "{0} should be dict".format(env)
#         mainLogger.log(ERROR, errmsg )
#         raise ParameterTypeIsInvalidatedException(errmsg)
#
#
# def insert_new_envs(domain_name: str, envs: dict) -> None:
#     """插入多条环境变量信息
#     :param node_id: node id
#     :param envs: 环境变量字典
#     :return: None
#     :exception: ParameterTypeIsInvalidatedException
#     """
#     if isinstance(envs, dict):
#         for name, value in envs.items():
#             db.session.add(INFA_ENV(name=name, value=value, node_domain_name=domain_name))
#         db.session.commit()
#         mainLogger.log(DEBUG, "insert {0} into infa_env".format(envs))
#     else:
#         errmsg = "{0} should be dict".format(envs)
#         mainLogger.log(ERROR, errmsg)
#         raise ParameterTypeIsInvalidatedException(errmsg)
#
#
# def update_env(domain_name: str, env) -> None:
#     """更新一个环境变量
#     :param node_id: node id
#     :param env: 新的环境变量字典
#     :return: None
#     :exception: ParameterTypeIsInvalidatedException
#     """
#     if isinstance(env, dict):
#         name, value = env.popitem()
#         upd_env = db.session.query(INFA_ENV).filter(INFA_ENV.name == name,
#                                                        INFA_ENV.node_domain_name ==domain_name).first()
#         mainLogger.log(DEBUG, "INFA_ENV: Old value is {0}".format(upd_env))
#         upd_env['value'] = value
#         db.session.update(upd_env)
#         db.session.commit()
#         mainLogger.log(DEBUG, "INFA_ENV: New value is {0}".format(upd_env))
#     elif isinstance(env, INFA_ENV):
#         db.session.update(env)
#         db.session.commit()
#     else:
#         errmsg = "{0} should be dict".format(env)
#         mainLogger.log(ERROR, errmsg)
#         raise ParameterTypeIsInvalidatedException(errmsg)
#
#
# def delele_env(domain_name: str, env) -> None:
#     """
#     删除一个环境变量
#     :param node_id: node id
#     :param env: 环境变量字典
#     :type env: str | dict
#     :return: None
#     :exception: ParameterTypeIsInvalidatedException
#     """
#     if isinstance(env, dict):
#         name, value = env.popitem()
#     else:
#         name = env
#     del_env = db.session.query(INFA_ENV).filter(INFA_ENV.name == name,
#                                                    INFA_ENV.node_domain_name == domain_name).first()
#     mainLogger.log(DEBUG, "{0} This will be deleted".format(del_env))
#     db.session.delete(del_env)
#
#
# def get_env(domain_name: str, env: str) -> dict:
#     """
#     获取一个环境变量值
#     :param node_id: node id
#     :param env: 环境变量名
#     :return: 环境变量字典|None
#     """
#     my_env = db.session.query(INFA_ENV).filter(INFA_ENV.name == env, INFA_ENV.node_domain_name == domain_name).first()
#     mainLogger.log(DEBUG, my_env)
#     return my_env
#
#
# def get_envs(domain_name: str) -> dict:
#     """
#     获取节点所有环境变量设置
#     :param node_id: node id
#     :return: 环境变量字典
#     """
#     my_envs = db.session.query(INFA_ENV).filter(INFA_ENV.node_domain_name == domain_name).all()
#     envs_dict = dict()
#     for env in my_envs: # type: INFA_ENV
#         envs_dict.setdefault(env.name, env.value)
#     mainLogger.log(DEBUG, envs_dict)
#     return envs_dict
#
#
# # ######################################################################################################################
# # Domain
# # ######################################################################################################################
# def insert_domain(domain) -> None:
#     if isinstance(domain, dict):
#         my_domain = Domain()
#         for key, value in domain.items():
#             if hasattr(my_domain, key):
#                 setattr(my_domain, key, value)
#             else:
#                 mainLogger.log(WARNING, "the {0}={1} is not for Domain".format(key, value))
#     elif isinstance(domain, Domain):
#         my_domain = domain
#     db.session.add(my_domain)
#     db.session.commit()
#
#
# def update_domain(domain: dict) -> None:
#     my_domain = db.session.query(Domain).first()
#     for key, value in domain.items():
#         if hasattr(my_domain, key):
#             setattr(my_domain, key, value)
#         else:
#             mainLogger.log(WARNING, "the {0}={1} is not for Domain".format(key, value))
#     db.session.update(my_domain)
#     db.session.commit()
#
#
# def delete_domain() -> None:
#     del_domain = db.session.query(Domain).first()
#     db.session.delete(del_domain)
#     db.session.commit()
#
#
# def query_domain() -> Domain:
#     return db.session.query(Domain).first()
#
#
# # ######################################################################################################################
# # Node
# # ######################################################################################################################
# def insert_node(node: dict) -> None:
#     if isinstance(node, dict):
#         new_node = Node()
#         for key, value in node.items():
#             if hasattr(new_node, key):
#                 setattr(new_node, key, value)
#             else:
#                 mainLogger.log(WARNING, "During the insert, the {0}={1} is not for Node".format(key, value))
#     elif isinstance(node, Node):
#         new_node = node
#
#     db.session.add(new_node)
#     db.session.commit()
#
#
# def update_node(node: dict) -> None:
#     upd_node = db.session.query(Node).filter(Node.id == node.get("id")).first()
#     for key, value in node.items():
#         if hasattr(upd_node, key):
#             setattr(upd_node, key, value)
#         else:
#             mainLogger.log(WARNING, "During the update, the {0}={1} is not for Node".format(key, value))
#     db.session.update(upd_node)
#     db.session.commit()
#     mainLogger.log(INFO, "Updated the node: {0}".format(upd_node))
#
#
# def delete_node(node: dict) -> None:
#     del_node = db.session.query(Node).filter(Node.id == node.get("id")).first()
#     if del_node is not None:
#         db.session.delete(del_node)
#         db.session.commit()
#         mainLogger.log(INFO, "Delete the node: {0} successful".format(del_node))
#     else:
#         mainLogger.log(WARNING, "this node {0} is not existing, so couldn't delete it".format(node))
#
# def query_nodes():
#     return db.session.query(Node).all()
#
#
# # ######################################################################################################################
# # Database metadata
# # ######################################################################################################################
# def _init_inner_db():
#     """Init the inner database"""
#     db.create_all(bind="migpie_inner")
#
#
# def _drop_inner_db():
#     """Drop the inner database"""
#     db.drop_all(bind="migpie_inner")
