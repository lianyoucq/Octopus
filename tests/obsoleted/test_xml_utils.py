from unittest import TestCase
import os
from octopus.common.xml_utils import Domains_Infa_XML, Nodemeta_XML
from octopus.common.path_utils import get_test_resources_dir
import pprint
pp = pprint.PrettyPrinter(indent=4)

# -*- coding:utf-8 -*-
class TestXml_utils(TestCase):
    domains_infa = os.path.join(get_test_resources_dir(), "domains.infa")
    dmXml = Domains_Infa_XML(domains_infa_file=domains_infa)

    nodemeta_xml = os.path.join(get_test_resources_dir(), "nodemeta_multigw.xml")
    nodemeta_worker_xml = os.path.join(get_test_resources_dir(), "nodemeta_worker.xml")
    nmXml = Nodemeta_XML(nodemeta_xml_file=nodemeta_xml)
    nm_wker_Xml = Nodemeta_XML(nodemeta_xml_file=nodemeta_worker_xml)

    def test_domains_infa_xml2dict(self):
        pp.pprint(self.dmXml.xml2dict())


    def test_nodemeta_xml_xml2dict(self):
        pp.pprint(self.nmXml.xml2dict())


    def test_nodemeta_worker_xml_xml2dict(self):
        pp.pprint(self.nm_wker_Xml.xml2dict())