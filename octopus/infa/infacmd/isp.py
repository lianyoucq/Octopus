# -*- coding:utf-8 -*-
import os
import re
from collections import namedtuple
from datetime import datetime

from octopus.common import run_cmd
from octopus.common.logger import mainLogger
from octopus.infa import _checking_infacmd_env_and_ret_base_cmd, _assemble_command_options, strip_ignored_cmd_messages
from octopus.infa.utils import pmpasswd

base_cmd = "isp"


def listServiceLevels(
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("ListServiceLevelsResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "ListServiceLevels"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        serviceLevels = stdout.split("\n\n")
        listServiceLevels_list = list()
        for serviceLevel in serviceLevels:
            stdout = serviceLevel.split("\n")
            listServiceLevels_dict = dict()
            for item in stdout:  # type: str
                a = re.split("[:=]", item, maxsplit=1)
                listServiceLevels_dict.setdefault(a[0].lstrip().rstrip(), a[1].lstrip().rstrip().rstrip(":"))
            listServiceLevels_list.append(listServiceLevels_dict)
        stdout = listServiceLevels_list
    else:
        stderr += stdout

    listServiceLevelsResult = namedtuple("ListServiceLevelsResult", ['retcode', 'stdout', 'stderr'])
    return listServiceLevelsResult(res.retcode, stdout, stderr)


def listServices(
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
        ServiceType: str = None,
) -> namedtuple("ListServicesResult", ['retcode', 'stdout', 'stderr']):
    """ list all services or services of specified Service Type

    retcode: 0 stands for success, otherwise failure

    stdout: list(str) like [service_name1, service_name2, .....] if retcode equals 0

    stderr: str

    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param Gateway:
    :param ResilienceTimeout:
    :param ServiceType: refer to the octopus.infa.infacmd.servicetype_namedtupe
    :return: namedtuple("ListServicesResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "ListServices"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "ServiceType", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout  # type:  str
    stderr = res.stderr
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        stdout = stdout.split("\n")
    else:
        stderr += stdout

    listServicesResult = namedtuple("ListServicesResult", ['retcode', 'stdout', 'stderr'])
    return listServicesResult(res.retcode, stdout, stderr)


def listServiceNodes(
        ServiceName: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None
) -> namedtuple("ListServiceNodesResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "ListServiceNodes"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "ServiceName", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        stdout = stdout.split("\n")
    else:
        stderr += stdout

    listServiceNodesResult = namedtuple("ListServiceNodesResult", ['retcode', 'stdout', 'stderr'])
    return listServiceNodesResult(res.retcode, stdout, stderr)


def listServicePrivileges(DomainName: str = None,
                          UserName: str = None,
                          Password: str = None,
                          SecurityDomain: str = "Native",
                          Gateway: str = None,
                          ResilienceTimeout: int = None,
                          ServiceType: str = None,
                          ) -> namedtuple("ListServicePrivilegesResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "ListServicePrivileges "
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "ServiceType", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    stdout = res.stdout
    stderr = res.stderr
    mainLogger.info(res)
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        stdout = stdout.split("\n")
    else:
        stderr += stdout

    listServicePrivilegesResult = namedtuple("ListServicePrivilegesResult", ['retcode', 'stdout', 'stderr'])
    return listServicePrivilegesResult(res.retcode, stdout, res.stderr)


def getServiceStatus(
        ServiceName: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None
) -> namedtuple("GetServiceStatusResult", ['retcode', 'stdout', 'stderr']):
    """Get the service's Status

    True stands for it's enabled

    False stands for it's disabled

    :param ServiceName:
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param Gateway:
    :param ResilienceTimeout:
    :return:
    """
    subcmd = "GetServiceStatus"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "ServiceName", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        stdout = True if stdout.upper().startswith("ENABLED") else False
    else:
        stderr += stdout

    getServiceStatusResult = namedtuple("GetServiceStatusResult", ['retcode', 'stdout', 'stderr'])
    return getServiceStatusResult(res.retcode, stdout, stderr)


def listLicenses(
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("ListLicensesResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "ListLicenses"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        mainLogger.info(stdout)
        licenses = stdout.split("\n")
        stdout = list()
        for license in licenses:
            name_sid = license.split(" ")
            licenseResult = namedtuple("LicenseResult", ["Name", "SerialNumber"])
            stdout.append(licenseResult(name_sid[0], name_sid[1].lstrip("(").rstrip(")")))
    else:
        stderr += stdout

    listLicensesResult = namedtuple("ListLicensesResult", ['retcode', 'stdout', 'stderr'])
    return listLicensesResult(res.retcode, stdout, stderr)


def showLicense(
        LicenseName: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("ShowLicenseResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "ShowLicense"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "LicenseName", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout  # type: str
    stderr = res.stderr
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
    else:
        stderr += stdout

    showLicenseResult = namedtuple("ShowLicenseResult", ['retcode', 'stdout', 'stderr'])
    return showLicenseResult(res.retcode, stdout, stderr)


def ping(
        ServiceName: str,
        NodeName: str = None,
        DomainName: str = None,
        GatewayAddress: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("PingResult", ['retcode', 'stdout', 'stderr']):
    """

    :param ServiceName:
    :param NodeName:
    :param DomainName:
    :param GatewayAddress:
    :param ResilienceTimeout:
    :return:
    """
    subcmd = "Ping"
    options = ["DomainName", "ServiceName", "GatewayAddress", "NodeName", "ResilienceTimeout", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=None, password=None, cmd=base_cmd,
                                                 subcmd=subcmd, verify_username_password=False)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
    else:
        stderr += stdout

    pingResult = namedtuple("PingResult", ['retcode', 'stdout', 'stderr'])
    return pingResult(res.retcode, stdout, stderr)


def enableServiceProcess(
        ServiceName: str,
        NodeName: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("EnableServiceProcessResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "EnableServiceProcess"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "ServiceName",
               "NodeName", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    return res


def disableServiceProcess(
        ServiceName: str,
        NodeName: str,
        Mode: str = "Complete",
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None
) -> namedtuple("DisableServiceProcessResult", ['retcode', 'stdout', 'stderr']):
    """
    Disable the Service process on a specified node


    :param ServiceName:
    :param NodeName:
    :param Mode: default is Complete, (Complete|Abort|Stop)
    :param DomainName: optional
    :param UserName: optional
    :param Password: optional
    :param SecurityDomain: default is Native
    :param Gateway: optional
    :param ResilienceTimeout: optional
    :return: namedtuple("DisableServiceProcessResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "DisableServiceProcess"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "ServiceName",
               "NodeName", "Mode", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout  # type: str
    stderr = res.stderr  # type: str
    if res.retcode == 0:
        pass
    else:
        stderr += stdout
    disableServiceProcessResult = namedtuple("DisableServiceProcessResult", ['retcode', 'stdout', 'stderr'])
    return disableServiceProcessResult(res.retcode, stdout, stderr)


def enableService(
        ServiceName: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None
) -> namedtuple("EnableServiceResult", ['retcode', 'stdout', 'stderr']):
    """ enable the service

    if retcode is 0, then it enables the service, otherwise, it will raise stderr.

    :param ServiceName:
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param Gateway:
    :param ResilienceTimeout:
    :return:
    """
    subcmd = "EnableService"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "ServiceName", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)

    stderr = res.stderr
    stdout = res.stdout
    if res.retcode != 0:
        stderr += stdout

    mainLogger.info(res)
    enableServiceResult = namedtuple("EnableServiceResult", ['retcode', 'stdout', 'stderr'])
    return enableServiceResult(res.retcode, stdout, stderr)


def listAllUsers(
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("ListAllUsersResult", ['retcode', 'stdout', 'stderr']):
    """
    list all users

    if retcode is 0, then stdout returns a list of users' dict,
    like [{securityDomain: securityDomainName_1, userName: userName_1}, ....]
    for example: [{'securityDomain': 'Native', 'userName': 'admin'}]

    else: return the stderr

    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param Gateway:
    :param ResilienceTimeout:
    :return: namedtuple("ListAllUsersResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "ListAllUsers "
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        usersList = stdout.split("\n")
        stdout = list()
        for user in usersList:
            userinfo = user.split("/")
            user_dict = dict()
            user_dict.setdefault("securityDomain", userinfo[0])
            user_dict.setdefault("userName", userinfo[1])
            stdout.append(user_dict)
    else:
        stderr += stdout

    listAllUsersResult = namedtuple("ListAllUsersResult", ['retcode', 'stdout', 'stderr'])
    return listAllUsersResult(res.retcode, stdout, stderr)


def listConnections(
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        ConnectionType: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None,
) -> namedtuple("ListConnectionsResult", ['retcode', 'stdout', 'stderr']):
    """ list all connections (Administrator Console)
    if retcode requals 0, then stdout returns a dict which contains Connection_Type and its list of connection(id: name)
    like, {CONN_TYPE_1: [{id: CONN_1_ID, name: CONN_1_NAME}, {id: CONN_2_ID, name: CONN_2_NAME}, ....], CONN_TYPE_2: [], .....}

    :param DomainName:
    :param UserName:
    :param Password:
    :param ConnectionType: refer to the octopus.infa.infacmd.connectiontype_namedtupe
    :param SecurityDomain:
    :param ResilienceTimeout:
    :return: namedtuple("ListConnectionsResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "ListConnections  "
    options = ["DomainName", "UserName", "Password", "ConnectionType", "SecurityDomain", "ResilienceTimeout", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)

    stdout = res.stdout  # type: str
    stderr = res.stderr

    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        stdout = stdout.split("\n")  # type: list
        stdout.reverse()
        conns_dict = dict()
        conns_list = list()
        for conn_val in stdout:
            if not conn_val.startswith("\t"):
                if len(conns_list) > 0:
                    conns_dict.setdefault(conn_val, conns_list)
                conns_list = list()
            else:
                # '\tINFA_102_DIS_PWD_210 - [ID: INFA_102_DIS_PWD_210
                conn_val = conn_val.lstrip("\t").rstrip("]").split(" - [ID: ")
                conns_list.append({"id": conn_val[1], "name": conn_val[0]})
                continue

        stdout = conns_dict
    else:
        stderr += stdout

    listConnectionsResult = namedtuple("ListConnectionsResult", ['retcode', 'stdout', 'stderr'])
    return listConnectionsResult(res.retcode, stdout, stderr)


def listConnectionOptions(
        ConnectionName: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None,

) -> namedtuple("ListConnectionOptionsResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "ListConnectionOptions"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout", "ConnectionName", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)

    stdout = res.stdout  # type: str
    stderr = res.stderr
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        conn_options = stdout.split("\n")  # type: list
        stdout = dict()
        for option in conn_options:  # type: str
            option_name_value = option.split(":", maxsplit=1)
            option_name = option_name_value[0]
            option_value = option_name_value[1].lstrip().rstrip()
            if option_value.startswith("[") and option_value.endswith("]"):
                option_value = option_value[1:-1]
            stdout.setdefault(option_name, option_value)
    else:
        stderr += stdout
    listConnectionOptionsResult = namedtuple("ListConnectionOptionsResult", ['retcode', 'stdout', 'stderr'])

    return listConnectionOptionsResult(res.retcode, stdout, stderr)


def disableService(
        ServiceName: str,
        Mode: str = "Complete",
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("DisableServiceResult", ['retcode', 'stdout', 'stderr']):
    """ disable the Service

    if retcode is 0, then it's disabled successfully, otherwise it will raise stderr

    :param ServiceName:
    :param Mode: (Complete|Abort|Stop) default is Complete
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param Gateway:
    :param ResilienceTimeout:
    :return:
    """
    subcmd = "DisableService"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "ServiceName",
               "Mode", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    return res


def listNodeResources(
        NodeName: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
        ResourceCategory: str = "PCIS",
) -> namedtuple("ListNodeResourcesResult", ['retcode', 'stdout', 'stderr']):
    """ list the resources of the node
    if

    :param NodeName:
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param Gateway:
    :param ResilienceTimeout:
    :param ResourceCategory:
    :return:
    """
    subcmd = "ListNodeResources"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "NodeName",
               "ResourceCategory", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        entrys = stdout.splitlines()
        stdout = list()
        for entry in entrys:  # type: str
            entry_dict = dict()
            entry_list = entry.split(";")
            name = entry_list[0]
            name = name[name.index("[") + 1:-1]
            entry_dict.setdefault("name", name)
            type = entry_list[1]
            type = type[type.index("[") + 1:-1]
            entry_dict.setdefault("type", type)
            available = entry_list[2]
            available = available[available.index("[") + 1:-2]
            entry_dict.setdefault("available", True if available.upper() == "TRUE" else False)
            stdout.append(entry_dict)
    else:
        stderr += stdout
    listNodeResourcesResult = namedtuple("ListNodeResourcesResult", ['retcode', 'stdout', 'stderr'])
    return listNodeResourcesResult(res.retcode, stdout, stderr)


def listNodes(
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
        NodeRole: str = "Service_compute",
) -> namedtuple("ListNodesResult", ['retcode', 'stdout', 'stderr']):
    """ list nodes of specified NodeRole
    retcode is int, 0 represents success, otherwise failure
    if retcode requals 0, the stdout will a list of nodes, and it must have one node, like [node1, node2].
    otherwise, the stderr will show the details of error

    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param Gateway:
    :param ResilienceTimeout:
    :param NodeRole: (Service_compute|Service|Compute) default is Service_compute
    :return: namedtuple("ListNodesResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "ListNodes "
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "NodeRole", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        stdout = stdout.splitlines()
    else:
        stderr += stdout

    listNodesResult = namedtuple("ListNodesResult", ['retcode', 'stdout', 'stderr'])
    return listNodesResult(res.retcode, stdout, stderr)


def listUserPermissions(
        ExistingUserName: str,
        ExistingUserSecurityDomain: str = "Native",
        ObjectType: str = None,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("ListUserPermissionsResult", ['retcode', 'stdout', 'stderr']):
    """ list user's permissions on these Object types

        if retcode equals 0, then stdout returns a dict with Object Types and its list of values. dict(list)

        otherwise, stderr will show the error messages.

        here is a sample of success:
         {
            'Folder': ['/System_Services',
                        '/'],
            'Grid': ['INFA210_GRID'],
            'License': ['dd',
                        'EndApr1'],
            'Node': ['ND_NoExisting',
                     'ND_INFA210'],
            'OS Profile': ['BDM_OS_Profile'],
            'Service': [
                 'Scheduler_Service',
                 'Email_Service',
                 'Resource_Manager_Service',
                 'IS_ASCII',
                 'D102_INFA210',
                 'M102_INFA210',
                 'R102_PRD_INFA210',
                 'IS_UNICODE',
                 'R102_INFA210']
        }

    :param ExistingUserName:
    :param ExistingUserSecurityDomain:
    :param ObjectType: (Service|License|Node|Grid|Folder|OSProfile) default is None which represents all
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param Gateway:
    :param ResilienceTimeout:
    :return:
    """
    subcmd = "ListUserPermissions"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout",
               "ExistingUserName", "ExistingUserSecurityDomain", "ObjectType", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout  # type: str
    stderr = res.stderr  # type: str
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        userPermissionsList = stdout.splitlines()
        userPermissionsList.reverse()
        stdout = dict()
        everyPermissionList = list()
        for entry in userPermissionsList:  # type: str
            if not entry.endswith(":"):
                entry = entry.strip(" ")
                if entry:
                    everyPermissionList.append(entry)
                continue
            else:
                stdout.setdefault(entry.rstrip(":").rstrip(" "), everyPermissionList)
                everyPermissionList = list()
    else:
        stderr += stdout

    listUserPermissionsResult = namedtuple("ListUserPermissionsResult", ['retcode', 'stdout', 'stderr'])
    return listUserPermissionsResult(res.retcode, stdout, stderr)


def listUserPrivileges(
        ServiceName: str,
        ExistingUserName: str,
        ExistingUserSecurityDomain: str = "Native",
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("ListUserPrivilegesResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "ListUserPrivileges"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout",
               "ExistingUserName", "ExistingUserSecurityDomain", "ServiceName", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout  # type: str
    stderr = res.stderr  # type: str
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        stdout = stdout.splitlines()
    else:
        stderr += stdout
    listUserPrivilegesResult = namedtuple("ListUserPrivilegesResult", ['retcode', 'stdout', 'stderr'])
    return listUserPrivilegesResult(res.retcode, stdout, stderr)


def listGroupsForUser(
        ExistingUserName: str,
        ExistingUserSecurityDomain: str = "Native",
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("ListGroupsForUserResult", ['retcode', 'stdout', 'stderr']):
    """ list group for the user
    if retcode equals 0, then stdout returns a list of dict which contains securityDomain and groupName
    else: stderr will show error messages

    for instance:
    [{'securityDomain': 'Native', 'groupName': 'Administrator'}, {'securityDomain': 'Native', 'groupName': 'Everyone'}]

    :param ExistingUserName:
    :param ExistingUserSecurityDomain:
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param Gateway:
    :param ResilienceTimeout:
    :return: namedtuple("ListGroupsForUserResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "ListGroupsForUser"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout",
               "ExistingUserName", "ExistingUserSecurityDomain", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout  # type: str
    stderr = res.stderr  # type: str
    if res.retcode == 0:
        stdout = strip_ignored_cmd_messages(stdout)
        groups_list = stdout.splitlines()
        stdout = list()
        for group in groups_list:
            temp_dict = dict()
            group_info = group.split("/")
            temp_dict.setdefault("securityDomain", group_info[0])
            temp_dict.setdefault("groupName", group_info[1])
            stdout.append(temp_dict)
    else:
        stderr += stdout
    listGroupsForUserResult = namedtuple("ListGroupsForUserResult", ['retcode', 'stdout', 'stderr'])
    return listGroupsForUserResult(res.retcode, stdout, stderr)


def purgeLog(
        BeforeDate: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("PurgeLogResult", ['retcode', 'stdout', 'stderr']):
    """
    purge log events for a domain or for application services, such as the PowerCenter Integration Service,
    the Data Integration Service, and the Web Services Hub.

    :param BeforeDate: (MM/dd/yyyy|yyyy-MM-dd)
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param Gateway:
    :param ResilienceTimeout:
    :return: namedtuple("PurgeLogResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "PurgeLog"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "BeforeDate", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    try:
        datetime.strptime(BeforeDate, "%Y-%m-%d")
    except Exception as e:
        mainLogger.exception(str(e))
        try:
            datetime.strptime(BeforeDate, "%m/%d/%Y")
        except Exception as e:
            mainLogger.exception(str(e))
            raise Exception("The format of the BeforeDate is not right, should be yyyy/MM/dd or MM/dd/yyyy")

    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout  # type: str
    stderr = res.stderr  # type: str
    if res.retcode == 0:
        pass
    else:
        stderr += stdout
    purgeLogResult = namedtuple("PurgeLogResult", ['retcode', 'stdout', 'stderr'])
    return purgeLogResult(res.retcode, stdout, stderr)


def resetPassword(
        ResetUserName: str,
        ResetUserPassword: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        Gateway: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("ResetPasswordResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "ResetPassword"

    options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "ResetUserName"]
    # for security reason, the ResetUserPassword will be set by the INFA_PASSWORD environment
    # options = ["DomainName", "UserName", "Password", "SecurityDomain", "Gateway", "ResilienceTimeout", "ResetUserName",
    #            "ResetUserPassword", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    encrypted_password_Result = pmpasswd(passwd=ResetUserPassword)
    resetPasswordResult = namedtuple("ResetPasswordResult", ['retcode', 'stdout', 'stderr'])
    if encrypted_password_Result.retcode == 0:
        os.environ.setdefault("INFA_PASSWORD", encrypted_password_Result.stdout)
    else:
        return resetPasswordResult(encrypted_password_Result.retcode, "",
                                   "Couldn't to generate the encrypted password. for {0}".format(
                                       encrypted_password_Result.stdout))
    mainLogger.debug(os.environ)
    res = run_cmd(cmd, env=os.environ)
    os.environ.pop("INFA_PASSWORD")
    mainLogger.info(res)
    stdout = res.stdout  # type: str
    stderr = res.stderr  # type: str
    if res.retcode != 0:
        stderr += stdout

    return resetPasswordResult(res.retcode, stdout, stderr)
