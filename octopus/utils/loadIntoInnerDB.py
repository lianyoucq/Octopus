# -*- coding:utf-8 -*-
from octopus.common.xml_utils import Domains_Infa_XML, Nodemeta_XML
from octopus.database.config import insert_node, query_nodes, insert_domain, query_domain, insert_new_envs,\
    Node, Domain, INFA_ENV
from config import Config
from octopus.common.logger import mainLogger


def load_domains_infa_N_nodemeta_xml(domains_infa_file, nodemeta_xml_file):
    dmXml = Domains_Infa_XML(domains_infa_file=domains_infa_file)
    domains_list = dmXml.xml2dict()  # type: list
    nmXml = Nodemeta_XML(nodemeta_xml_file=nodemeta_xml_file)
    nodemeta_dict = nmXml.xml2dict()  # type: dict
    domain_db_config = nodemeta_dict.get("domain_db_config")
    current_node_config = nodemeta_dict.get("current_node_config") # type: dict
    domain_node_info = nodemeta_dict.get("domain_node_info")
    gateway_nodes = nodemeta_dict.get("gateway_nodes")
    securityConfig = nodemeta_dict.get("securityConfig")

    kerberos_enabled = False
    saml_enabled = False
    tls_enabled = False
    domain_name = None
    db_schema = None
    db_service_name = None
    db_tablespace = None
    db_type = None
    db_username = None
    db_host = None
    db_port = None
    is_current_node = False
    for domain_node in domains_list:
        domain_name = domain_node.get("domainName")
        host = domain_node.get("host")
        kerberos_enabled = domain_node.get("kerberosEnabled")
        port = domain_node.get('port')
        tls_enabled = domain_node.get('tlsEnabled')
        for gw_node in gateway_nodes:
            if gw_node.get("host") == host and gw_node.get('httpPort') == port:
                domain_name = domain_node.get("domainName")
                host = domain_node.get("host")
                kerberos_enabled = domain_node.get("kerberosEnabled")
                port = domain_node.get('port')
                tls_enabled = domain_node.get('tlsEnabled')
                break


    # 如果domain_db_config存在的话，那么当前这个节点就是Gateway类型
    if domain_db_config is not None:
        db_tablespace = domain_db_config.get("dbTableSpace")
        db_schema = domain_db_config.get("dbSchema")
        db_host = domain_db_config.get("dbHost")
        db_port = domain_db_config.get("dbPort")
        db_service_name = domain_db_config.get("dbName")
        db_type = domain_db_config.get("dbType")
        db_username = domain_db_config.get("dbUsername")

        domain_inst = Domain(name=domain_name,
                             saml_enabled=saml_enabled,
                             kerberos_enabled=kerberos_enabled,
                             tls_enabled=tls_enabled,
                             db_tablespace=db_tablespace,
                             db_schema=db_schema,
                             db_host=db_host,
                             db_port=db_port,
                             db_service_name=db_service_name,
                             db_type=db_type,
                             db_username=db_username
                             )

        insert_domain(domain_inst)

    is_gateway_for_current_node = False
    # gateways nodes
    for gw_node in gateway_nodes:
        if current_node_config.get("host") == gw_node.get("host") \
                and current_node_config.get("port") == gw_node.get("port") \
                and current_node_config.get("httpPort") == gw_node.get("httpPort"):
            is_gateway_for_current_node = True
            is_current_node = True
        else:
            is_current_node = False
        node = Node(ac_port=domain_node_info.get("adminconsolePort"),
                    ac_shutdown_port=domain_node_info.get("adminconsoleShutdownPort"),
                    domain_name=domain_node_info.get('domainName'),
                    host=gw_node.get("host"),
                    http_port=gw_node.get("httpPort"),
                    is_gateway=True,
                    name=gw_node.get("nodeName"),
                    node_port=gw_node.get("port"),
                    is_current_node = is_current_node
                    )
        print("node is {0}".format(node))
        insert_node(node)



    # 检查当前节点
    # 如果在gateway_nodes里，那么就当前节点已经添加了，否者将作为worker 节点加入。
    if not is_gateway_for_current_node:
        # 如果是worker node，那么domains.infa应该只有一条记录
        domain_node_for_current_worker_node = domains_list[0]
        name = domain_node_for_current_worker_node.get("domainName")
        host = domain_node_for_current_worker_node.get("host")
        kerberos_enabled = domain_node_for_current_worker_node.get("kerberosEnabled")
        port = domain_node_for_current_worker_node.get('port')
        tls_enabled = domain_node_for_current_worker_node.get('tlsEnabled')
        """
        'current_node_config': {   'host': 'infa211.sleety.com',
                                           'httpPort': '6205',
                                           'port': '6206',
                                           '{http://com.informatica.imx}id': 'ID_2',
                                           '{http://com.informatica.imx}iid': '104',
                                           '{http://www.w3.org/2001/XMLSchema-instance}type': 'mgt:NodeAddress'},
        """
        node = Node(
                    domain_name=domain_name,
                    host=current_node_config.get("host"),
                    http_port=current_node_config.get("httpPort"),
                    is_gateway=False,
                    name=domain_node_info.get("nodeName"),
                    node_port=current_node_config.get("port"),
                    is_current_node = True
                    )
        print("node is {0}".format(node))
        insert_node(node)



