# -*- coding:utf-8 -*-
import os

from octopus.common.logger import mainLogger
from octopus.common.nodemeta_xml import Nodemeta
from octopus.common.url_utils import unquote
from octopus.database.metadata import INFA_ENV, Node, Domain
from octopus.exceptions import ParseNodemetaxmlExeption, NotFoundNodemetaxmlException


def load_metadata(nodemeta_xml_file):
    if not os.path.isfile(nodemeta_xml_file):
        raise NotFoundNodemetaxmlException("The nodemeta.xml file: {0} is not existing".format(nodemeta_xml_file))
    nodemeta = Nodemeta(nodemeta_xml_file=nodemeta_xml_file)
    domain = Domain()
    node = Node()
    infa_env = INFA_ENV()

    nodeConfig = nodemeta.get_NodeConfig()
    domain_dict = dict()
    domain_dict.setdefault("name", nodeConfig.get_domainName())
    try:
        dbConn = nodemeta.get_gw_DBConnectivity()
        domain_dict.setdefault("db_connectionstring", unquote(dbConn.get_dbConnectString()))
        domain_dict.setdefault("db_encryptedpassword", unquote(dbConn.get_dbEncryptedPassword()))
        domain_dict.setdefault("db_host", dbConn.get_dbHost())
        domain_dict.setdefault("db_service_name", dbConn.get_dbName())
        domain_dict.setdefault("db_port", dbConn.get_dbPort())
        domain_dict.setdefault("db_type", dbConn.get_dbType())
        domain_dict.setdefault("db_username", dbConn.get_dbUsername())
        domain_dict.setdefault("db_schema", dbConn.get_dbSchema())
        domain_dict.setdefault("db_tablespace", dbConn.get_dbTableSpace())
        domain_dict.setdefault("db_tls_enabled", dbConn.get_dbTLSEnabled())
        domain_dict.setdefault("db_truststore_location", unquote(dbConn.get_dbTruststoreLocation()))
        domain_dict.setdefault("db_trustedconnection", dbConn.get_trustedConnection())
        domain_dict.setdefault("db_truststorepassword", dbConn.get_truststorePassword())
    except Exception as e:
        mainLogger.exception(str(e))

    mainLogger.info("domain objects: {0}".format(domain_dict))
    domain.insert_domain(domain_dict)
    domain_output = domain.get_domain()  # type: Domain

    if domain_output is None:
        raise ParseNodemetaxmlExeption(
            "Couldn't parse the nodemeta.xml {0} for the domain information".format(nodemeta_xml_file))

    node_dict = dict()
    node_dict.setdefault("name", nodeConfig.get_nodeName())

    node_addr = nodeConfig.get_address()  # type: ds.NodeAddress
    mainLogger.debug("before node address is {0}".format(node_addr))
    node_addr = node_addr[0]
    mainLogger.debug("after node address is {0}".format(node_addr))
    print(dir(node_addr))
    node_dict.setdefault("nd_host", node_addr.get_host())
    node_dict.setdefault("nd_port", node_addr.get_port())
    node_dict.setdefault("nd_httpport", node_addr.get_httpPort())
    node_dict.setdefault("nd_logservicedir", unquote(nodeConfig.get_logServiceDir()))
    node_dict.setdefault("nd_options", nodeConfig.get_options())
    node_dict.setdefault("nd_resethostport", nodeConfig.get_resetHostPort())
    node_dict.setdefault("nd_systemlogdir", nodeConfig.get_systemLogDir())
    node_dict.setdefault("nd_tlsenabled", nodeConfig.get_tlsEnabled())

    sc = nodemeta.get_SecurityConfig()

    node_dict.setdefault("sc_secretkeysdirectory", unquote(sc.get_secretKeysDirectory()))
    node_dict.setdefault("sc_sitekeyhashvalue", unquote(sc.get_siteKeyHashValue()))
    node_dict.setdefault("sc_kerberosenabled", sc.get_kerberosEnabled())
    node_dict.setdefault("sc_keystore", sc.get_keystore())
    node_dict.setdefault("sc_keystorepassword", unquote(sc.get_keystorePassword()))
    node_dict.setdefault("sc_servicerealmname", sc.get_serviceRealmName())
    node_dict.setdefault("sc_ciphers", sc.get_ciphers())
    node_dict.setdefault("sc_nodesamlconfig", "\0".join(str(v) for v in sc.get_nodeSamlConfig()))
    node_dict.setdefault("sc_truststore", sc.get_trustStore())
    node_dict.setdefault("sc_truststorepassword", unquote(sc.get_trustStorePassword()))
    node_dict.setdefault("sc_nodeuseraccount", sc.get_nodeUserAccount())
    node_dict.setdefault("sc_userrealmname", sc.get_userRealmName())

    try:
        saml = nodemeta.get_NodeSamlConfig()
        node_dict.setdefault("samlenabled", saml.get_samlEnabled())
        node_dict.setdefault("samltruststore", saml.get_samlTrustStore())
        node_dict.setdefault("samltruststorepassword", unquote(saml.get_samlTrustStorePassword()))
    except Exception as e:
        mainLogger.exception(str(e))

    is_gateway_node = nodemeta.is_gateway_node()
    if is_gateway_node:
        node_dict.setdefault("adminconsoleport", nodeConfig.get_adminconsolePort())
        node_dict.setdefault("adminconsoleshutdownport", nodeConfig.get_adminconsoleShutdownPort())
    else:
        node_dict.setdefault("username", nodeConfig.get_username())
        node_dict.setdefault("securitydomain", nodeConfig.get_securityDomain())
        node_dict.setdefault("encryptedpassword", unquote(nodeConfig.get_encryptedPassword()))

    node_dict.setdefault("is_gateway", is_gateway_node)
    node_dict.setdefault("is_current_node", True)
    node_dict.setdefault("domain_id", domain_output.id)

    query_domain = domain.get_domain()  # type: Domain
    mainLogger.info("query from db: {0}".format(query_domain.name))

    mainLogger.info("the node value: {0}".format(node_dict))
    node.insert_node(node_dict)

    gateway_nodes_info = nodemeta.get_gateway_nodes_info_list()
    mainLogger.info("gateway nodes info is {0}".format(gateway_nodes_info))

    for gateway_node in gateway_nodes_info:  # type: dict
        nodeName = gateway_node.get("nodeName")
        host = gateway_node.get("host")
        port = gateway_node.get("port")
        httpPort = gateway_node.get("httpPort")

        if nodeName != node_dict.get("name"):
            node_dict_gw = dict()
            node_dict_gw.setdefault("name", nodeName)
            node_dict_gw.setdefault("nd_host", host)
            node_dict_gw.setdefault("nd_port", port)
            node_dict_gw.setdefault("nd_httpport", httpPort)
            node_dict_gw.setdefault("is_gateway", True)
            node_dict_gw.setdefault("is_current_node", False)
            node_dict_gw.setdefault("domain_id", domain_output.id)
            node.insert_node(node_dict_gw)

    # release them
    domain_dict = None
    domain_output = None
    node_dict = None