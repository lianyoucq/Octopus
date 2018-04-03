# -*- coding:utf-8 -*-
import os
from collections import namedtuple
from octopus.common.logger import mainLogger
from octopus.common import run_cmd
from octopus.infa import  _checking_infacmd_env_and_ret_base_cmd, _assemble_command_options

base_cmd = "oie"


def deployApplication(
        RepositoryService: str,
        OutputDirectory: str,
        ApplicationPath: str,
        DomainName: str = None,
        UserName: str = None,
        Password: str = None,
) -> namedtuple("DeployApplicationResult", ['retcode', 'stdout', 'stderr']):
    """ deploy the application to .iar file

    if retcode equals 0, then the stdout returns the .iar file

    otherwise, the stderr returns the error message.

    :param RepositoryService: Model Repository Service
    :param OutputDirectory:
    :param ApplicationPath: "Project/Folder/application"
    :param DomainName:
    :param UserName:
    :param Password:
    :return: namedtuple("DeployApplicationResult", ['retcode', 'stdout', 'stderr'])
    """
    subcmd = "DeployApplication"
    options = ["DomainName", "UserName", "Password", "RepositoryService", "OutputDirectory", "ApplicationPath", ]

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
        stdout = stdout[stdout.index("File [")+6:stdout.index("] has been generate")]
    else:
        stderr += stdout
    deployApplicationResult = namedtuple("DeployApplicationResult", ['retcode', 'stdout', 'stderr'])
    return deployApplicationResult(res.retcode, stdout, stderr)
