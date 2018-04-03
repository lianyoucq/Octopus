# -*- coding:utf-8 -*-
"""
infasetup Command Reference

Using infasetup

BackupDomain

DefineDomain

DefineGatewayNode

DefineWorkerNode

DeleteDomain

GenerateEncryptionKey

Help

ListDomainCiphers

MigrateEncryptionKey

RestoreDomain

restoreMitKerberosLinkage

SwitchToKerberosMode

UpdateDomainCiphers

UpdateGatewayNode

UpdateKerberosAdminUser

UpdateKerberosConfig

updateMitKerberosLinkage

updateDomainSamlConfig

UpdateWorkerNode

UnlockUser

ValidateandRegisterFeature
"""

import os
from collections import namedtuple
from octopus.common import run_cmd, shell_suffix, is_none
from octopus.common.path_utils import get_backup_dir
from config import Config
from octopus.common.logger import mainLogger
from datetime import datetime
from octopus.exceptions import MissingEnvironmentVariable
from octopus.infa import _assemble_command_options


def backupDomain(domainname,
                 databasetype,
                 databaseaddress = None,
                 databaseconnectionstring = None,
                 databaseusername = None,
                 databaseservicename = None,
                 backupfile = None,
                 force = False,
                 tablespace = None,
                 schemaname = None,
                 databasetlsenabled = None,
                 databasetruststorepassword = None,
                 trustedconnection = False,
                 encryptionkeylocation = None,
                 databasetruststorelocation = None)\
        -> namedtuple("CommandResult", ['retcode', "stdout", "backupfile"]):
    """备份domain 元数据
    Backs up the configuration metadata for the domain. infasetup stores the backup domain metadata in a backup file
    with an extension of .mrep. You must shut down the domain before you run this command.
    When you run this command, infasetup backs up the domain configuration database tables to restore the domain to
    another database. You must back up the ISP_RUN_LOG table contents manually to get the previous workflow and session
    logs. If the command fails with a Java memory error, increase the system memory available for infasetup. To increase
     the system memory, set the -Xmx value in the INFA_JAVA_CMD_OPTS environment variable.
    :param domain_name:
    :param databaseaddress:
    :param databaseconnectionstring:
    :param databaseusername:
    :param databasetype:
    :param databaseservicename:
    :param backupfile:
    :param force:
    :param tablespace:
    :param schemaname:
    :param databasetlsenabled:
    :param databasetruststorepassword:
    :param trustedconnection:
    :param encryptionkeylocation:
    :param databasetruststorelocation:
    :param db_host:
    :param db_port:
    :param db_user:
    :param db_type:
    :param db_service_name:
    :param envs: 环境变量
    :param backup_path: 备份绝对路径或者绝对路径的备份文件
    :return: namedtuple("CommandResult", ['retcode', "stdout", "backupfile"])
    """
    mainLogger.info("invoking the backupdomain command")
    """ get environment parameters"""
    infa_default_database_password_key = Config.PREDEFINED_ENV_VARIABLES.get("INFA_DEFAULT_DATABASE_PASSWORD")
    infa_default_database_password = os.environ.get(infa_default_database_password_key)

    infa_home_key = Config.PREDEFINED_ENV_VARIABLES.get("INFA_HOME")
    infa_home = os.environ.get(infa_home_key)

    if is_none(infa_default_database_password) or is_none(infa_home):
        raise MissingEnvironmentVariable("the {0} or {1} is missing ".format(infa_home_key,
                                                                             infa_default_database_password_key))

    """Backup direcotry or filename"""
    filename = "{0}.{1}".format(datetime.strftime(datetime.now(), "%Y-%m-%d-%H-%M-%S-%s"), "mrep")

    if backupfile is None:
        backupfile = os.path.join(get_backup_dir(domain_name=domainname), filename)
    # if the backupfile is existing and directory, then it will use our defined backup directory
    elif backupfile is not None and os.path.isdir(backupfile):
        backupfile = os.path.join(get_backup_dir(backup_path=backupfile, domain_name=domainname), filename)
    elif backupfile is not None and os.path.isfile(backupfile):
        # backupfile = backupfile
        pass
    else:
        raise Exception("Backup directory you specified is not existing, please make sure it's existing and direcotry!")

    """assemble the backup commands"""
    commands = "{INFA_HOME}/isp/bin/infasetup{scipt_suffix} backupdomain ".format(INFA_HOME=infa_home,
                            scipt_suffix=shell_suffix())

    options = ["domainname", "databaseaddress", "databaseconnectionstring", "databaseusername", "databasetype",
               "databaseservicename", "backupfile", "force", "tablespace", "schemaname", "databasetlsenabled",
               "databasetruststorepassword", "trustedconnection", "encryptionkeylocation", "databasetruststorelocation"]
    options_value_dict = locals()
    for option in options:
        commands = _assemble_command_options(commands, option, options_value_dict.get(option))

    mainLogger.debug(os.environ)
    mainLogger.info(commands)
    """invoke the command"""
    cmd = run_cmd(commands, env=os.environ, live=False )

    """reformat the outputs and return the outputs"""
    msg = cmd.stdout
    # 0 stands for success, others stand for failure
    # if fails, the concatenates the stderr messages
    if cmd.retcode != 0:
        msg = "{0}; {1}".format(msg, cmd.stderr.decode())
    result = namedtuple("CommandResult", ['retcode', "stdout", "backupfile"])
    mainLogger.info(msg)
    return result(cmd.retcode, msg, backupfile)



