# -*- coding:utf-8 -*-


class Dict2Attrib(dict):
    def __init__(self, *args, **kwargs):
        super(Dict2Attrib, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Config():
    SECRET_KEY = "Octopus@Secret"
    DEBUG = True
    PERFTRACE = True
    PORT = 5000
    HOST = '0.0.0.0'

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:infa@udid.sleety.com/octopus?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = False

    # informatica predefined environment variables
    PREDEFINED_ENV_VARIABLES = {
        "INFA_HOME": "INFA_HOME",
        "ICMD_JAVA_OPTS": "ICMD_JAVA_OPTS",
        "INFA_CLIENT_RESILIENCE_TIMEOUT": "INFA_CLIENT_RESILIENCE_TIMEOUT",
        "INFA_CODEPAGENAME": "INFA_CODEPAGENAME",
        "INFA_DEFAULT_DATABASE_PASSWORD": "INFA_DEFAULT_DATABASE_PASSWORD",
        "INFA_DEFAULT_DB_TRUSTSTORE_PASSWORD": "INFA_DEFAULT_DB_TRUSTSTORE_PASSWORD",
        "INFA_DEFAULT_DOMAIN": "INFA_DEFAULT_DOMAIN",
        "INFA_DEFAULT_DOMAIN_PASSWORD": "INFA_DEFAULT_DOMAIN_PASSWORD",
        "INFA_DEFAULT_DOMAIN_USER": "INFA_DEFAULT_DOMAIN_USER",
        "INFA_DEFAULT_PWX_OSEPASSWORD": "INFA_DEFAULT_PWX_OSEPASSWORD",
        "INFA_DEFAULT_PWX_OSPASSWORD": "INFA_DEFAULT_PWX_OSPASSWORD",
        "INFA_DEFAULT_SECURITY_DOMAIN": "INFA_DEFAULT_SECURITY_DOMAIN",
        "INFA_JAVA_CMD_OPTS": "INFA_JAVA_CMD_OPTS",
        "INFA_PASSWORD": "INFA_PASSWORD",
        "INFA_NODE_KEYSTORE_PASSWORD": "INFA_NODE_KEYSTORE_PASSWORD",
        "INFA_NODE_TRUSTSTORE_PASSWORD": "INFA_NODE_TRUSTSTORE_PASSWORD",
        "INFA_REPCNX_INFO": "INFA_REPCNX_INFO",
        "INFA_REPOSITORY_PASSWORD": "INFA_REPOSITORY_PASSWORD",
        "INFATOOL_DATEFORMAT": "INFATOOL_DATEFORMAT",
        "INFA_TRUSTSTORE": "INFA_TRUSTSTORE",
        "INFA_TRUSTSTORE_PASSWORD": "INFA_TRUSTSTORE_PASSWORD"
    }

    PREDEFINED_ENV_VARIABLES_ATTRIBUTE = Dict2Attrib(PREDEFINED_ENV_VARIABLES)

    PREDEFINED_CONTENT_TYPES = {
        "PROTOBUF": "application/x-protobuf",
        "JSON": "application/json"
    }

    __PREDEFINED_METADATA_SCHEMA_TYPES = {
        "GatewayNodeConfig": "GatewayNodeConfig",
        "DBConnectivity": "DBConnectivity",
        "WorkerNodeConfig": "WorkerNodeConfig",
        "NodeAddress": "NodeAddress",
        "NodeSamlConfig": "NodeSamlConfig",
        "NodeRef": "NodeRef",
    }

    PRED_METADATA_SCHEMA_TYPES = Dict2Attrib(__PREDEFINED_METADATA_SCHEMA_TYPES)
