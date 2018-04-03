# -*- coding:utf-8 -*-
"""
`worker`
{   'current_node_config': {   'host': 'infa211.sleety.com',
                               'httpPort': '6405',
                               'port': '6406',
                               '{http://com.informatica.imx}id': 'ID_1',
                               '{http://www.w3.org/2001/XMLSchema-instance}type': 'mgt:NodeAddress'},
    'domain_node_info': {   'domainName': 'DM102_INFA210',
                            'encryptedPassword': 'GYYJdd8lWyo5cXRbEieV6Q%3D%3D',
                            'nodeName': 'Node_infa211',
                            'securityDomain': 'Native',
                            'username': 'admin',
                            '{http://com.informatica.imx}id': 'U:JS1U7OPQEeesxSEpImVFMw'},
    'gateway_nodes': [   {   'host': 'infa210.sleety.com',
                             'httpPort': '6405',
                             'port': '6406',
                             '{http://com.informatica.imx}id': 'ID_3'}],
    'securityConfig': {   'secretKeysDirectory': '/opt/infa/pwc/1020/isp/config/keys',
                          'siteKeyHashValue': 'RmZZliVMAFxODoD2m+22jXnk0mo=',
                          '{http://com.informatica.imx}id': 'ID_4',
                          '{http://www.w3.org/2001/XMLSchema-instance}type': 'domainservice:SecurityConfig'}}

`Gateway`
{   'current_node_config': {   'host': 'infa211.sleety.com',
                               'httpPort': '6205',
                               'port': '6206',
                               '{http://com.informatica.imx}id': 'ID_2',
                               '{http://com.informatica.imx}iid': '104',
                               '{http://www.w3.org/2001/XMLSchema-instance}type': 'mgt:NodeAddress'},
    'domain_db_config': {   'dbEncryptedPassword': 'lr2VQMjg5iehwwYvPB3ipg%3D%3D',
                            'dbHost': 'ora119.sleety.com',
                            'dbName': 'ora119.sleety.com',
                            'dbPort': '1521',
                            'dbType': 'ORACLE',
                            'dbUsername': 'INFA_961_DOMAIN_210',
                            '{http://com.informatica.imx}id': 'ID_1'},
    'domain_node_info': {   'adminconsolePort': '6208',
                            'adminconsoleShutdownPort': '6209',
                            'dbConnectivity': 'ID_1',
                            'domainName': 'DM_INFA210',
                            'nodeName': 'ND_INFA211',
                            '{http://com.informatica.imx}id': 'U:P0rSAiMsEeakBpkdJbk0sw'},
    'gateway_nodes': [   {   'address': 'ID_4',
                             'host': 'infa211.sleety.com',
                             'httpPort': '6205',
                             'nodeName': 'ND_INFA211',
                             'port': '6206',
                             '{http://com.informatica.imx}id': 'ID_3',
                             '{http://com.informatica.imx}iid': '104',
                             '{http://www.w3.org/2001/XMLSchema-instance}type': 'mgt:NodeRef'},
                         {   'address': 'ID_6',
                             'host': 'infa210.sleety.com',
                             'httpPort': '6005',
                             'nodeName': 'ND_INFA210',
                             'port': '6006',
                             '{http://com.informatica.imx}id': 'ID_5',
                             '{http://com.informatica.imx}iid': '564',
                             '{http://www.w3.org/2001/XMLSchema-instance}type': 'mgt:NodeRef'}],
    'securityConfig': {   'secretKeysDirectory': '/opt/infa/pwcnode/961/isp/config/keys',
                          'siteKeyHashValue': 'cIorzeOgFGZ6W56+fyYGroR1XaI=',
                          '{http://com.informatica.imx}id': 'ID_7',
                          '{http://www.w3.org/2001/XMLSchema-instance}type': 'domainservice:SecurityConfig'}}
"""

import xml.etree.ElementTree as ET
from octopus.common.logger import mainLogger
import urllib.parse as urlparse


class Domains_Infa_XML():
    def __init__(self, domains_infa_file):
        self.domains_infa = domains_infa_file
        mainLogger.info(self.domains_infa)

    def __parse(self):
        tree = ET.parse(self.domains_infa)
        root = tree.getroot()
        mainLogger.debug("root.tag = {0}, root.text={1}, root.attrib={2}".format(root.tag, root.text, root.attrib))
        vector_dict = dict()
        vector_list = list()
        for vectors in root:
            for vector in vectors:
                tag = vector.tag  # type: str
                text = vector.text  # type: str
                if tag.lower() == 'address':
                    for addr in vector:
                        tag = addr.tag
                        text = addr.text
                        vector_dict.setdefault(tag, text)
                else:
                    vector_dict.setdefault(tag, text)
            vector_list.append(vector_dict)
        return vector_list

    def xml2dict(self):
        return self.__parse()


class Nodemeta_XML():
    def __init__(self, nodemeta_xml_file):
        self.nodemeta_xml = nodemeta_xml_file
        mainLogger.debug( self.nodemeta_xml)

    def __parse(self):
        tree = ET.parse(self.nodemeta_xml)
        root = tree.getroot()
        nodemeta_xml_dict = dict()
        nodes_list = list()
        ha_nodes_list = list()
        gateway_node_for_worker_node_info = list()
        for entity in root:
            tag = entity.tag  # type: str
            text = entity.text  # type: str
            attrib = entity.attrib  # type: dict
            mainLogger.debug( "tag={0} \t text={1} \t attrib={2}".format(tag, text, attrib))

            # Gateway信息
            if tag.lower().__contains__("GatewayNodeConfig".lower()):
                current_gw_dict = dict()
                current_gw_dict.setdefault("domain_node_info", attrib)
                mainLogger.debug( current_gw_dict)
                # append current gw dict
                nodemeta_xml_dict.update(current_gw_dict)

                for gw_entity in entity:
                    tag = gw_entity.tag
                    text = gw_entity.text
                    attrib = gw_entity.attrib

                    self.__parse_address(gw_entity, nodemeta_xml_dict )

                    self.__parse_portals(tag, gw_entity, ha_nodes_list)

                    self.__parse_security_config(tag, gw_entity, nodemeta_xml_dict)

            # worknode 信息
            """
            <domainservice:WorkerNodeConfig imx:id="U:JS1U7OPQEeesxSEpImVFMw" domainName="DM102_INFA210" nodeName="Node_infa211" encryptedPassword="GYYJdd8lWyo5cXRbEieV6Q%3D%3D" securityDomain="Native" username="admin">
            <address imx:id="ID_1" xsi:type="mgt:NodeAddress" host="infa211.sleety.com" httpPort="6405" port="6406"/>
            <portals>
            <NodeRef imx:id="ID_2" xsi:type="mgt:NodeRef" address="ID_3" nodeName="ND_INFA210"/>
            </portals>
            <securityConfig imx:id="ID_4" xsi:type="domainservice:SecurityConfig" secretKeysDirectory="%2Fopt%2Finfa%2Fpwc%2F1020%2Fisp%2Fconfig%2Fkeys" siteKeyHashValue="RmZZliVMAFxODoD2m%2B22jXnk0mo%3D"/>
            </domainservice:WorkerNodeConfig>
            <mgt:NodeAddress imx:id="ID_3" host="infa210.sleety.com" httpPort="6405" port="6406"/>
            """
            if tag.lower().__contains__("WorkerNodeConfig".lower()):
                current_worker_node_config = {"domain_node_info": attrib}
                for wk_entity in entity:
                    tag = wk_entity.tag # type: str
                    attrib = wk_entity.attrib # type: dict

                    self.__parse_address(wk_entity, nodemeta_xml_dict)

                    self.__parse_portals(tag, wk_entity, gateway_node_for_worker_node_info)
                    self.__parse_security_config(tag, attrib, current_worker_node_config)

                nodemeta_xml_dict.update({"gateway_nodes": gateway_node_for_worker_node_info})
                nodemeta_xml_dict.update(current_worker_node_config)
            # 如果Domain里有多少个节点，这里也会有多少个节点信息，包括host， httpPort和domain Port
            if tag.lower().__contains__("nodeaddress"):
                nodes_list.append(attrib)

            # Domain数据库链接信息
            if tag.lower().__contains__("DBConnectivity".lower()):
                domain_db_dict = dict()
                domain_db_dict.setdefault("domain_db_config", attrib)
                nodemeta_xml_dict.update(domain_db_dict)

        nodemeta_xml_dict.update({"gateway_nodes_detail": nodes_list})
        nodemeta_xml_dict.update({"gateway_nodes": ha_nodes_list})

        self.__recombination(nodemeta_xml_dict)

        return nodemeta_xml_dict

    def __parse_address(self,entry, container: dict):
        current_node_config = dict()
        if entry.tag.lower().__contains__("address"):
            current_node_config.setdefault("current_node_config", entry.attrib)
            container.update(current_node_config)

    def __parse_portals(self, tag, gw_entity, container: list):
        # portals, 如果是HA，那么这里会有多个HA节点
        if tag.lower().__contains__("portals"):
            for portal in gw_entity:
                attrib = portal.attrib
                container.append(attrib)

    def __parse_security_config(self, tag: str, entry: dict, container: dict):
        if tag.lower().__contains__("securityconfig"):
            drip_urlquotes = dict()
            for key, value in entry.items():
                drip_urlquotes.setdefault(key, urlparse.unquote(value))
            container.update({"securityConfig": drip_urlquotes})

    def __recombination(self, config: dict):
        gw_nodes_list = list()
        ha_nodes = config.get("gateway_nodes")
        nodes = config.get("gateway_nodes_detail")

        for node in nodes:
            gw_nodes = dict()
            gw_nodes.update(node)
            for ha_node in ha_nodes:
                if node.get("{http://com.informatica.imx}id") == ha_node.get("address"):
                    gw_nodes.update(ha_node)

            gw_nodes_list.append(gw_nodes)

        # discard the  gateway_nodes and gateway_nodes_detail
        config.pop("gateway_nodes")
        config.pop("gateway_nodes_detail")
        config.update({"gateway_nodes": gw_nodes_list})
        return gw_nodes_list


    def xml2dict(self):
        return self.__parse()
