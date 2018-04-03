# -*- coding:utf-8 -*-
import os
from octopus.common import run_cmd, shell_suffix, is_none
from octopus.common.logger import mainLogger
from collections import namedtuple
from octopus.infa import _assemble_command_options, _checking_infacmd_env_and_ret_base_cmd

base_cmd = "dis"


def listApplications(
        servicename: str,
        domainname: str = None,
        username: str = None,
        password: str = None,
        securitydomain: str = "Native",
        resiliencetimeout: int = None) -> namedtuple("ListApplicationsResult",
                                                     ['retcode', "stdout",
                                                      "stderr"]):
    sub_cmd = "listapplications"
    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname, username, password, base_cmd, sub_cmd)
    options = ["domainname", "servicename", "username", "password", "securitydomain",
               "resiliencetimeout"]

    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)

    stdout = res.stdout  # type: str
    stderr = res.stderr  # type: str
    if res.retcode == 0 and not is_none(res.stdout):
        # format the stdout
        stdout_formated = stdout.split("\n")  # type: list
        stdout = stdout_formated[:-1]
    else:
        stderr += stdout

    ret = namedtuple("ListApplicationsResult", ['retcode', "stdout", "stderr"])
    return ret(res.retcode, stdout, stderr)


def listApplicationObjects(servicename: str,
                           application: str,
                           domainname: str = None,
                           domainaddress: str = None,
                           username: str = None,
                           password: str = None,
                           securitydomain: str = "Native",
                           resiliencetimeout: int = None,
                           objecttype: str = None,
                           listobjecttype: bool = False,
                           pagesize: int = None,
                           pageindex: int = None) -> namedtuple("ListApplicationObjectsResult",
                                                                ['retcode', "stdout", "stderr"]):
    """ list the objects under this application.

    if retcode equals 0, then stdout returns the a list of tuples which is formated with (objectName, type )

    for example;
    [('ConnectInfoProject/HADOOP_cuttlefish', '.GenericSDKConnectInfo'),
    ('ConnectInfoProject/HIVE_cuttlefish', 'Hiveconnectionmodel'),
    ('PRJ_DEV/FF_dual', 'FlatFileDataObject'),
    ('PRJ_DEV/dual', 'RelationalDataObject'),
    ('PRJ_DEV/dual1', 'RelationalDataObject'),
    ('PRJ_DEV/m_cuttlefish_single_triple_20180116', 'Mapping'),
    ('PRJ_DEV/m_ff2ff_parameter_20180309', 'Mapping'),
    ('PRJ_DEV/m_hive2hive_dual_20171019', 'Mapping'),
    ('PRJ_DEV/tgt_single1', 'RelationalDataObject'),
    ('PRJ_DEV/triple2', 'RelationalDataObject'),
    ('PRJ_DEV/wf_cuttlefish_hive2hive_failure', 'Workflow'),
    ('PRJ_DEV/wf_cuttlefish_single_triple_20180116', 'Workflow'),
    ('app_wf_cuttlefish_hive2hive_failure/app_wf_cuttlefish_hive2hive_failure', 'Application')

    :param servicename: dis
    :param application:
    :param domainname: domainname and domainaddress are alternative
    :param domainaddress: host:port
    :param username:
    :param password:
    :param securitydomain: Default is Native
    :param resiliencetimeout: INFA_CLIENT_RESILIENCE_TIMEOUT
    :param objecttype: (Hiveconnectionmodel|RelationalDataObject|Mapping|Workflow|Application|...)
    :param listobjecttype: true|false
    :param pagesize: pagesize and pageindex are together
    :param pageindex:
    :return: namedtuple("ListApplicationObjectsResult", ['retcode', "stdout", "stderr"])
    """
    subcmd = "listApplicationObjects"
    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname, username, password, base_cmd, subcmd)

    options = ["domainname", "domainaddress", "servicename", "username", "password", "securitydomain",
               "resiliencetimeout", "application", "objecttype", "listobjecttype", "pagesize", "pageindex"]
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)

    ret = namedtuple("ListApplicationObjectsResult", ['retcode', "stdout", "stderr"])
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        formated_stdout = stdout.split("\n")
        stdout = formated_stdout[:-1]
        if listobjecttype:
            stdout_temp = list()
            for item in stdout:
                item_formated = item.split("\t")
                stdout_temp.append(tuple(item_formated))
            stdout = stdout_temp
    else:
        stderr += stdout

    return ret(res.retcode, stdout, stderr)


def stopBlazeService(
        ServiceName: str,
        HadoopConnection: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None,
) -> namedtuple("stopBlazeServiceResult", ['retcode', 'stdout', 'stderr']):
    """ stop the Blaze Service

    if retcode equals 0, then it stops the Blaze Service successfully.

    otherwise, it fails to stop the Blaze Service.

    :param ServiceName: Data Integration Service
    :param HadoopConnection:  HADOOP [or using connectiontype_namedtupe.HADOOP]
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param ResilienceTimeout:
    :return: namedtuple("stopBlazeServiceResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "stopBlazeService"
    options = ["DomainName", "ServiceName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout",
               "HadoopConnection", ]

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
    stopBlazeServiceResult = namedtuple("stopBlazeServiceResult", ['retcode', 'stdout', 'stderr'])
    return stopBlazeServiceResult(res.retcode, stdout, stderr)


def backupApplication(
        ServiceName: str,
        Application: str,
        FileName: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None
) -> namedtuple("BackupApplicationResult", ['retcode', 'stdout', 'stderr']):
    """ backup Application

    it requires the application is stopped

    if retcode equals 0, then the stdout will show the backup FileName

    otherwise, the stderr will show the error message

    :param ServiceName: Data Integration Service
    :param Application:
    :param FileName:
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param ResilienceTimeout:
    :return: namedtuple("BackupApplicationResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "BackupApplication"
    options = ["DomainName", "ServiceName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout",
               "Application", "FileName", ]

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
        stdout = FileName
    else:
        stderr += stdout
    backupApplicationResult = namedtuple("BackupApplicationResult", ['retcode', 'stdout', 'stderr'])
    return backupApplicationResult(res.retcode, stdout, stderr)


def stopApplication(
        ServiceName: str,
        Application: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None
) -> namedtuple("StopApplicationResult", ['retcode', 'stdout', 'stderr']):
    """
    if retcode equals 0, then it stops the application successfully
    otherwise, it fails to stop it.

    :param ServiceName: Data Integration Service
    :param Application:
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param ResilienceTimeout:
    :return: namedtuple("StopApplicationResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "StopApplication"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout", "ServiceName",
               "Application", ]

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
    if res.retcode != 0:
        stderr += stdout
    stopApplicationResult = namedtuple("StopApplicationResult", ['retcode', 'stdout', 'stderr'])
    return stopApplicationResult(res.retcode, stdout, stderr)


def startApplication(
        ServiceName: str,
        Application: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None
) -> namedtuple("StartApplicationResult", ['retcode', 'stdout', 'stderr']):
    """
    if retcode equals 0, then it stops the application successfully
    otherwise, it fails to stop it.

    :param ServiceName: Data Integration Service
    :param Application:
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param ResilienceTimeout:
    :return: namedtuple("StartApplicationResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "StartApplication"
    options = ["DomainName", "ServiceName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout",
               "Application", ]

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
    if res.retcode != 0:
        stderr += stdout
    startApplicationResult = namedtuple("StartApplicationResult", ['retcode', 'stdout', 'stderr'])
    return startApplicationResult(res.retcode, stdout, stderr)
