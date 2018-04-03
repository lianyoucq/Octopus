# -*- coding:utf-8 -*-
import os
from collections import namedtuple

from octopus.common import run_cmd
from octopus.common.logger import mainLogger
from octopus.infa import _assemble_command_options, _checking_infacmd_env_and_ret_base_cmd, strip_ignored_cmd_messages

base_cmd = "mrs"


def backupContents(
        ServiceName: str,
        OutputFileName: str,
        DomainName: str = None,
        SecurityDomain: str = "Native",
        UserName: str = None,
        Password: str = None,
        OverwriteFile: False = None,
        Description: str = None,
        BackupSearchIndices: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("BackupContentsResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "BackupContents"
    options = ["DomainName", "SecurityDomain", "UserName", "Password", "ServiceName", "OutputFileName", "OverwriteFile",
               "Description", "BackupSearchIndices", "ResilienceTimeout", ]

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
    backupContentsResult = namedtuple("BackupContentsResult", ['retcode', 'stdout', 'stderr'])
    return backupContentsResult(res.retcode, stdout, stderr)


def listBackupFiles(
        ServiceName: str,
        DomainName: str = None,
        SecurityDomain: str = "Native",
        UserName: str = None,
        Password: str = None,
        ResilienceTimeout: int = None,
) -> namedtuple("ListBackupFilesResult", ['retcode', 'stdout', 'stderr']):
    subcmd = "ListBackupFiles"
    options = ["DomainName", "SecurityDomain", "UserName", "Password", "ServiceName", "ResilienceTimeout", ]

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
    listBackupFilesResult = namedtuple("ListBackupFilesResult", ['retcode', 'stdout', 'stderr'])

    return listBackupFilesResult(res.retcode, stdout, stderr)
