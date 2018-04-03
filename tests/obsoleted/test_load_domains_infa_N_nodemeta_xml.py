from unittest import TestCase
import os
from octopus.utils.loadIntoInnerDB import load_domains_infa_N_nodemeta_xml
from octopus.common.path_utils import get_test_resources_dir
# from octopus.database.config import insert_new_envs, query_domain

import pprint
pp = pprint.PrettyPrinter(indent=4)


class TestLoad_domains_infa_N_nodemeta_xml(TestCase):

    domains_infa = os.path.join(get_test_resources_dir(), "domains.infa")

    nodemeta_xml = os.path.join(get_test_resources_dir(), "nodemeta_multigw.xml")
    nodemeta_worker_xml = os.path.join(get_test_resources_dir(), "nodemeta_worker.xml")
    nodemeta_210_6405_xml = os.path.join(get_test_resources_dir(), "nodemeta_210_6405.xml")

    def test_1_load_domains_infa_N_nodemeta_xml(self):
        value = load_domains_infa_N_nodemeta_xml(domains_infa_file=self.domains_infa,
                                                   nodemeta_xml_file=self.nodemeta_210_6405_xml)

    def test_2_insert_into_predefined_env(self):
        envs = {"INFA_HOME": "/home/arthur/opt/infa/10.1.1/PowerCenter",
                "INFA_DEFAULT_DOMAIN_USER":"admin",
                "INFA_DEFAULT_DOMAIN_PASSWORD": "w56tc9AaOo7lP467vsdZpg==",
                "INFA_DEFAULT_DATABASE_PASSWORD":"w56tc9AaOo7lP467vsdZpg==",
                "INFA_DEFAULT_SECURITY_DOMAIN":"Native"}
        # domain = query_domain()
        # insert_new_envs(domain.name, envs)