import os
from pprint import pprint
from flask_testing import TestCase
from config import Config
from octopus import app
from octopus.common.path_utils import get_work_dir
from octopus.database.metadata import Domain, INFA_ENV, Node
from octopus.infa.infacmd import listServices, ping, servicetype_namedtuple, listServiceNodes, listServiceLevels, \
    listServicePrivileges, listLicenses, showLicense, enableService, disableService, getServiceStatus, listAllUsers, \
    listConnections, listNodeResources, listConnectionOptions, listNodes, listUserPermissions, listUserPrivileges, \
    listGroupsForUser, purgeLog, resetPassword
from octopus.common.logger import rootLogger


class Test_infa_infacmd_isp(TestCase):
    def create_app(self):
        self.app = app
        self.app.config.from_object(Config)
        self.app.config.update(SQLALCHEMY_BINDS={
            'octopus_db': Config.SQLALCHEMY_DATABASE_URI,
            'octopus_inner': "sqlite:///{0}/config.db".format(get_work_dir())
        })

        # json 正确显示中文，而不是unicode
        self.app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
        return self.app

    def setUp(self):
        domain_inst = Domain()
        self.domain = domain_inst.get_domain()
        node_inst = Node()
        self.node = node_inst.get_current_node()
        infa_env_inst = INFA_ENV()
        self.envs = infa_env_inst.get_envs(self.node.id)
        os.environ.update(self.envs)
        self.dis_name = "D102_INFA210"
        self.application = "app_wf_cuttlefish_hive2hive_failure"
        # self.application = "app_wf_cuttlefish_single2triple_test"
        self.workflow_name = "wf_cuttlefish_single_triple_20180116"

    def test_listServiceLevels(self):
        res = listServiceLevels()
        rootLogger.info(res)

    def test_listServices(self):
        res = listServices(DomainName=self.domain.name,
                           ServiceType=servicetype_namedtuple.Model_Repository_Service)

        rootLogger.info(res)
        self.assertEqual(res.retcode, 0, res.stderr)

        res = listServices(DomainName=self.domain.name)

        rootLogger.info(res)

        return res.stdout

    def test_listServiceNodes(self):
        services = self.test_listServices()
        for service in services:
            res = listServiceNodes(ServiceName=service)
            rootLogger.info(res)
            self.assertEqual(res.retcode, 0, res.stderr)

    def test_listServicePrivileges(self):
        res = listServicePrivileges()
        rootLogger.info(res)

    def test_ping(self):
        services = listServices(DomainName=self.domain.name,
                                ServiceType=servicetype_namedtuple.Data_Integration_Service)
        self.assertEqual(services.retcode, 0, services.stderr)
        if services.retcode == 0:
            stdout = services.stdout
            for s in stdout:
                res = ping(ServiceName=s, DomainName=self.domain.name)
                rootLogger.info(res)
                self.assertEqual(res.retcode, 0, res.stderr)

    def test_listLicenses(self):
        licenses = listLicenses()
        rootLogger.info(licenses)

    def test_showLicense(self):
        licensesResult = listLicenses()
        if licensesResult.retcode == 0:
            licenses = licensesResult.stdout
            rootLogger.info(licenses)
            for license in licenses:
                licenseInfo = showLicense(LicenseName=license.Name)
                rootLogger.info(licenseInfo)

    def test_getServiceStatus(self):
        services = listServices()
        for service in services.stdout:
            res = getServiceStatus(ServiceName=service)
            rootLogger.info(res)

    def test_enableService(self):
        servicesResult = listServices(ServiceType=servicetype_namedtuple.PowerCenter_Integration_Service)
        self.assertEqual(servicesResult.retcode, 0, servicesResult.stderr)

        for service in servicesResult.stdout:  # type: str
            statusResult = getServiceStatus(ServiceName=service)
            rootLogger.info(statusResult)
            self.assertEqual(statusResult.retcode, 0, statusResult.stderr)
            if not statusResult.stdout:
                res = enableService(ServiceName=service)
            else:
                res = disableService(ServiceName=service)
            rootLogger.info(res)
            self.assertEqual(res.retcode, 0, res.stderr)

    def test_disableService(self):
        self.test_enableService()

    def test_listAllUsers(self):
        allUsers = listAllUsers()
        rootLogger.info(allUsers)

    def test_listConnections(self):
        allConnections = listConnections()
        rootLogger.info(allConnections)
        self.assertEqual(allConnections.retcode, 0, allConnections.stderr)
        pprint(allConnections.stdout)

    def test_listConnectionOptions(self):
        allConnectionsResult = listConnections()
        if allConnectionsResult.retcode == 0:
            allConnections = allConnectionsResult.stdout  # type: dict
            for k, v in allConnections.items():
                if len(v) > 0:
                    print(v)
                    for conn in v:
                        res = listConnectionOptions(ConnectionName=conn.get("name"))
                        rootLogger.info(res)
                        pprint(res.stdout)

    def test_listNodes(self):
        nodesResult = listNodes()
        self.assertEqual(nodesResult.retcode, 0, nodesResult.stderr)
        nodes = nodesResult.stdout
        rootLogger.info(nodes)

    def test_listNodeResources(self):
        nodeResult = listNodes()
        self.assertEqual(nodeResult.retcode, 0, nodeResult.stderr)

        nodes = nodeResult.stdout
        for node in nodes:
            rootLogger.info("######################\t{0}".format(node))
            res = listNodeResources(NodeName=node)
            rootLogger.info(res)
            self.assertEqual(res.retcode, 0, res.stderr)
            print()
            pprint(res.stdout)

    def test_listUserPermissions(self):
        usersResult = listAllUsers()
        self.assertEqual(usersResult.retcode, 0, usersResult.stderr)
        for userDict in usersResult.stdout:  # type: dict
            userPermissionsResult = listUserPermissions(ExistingUserName=userDict.get("userName"),
                                                        ExistingUserSecurityDomain=userDict.get("securityDomain"))
            rootLogger.info(userPermissionsResult)
            self.assertEqual(userPermissionsResult.retcode, 0, userPermissionsResult.stderr)
            pprint(userPermissionsResult.stdout)
            self.assertTrue(isinstance(userPermissionsResult.stdout, dict),
                            "The result of listUserPermissions shoudl be dict ")

    def test_listUserPrivileges(self):
        servicesResult = listServices(ServiceType=servicetype_namedtuple.PowerCenter_Repository_Service)
        usersResult = listAllUsers()
        self.assertEqual(servicesResult.retcode, 0, servicesResult.stderr)
        self.assertEqual(usersResult.retcode, 0, usersResult.stderr)
        servicesList = servicesResult.stdout
        usersList = usersResult.stdout  # type: dict

        for service in servicesList:
            serviceStatus = getServiceStatus(ServiceName=service)
            self.assertEqual(serviceStatus.retcode, 0, serviceStatus.stderr)
            if serviceStatus.stdout:
                for user in usersList:
                    res = listUserPrivileges(ServiceName=service,
                                             ExistingUserName=user.get("userName"),
                                             ExistingUserSecurityDomain=user.get("securityDomain"))
                    rootLogger.info(res)
                    self.assertEqual(res.retcode, 0, res.stderr)
                    print()
                    pprint(res.stdout)

    def test_listGroupsForUser(self):
        usersResult = listAllUsers()
        self.assertEqual(usersResult.retcode, 0, usersResult.stderr)
        users = usersResult.stdout
        for user in users:  # type: dict
            groupsForUser = listGroupsForUser(ExistingUserName=user.get("userName"),
                                              ExistingUserSecurityDomain=user.get("securityDomain"))

            rootLogger.info(groupsForUser)

    def test_purgeLog(self):
        BeforeDate = "2017/03/08"
        try:
            res = purgeLog(BeforeDate=BeforeDate)
            rootLogger.info(res)
        except Exception as e:
            rootLogger.exception(str(e))
            BeforeDate = "2017-03-08"
            res = purgeLog(BeforeDate=BeforeDate)
            rootLogger.info(res)
            self.assertEqual(res.retcode, 0, res.stderr)

            BeforeDate = "04/08/2018"
            res = purgeLog(BeforeDate=BeforeDate)
            rootLogger.info(res)
            self.assertEqual(res.retcode, 0, res.stderr)

    def test_resetPassword(self):
        username = "readonly"
        password = "infa"
        res = resetPassword(ResetUserName=username, ResetUserPassword=password)
        self.assertEqual(res.retcode, 0, res.stderr)

        username = "readonly_notexisting"
        res = resetPassword(ResetUserName=username, ResetUserPassword=password)
        self.assertNotEqual(res.retcode, 0, res.stderr)
        rootLogger.info(res)
