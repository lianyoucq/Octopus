# -*- coding:utf-8 -*-
import os
import re
from collections import namedtuple
from config import Config
from octopus.infa import _assemble_command_options, _checking_infacmd_env_and_ret_base_cmd, \
    strip_ignored_cmd_messages
from octopus.common.logger import mainLogger
from octopus.common import run_cmd, is_none

base_cmd = "ms"


def listMappings(
        ServiceName: str,
        Application: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None
) -> namedtuple("listMappingsResult", ["retcode", 'stdout', 'stderr']):
    """ list all mappings under the application

    if retcode equals 0, then stdout returns a list of mappings

    else: stderr will return the error message

    :param ServiceName: Data Integration Service
    :param Application:
    :param DomainName:
    :param UserName:
    :param Password:
    :param SecurityDomain:
    :param ResilienceTimeout:
    :return: namedtuple("listMappingsResult", ["retcode", 'stdout', 'stderr'])
    """
    subcmd = "ListMappings"
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
    if res.retcode == 0:
        # format the stdout
        stdout = strip_ignored_cmd_messages(stdout)
        stdout = stdout.split("\n")[:-1]
    else:
        stderr += stdout

    ret = namedtuple("ListMappingsResult", ["retcode", 'stdout', 'stderr'])
    return ret(res.retcode, stdout, stderr)


def runMapping(
        ServiceName: str,
        Application: str,
        Mapping: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None,
        Wait: bool = False,
        ParameterFile: str = None,
        ParameterSet: str = None,
        OperatingSystemProfile: str = None,
        NodeName: str = None,
        OptimizationLevel: str = None,
        PushdownType: str = None,
        CustomProperties: str = None,
) -> namedtuple("RunMappingResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "RunMapping"
    options = ["DomainName", "ServiceName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout",
               "Application",
               "Mapping", "Wait", "ParameterFile", "ParameterSet", "OperatingSystemProfile", "NodeName",
               "OptimizationLevel", "PushdownType", "CustomProperties", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    # stdout => [MSCMD_10023] Job with ID [rsSgcBxrEei_oNrsW-zrpQ] submitted to the Integration Service [D102_INFA210]
    runMappingResult = namedtuple("RunMappingResult", ['retcode', 'stdout', 'stderr'])
    stdout = res.stdout  # type: str
    stderr = res.stderr
    if res.retcode == 0:
        # format the stdout
        outNamed = namedtuple("runMappingResult", ["JobId", "ServiceName"])
        jobId = stdout[stdout.index("Job with ID [") + 13:stdout.index('] submitted to ')]
        serviceName = stdout[stdout.index("Integration Service [") + 21:stdout.index("].\nCommand ran successfully")]
        stdout = outNamed(jobId, serviceName)
    else:
        stderr += stdout

    mainLogger.info(stdout)
    return runMappingResult(res.retcode, stdout, stderr)


def getMappingStatus(
        ServiceName: str,
        JobId: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None,
) -> namedtuple("GetMappingStatusResult", ['retcode', 'stdout', 'stderr']):
    """

    for example:
    GetMappingStatusResult(retcode=0,
    stdout={'JobID': ' TA-1CRxxEei_oNrsW-zrpQ', 'StartTime': ' 02/28/2018 18','OnNode': ' ND_INFA210',
    'JobState': ' RUNNING',
    'LogFile': ' /opt/infa/pwc/1020/logs/ND_INFA210/services/DataIntegrationService/disLogs/ms/DEPLOYED_MAPPING_app_wf_
    cuttlefish_hive2hive_failure-m_cuttlefish_single_triple_20180116_20180228_182236_130.log'},
    stderr='')
    :param DomainName:
    :param ServiceName:
    :param JobId:
    :param UserName: optional
    :param Password: optional
    :param SecurityDomain: default is Native
    :param ResilienceTimeout: int
    :return: namedtuple("GetMappingStatusResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "GetMappingStatus"
    options = ["DomainName", "UserName", "Password", "SecurityDomain", "ServiceName", "JobId", "ResilienceTimeout", ]

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
        # format the stdout
        stdout = strip_ignored_cmd_messages(stdout)
        stdout = stdout.split("\n")

        format_stdout_dict = dict()
        for item in stdout:
            split_item = item.split(":")
            k = split_item[0].replace(" ", "")
            format_stdout_dict.setdefault(k, split_item[1])
        stdout = format_stdout_dict
    else:
        stderr += stdout

    getMappingStatusResult = namedtuple("GetMappingStatusResult", ['retcode', 'stdout', 'stderr'])
    return getMappingStatusResult(res.retcode, stdout, stderr)


def getRequestLog(
        ServiceName: str,
        RequestId: str,
        FileName: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None,
) -> namedtuple("GetRequestLogResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "GetRequestLog"
    options = ["DomainName", "ServiceName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout", "RequestId",
               "FileName", ]

    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password,
                                                 cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    return res


def listMappingParams(
        ServiceName: str,
        Application: str,
        Mapping: str,
        OutputFile: str = None,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None,
) -> namedtuple("ListMappingParamsResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "ListMappingParams"
    options = ["DomainName", "ServiceName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout",
               "Application", "Mapping", "OutputFile", ]

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
    else:
        stderr += stdout
    listMappingParamsResult = namedtuple("ListMappingParamsResult", ['retcode', 'stdout', 'stderr'])
    return listMappingParamsResult(res.retcode, stdout, stderr)
