# -*- coding:utf-8 -*-
import octopus.common.domainservice as ds
from octopus.common.logger import mainLogger
from collections import namedtuple
from octopus.exceptions import NodeTagNotExistingException, NotFoundMetadataTypesException
from config import Config


class Nodemeta():
    def __init__(self, nodemeta_xml_file):
        mainLogger.info("invoking the Nodemeta class to parse the nodemeta.xml( {0} )".format(nodemeta_xml_file))
        self.node_xml_file = nodemeta_xml_file
        doc = ds.parsexml_(self.node_xml_file)
        self.rootNode = doc.getroot()
        doc = None

    def get_exiting_types(self) -> dict:
        output_dict = dict()
        t_c_n = namedtuple("nodeInfo", ["nodeClass", "node"])
        nodeAddress_list = list()
        for node in self.rootNode.getchildren():
            rootTag, rootClass = ds.get_root_tag(node)  # type: str, str
            mainLogger.debug("tag is {0} and class is {1}, the node is {2}".format(rootTag, rootClass, node))
            # NodeAddress will be multiple entries
            if rootTag == Config.PRED_METADATA_SCHEMA_TYPES.NodeAddress:
                nodeAddress_list.append(t_c_n(rootClass, node))
            else:
                output_dict.setdefault(rootTag, t_c_n(rootClass, node))
        if len(nodeAddress_list) != 0:
            output_dict.setdefault(Config.PRED_METADATA_SCHEMA_TYPES.NodeAddress, nodeAddress_list)
        mainLogger.info(output_dict)
        return output_dict

    def get_supported_db_types(self):
        TYPES = "DBType"
        pass

    def __get_defined_type_inst(self, tag, nodeClass=None, node=None):
        nodeInfo = namedtuple("nodeInfo", ["nodeClass", "node"])
        if nodeClass is not None and node is not None:
            mainLogger.debug("the nodeClass {0} and node {1}".format(nodeClass, node))
            nodeInfo=nodeInfo(nodeClass, node)
        else:
            exiting_types = self.get_exiting_types()
            nodeInfo = exiting_types.get(tag)  # type: namedtuple("nodeInfo", ["nodeClass", "node"])
            if nodeInfo is None:
                raise NodeTagNotExistingException(
                    "The node tag {0} is not exiting in the nodemeta.xml file".format(tag))

        mainLogger.info(nodeInfo)
        rootClazz = nodeInfo.nodeClass
        rootObj = rootClazz.factory()
        mainLogger.debug("the tag is {0} and the node is {1}".format(tag, nodeInfo.node))
        rootObj.build(nodeInfo.node)
        return rootObj

    def is_gateway_node(self):
        if Config.PRED_METADATA_SCHEMA_TYPES.GatewayNodeConfig in self.get_exiting_types().keys():
            return True
        return False

    def get_gw_DBConnectivity(self) -> ds.DBConnectivity:
        """获取DBConnection
        只有Gateway Node有DBConnectivity属性。
        :return: DBConnectivity
        """
        return self.__get_defined_type_inst(Config.PRED_METADATA_SCHEMA_TYPES.DBConnectivity)

    def get_gw_GatewayNodeConfig(self) -> ds.GatewayNodeConfig:
        return self.__get_defined_type_inst(Config.PRED_METADATA_SCHEMA_TYPES.GatewayNodeConfig)

    def get_wk_WorkerNodeConfig(self) -> ds.WorkerNodeConfig:
        return self.__get_defined_type_inst(Config.PRED_METADATA_SCHEMA_TYPES.WorkerNodeConfig)

    def get_NodeAddress_list(self) -> [ds.NodeAddress]:
        nodeAddress_list = self.get_exiting_types().get(Config.PRED_METADATA_SCHEMA_TYPES.NodeAddress)
        nodeAddress_inst_list = list()
        if nodeAddress_list is not None and len(nodeAddress_list) > 0:
            for nodeAddress in nodeAddress_list:
                nodeAddress_inst_list.append(self.__get_defined_type_inst(Config.PRED_METADATA_SCHEMA_TYPES.NodeAddress,
                                             nodeClass=nodeAddress.nodeClass,
                                             node=nodeAddress.node))
        return nodeAddress_inst_list

    def get_NodeRef_list(self) -> [ds.NodeRef]:
        portals = self.get_NodeConfig().get_portals()
        mainLogger.debug("portals is {0}".format(portals))
        nodeRef_inst_list = list()
        for portal in portals:
            mainLogger.error(dir(portal))
            nodeRefs  = portal.NodeRef
            for nodeRef in nodeRefs: # type: ds.NodeRef
                nodeRef_inst_list.append(nodeRef)
        return nodeRef_inst_list

    def get_gateway_nodes_info_list(self):
        node_address_list = self.get_NodeAddress_list()
        node_ref_list = self.get_NodeRef_list()

        gateway_node_info_list = list()
        for node_address in node_address_list: # type: ds.NodeAddress
            node_address_id  = node_address.get_id()
            host = node_address.get_host()
            port = node_address.get_port()
            http_port = node_address.get_httpPort()

            for node_ref in node_ref_list: # type: ds.NodeRef
                node_ref_address = node_ref.get_address()
                node_ref_nodename = node_ref.get_nodeName()
                if node_address_id == node_ref_address:
                    node_info_dict = dict()
                    node_info_dict.setdefault("host", host)
                    node_info_dict.setdefault("nodeName", node_ref_nodename)
                    node_info_dict.setdefault("httpPort", http_port)
                    node_info_dict.setdefault("port", port)
                    gateway_node_info_list.append(node_info_dict)
        return gateway_node_info_list

    def get_SecurityConfig(self) -> ds.SecurityConfig:
        nodeConfig = self.get_NodeConfig()
        security_config = nodeConfig.get_securityConfig()
        mainLogger.info(security_config)

        return security_config[0]

    def get_NodeConfig(self):
        """
        :return: GatewayNodeConfig | WorkerNodeConfig
        """
        # gateway nodes
        try:
            nodeConfig = self.get_gw_GatewayNodeConfig()
        except Exception as e:
            mainLogger.exception("{0}, and Will try to use the worker node configuration".format(str(e)))
            # worker nodes
            try:
                nodeConfig = self.get_wk_WorkerNodeConfig()
            except Exception as e:
                mainLogger.exception("Will try to use the worker node configuration")
                raise NotFoundMetadataTypesException("Neither the Gateway nor Worker node existing")
        return nodeConfig

    def get_current_NodeAddress(self) -> ds.NodeAddress:
        nd = self.get_NodeConfig().get_address()[0]  # type: ds.NodeAddress

        return nd

    def get_NodeSamlConfig(self) -> ds.NodeSamlConfig:
        samlConfig = self.__get_defined_type_inst(tag=Config.PRED_METADATA_SCHEMA_TYPES.NodeSamlConfig)

        return samlConfig