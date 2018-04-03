from unittest import TestCase
from octopus.common.nodemeta_xml import Nodemeta
import octopus.common.domainservice as ds
# -*- coding:utf-8 -*-
class TestNodemeta(TestCase):
    nodemeta = Nodemeta("resources/nodemeta_gw_130.xml")

    def test_get_exiting_types(self):
        print(self.nodemeta.get_exiting_types())

    def test_get_supported_dbTypes(self):
        pass

    def test_get_DBConnectivity(self):
        a = self.nodemeta.get_gw_DBConnectivity()

        print("##########################################")
        print("the dbconnection string is {0}".format(a.get_dbConnectString()))
        print("##########################################")

    def test_get_GatewayNodeConfig(self):
        gnc = self.nodemeta.get_gw_GatewayNodeConfig()
        print("##### address {0}".format(gnc.get_address()) )


######################################################################################################################
class TestNodemeta_Worker(TestCase):
    nodemeta = Nodemeta("resources/nodemeta_wk_deu.xml")

    def test_get_NodeAddress(self):
        nodeAddress_insts = self.nodemeta.get_NodeAddress_list()
        for nodeAddres in nodeAddress_insts: # type: ds.NodeAddress
            print()
            print(nodeAddres.get_host())
            print(nodeAddres.get_httpPort())
            print(nodeAddres.get_idref())
            print(nodeAddres.get_port())
            print(nodeAddres.get_id())

    def test_get_SecurityConfig(self):
        sc = self.nodemeta.get_SecurityConfig()
        print(sc.get_secretKeysDirectory())
        print(sc.get_siteKeyHashValue())

    def test_get_current_NodeConfig(self):
        nodeConfig = self.nodemeta.get_NodeConfig()
        print("###################################################")
        print(nodeConfig.nodeName)
        print(nodeConfig.domainName)
        print(dir(nodeConfig))

        print(nodeConfig.get_logServiceDir())

        print("##############################")
        nd = self.nodemeta.get_NodeConfig().get_address()[0] # type: ds.NodeAddress
        print(nd.get_httpPort())
        print(nd.get_host())


    def test_get_NodeSamlConfig(self):
        print(self.nodemeta.get_NodeSamlConfig())
