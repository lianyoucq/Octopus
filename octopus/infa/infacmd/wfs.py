# -*- coding:utf-8 -*-
"""
abortWorkflow
bulkComplete
cancelWorkflow
completeTask
createTables
delegateTask
dropTables
listActiveWorkflowInstances
listMappingPersistedOutputs
listTasks
listWorkflowParams
listWorkflows
recoverWorkflow
releaseTask
setMappingPersistedOutputs
startTask
startWorkflow
upgradeWorkflowParameterFile
"""
import re
import os
from collections import namedtuple
from octopus.infa import _checking_infacmd_env_and_ret_base_cmd, _assemble_command_options, strip_ignored_cmd_messages
from octopus.common.logger import mainLogger
from octopus.common import run_cmd

base_cmd = "wfs"


def startWorkflow(DomainName: str,
                  ServiceName: str,
                  Application: str,
                  Workflow: str,
                  Wait: bool = False,
                  ParameterFile: str = None,
                  ParameterSet: str = None,
                  UserName: str = None,
                  Password: str = None,
                  SecurityDomain: str = "Native",
                  ResilienceTimeout: int = None,
                  OsProfile: str = None) -> namedtuple("CmdResult", ['retcode', "stdout", "stderr"]):
    options = ["DomainName", "ServiceName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout",
               "Application", "Workflow", "Wait", "ParameterFile", "ParameterSet", "OsProfile"]

    subcmd = "startWorkflow"
    cmd = _checking_infacmd_env_and_ret_base_cmd(DomainName, UserName, Password, base_cmd, subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    stdout = res.stdout
    stderr = res.stderr
    ret = namedtuple("CommandResult", ['retcode', "stdout", "stderr"])
    return ret(res.retcode, stdout, stderr)


def listWorkflows(DomainName: str,
                  ServiceName: str,
                  Application: str,
                  UserName: str = None,
                  Password: str = None,
                  SecurityDomain: str = "Native",
                  ResilienceTimeout: int = None
                  ) -> namedtuple("CmdResult", ['retcode', "stdout", "stderr"]):
    subcmd = "listWorkflows"
    options = ["DomainName", "ServiceName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout",
               "Application"]
    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName,
                                                 password=Password, cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        stdout_formated = stdout.split("\n")
        stdout = stdout_formated[:-1]

    ret = namedtuple("CmdResult", ['retcode', "stdout", "stderr"])
    return ret(res.retcode, stdout, stderr)


def listTasks(DomainName: str,
              ServiceName: str,
              UserName: str = None,
              Password: str = None,
              MaxTasks: int = None,
              FilterByOwner: str = None,
              FilterByStatus: str = None,
              FilterByCreationDate: str = None,
              FilterByType: str = None,
              FilterByDueDate: str = None,
              FilterByID: str = None,
              FilterByName: str = None,
              FilterByNameLike: str = None,
              TasksOffset: str = None,
              Role: str = "ALL",
              SecurityDomain: str = None,
              ResilienceTimeout: str = None,
              ) -> namedtuple("CmdResult", ['retcode', "stdout", "stderr"]):
    options = ["DomainName", "ServiceName", "UserName", "Password", "MaxTasks", "FilterByOwner", "FilterByStatus",
               "FilterByCreationDate", "FilterByType", "FilterByDueDate", "FilterByID", "FilterByName",
               "FilterByNameLike", "TasksOffset", "Role", "SecurityDomain", "ResilienceTimeout"]
    subcmd = "listTasks"
    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName,
                                                 password=Password, cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    stdout = res.stdout
    stderr = res.stderr
    if res.retcode == 0:
        stdout_formated = stdout.split("\n")
        stdout = stdout_formated[:-1]

    ret = namedtuple("CmdResult", ['retcode', "stdout", "stderr"])
    return ret(res.retcode, stdout, stderr)


def listActiveWorkflowInstances(DomainName: str,
                                ServiceName: str,
                                UserName: str = None,
                                Password: str = None,
                                SecurityDomain: str = "Native",
                                ResilienceTimeout: int = None
                                ) -> namedtuple("ListActiveWorkflowInstancesResult",
                                                ['retcode', "stdout", "stderr"]):
    """

    :param DomainName:
    :param ServiceName:
    :param UserName:
    :param Password:
    :param SecurityDomain: default is Native
    :param ResilienceTimeout:
    :return: namedtuple("CmdResult",['retcode', "stdout", "stderr"])
    if stdout is existing, then it will return namedtuple('activeWorkflowInst', ['Workflow_Instance_State',
    'Workflow_Instance_ID', 'Workflow_Name', 'Application_Name']
    """
    envs = os.environ
    options = ["DomainName", "ServiceName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout"]
    subcmd = "listActiveWorkflowInstances"
    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName,
                                                 password=Password, cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=envs)
    stdout = res.stdout  # type: str
    stderr = res.stderr  # type: str
    if res.retcode == 0:
        if stdout.startswith("Cannot find an active workflow instance"):
            stderr += stdout
            stdout = None
        else:
            stdout_formated = stdout.split("\n")
            # as the output has \n\n
            head = stdout_formated[1:2][0]  # type: str
            head = head.rstrip().replace(" ", "_")
            head = re.split("_{2,}", head)
            item_namedtuple = namedtuple("activeWorkflowInst", head)
            mainLogger.debug(head)
            stdout_formated = stdout_formated[2:-2]
            """
             ['Workflow instances that are running or that are canceled and enabled for recovery:', 
             'Workflow Instance State     Workflow Instance ID        Workflow Name                                       Application Name     ', 
             'Running                     Ub_rShwwEei_oNrsW-zrpQ      wf_cuttlefish_single_triple_20180116                app_wf_cuttlefish_single2triple_test     ']
            """
            stdout = list()  # type: list
            for item in stdout_formated:
                stdout.append(item_namedtuple(*tuple(re.split(r" *", item.rstrip()))))
    else:
        stderr += stdout

    ret = namedtuple("ListActiveWorkflowInstancesResult", ['retcode', "stdout", "stderr"])
    return ret(res.retcode, stdout, stderr)


def listWorkflowParams(
        ServiceName: str,
        Application: str,
        Workflow: str,
        DomainName: str = None,
        OutputFile: str = None,
        UserName: str = None,
        Password: str = None,
        SecurityDomain: str = "Native",
        ResilienceTimeout: int = None,
) -> namedtuple("listWorkflowParamsResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "listWorkflowParams"
    options = ["DomainName", "ServiceName", "UserName", "Password", "SecurityDomain", "ResilienceTimeout",
               "Application", "Workflow", "OutputFile", ]

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
    listWorkflowParamsResult = namedtuple("listWorkflowParamsResult", ['retcode', 'stdout', 'stderr'])
    return listWorkflowParamsResult(res.retcode, stdout, stderr)
