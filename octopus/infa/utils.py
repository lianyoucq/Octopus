# -*- coding:utf-8 -*-
from collections import namedtuple
import os
from config import Config
from octopus.exceptions import UnsupportedEncryptionType, MissingEnvironmentVariable
from octopus.common import run_cmd, get_LIBRARY_PATH_NAME, is_none
from octopus.common.logger import mainLogger


def pmpasswd(passwd: str, encrypt_type: str=None) -> namedtuple("pmpasswdResult", ['retcode', 'stdout']):
    """
    You can encrypt passwords to create an environment variable to use with infacmd, 
    infasetup, pmcmd, and pmrep or to define a password in a parameter file. 
    For example, you can encrypt the repository and database passwords for pmrep to maintain
    security when using pmrep in scripts. Then you can create an environment variable to store the 
    encrypted password. Or, you can define a password for a relational database connection object in 
    a parameter file.

    :param passwd: to be encrypted password
    :param encrypt_type: CRYPT_DATA | CRYPT_SYSTEM
    :return: encrypted password
    """
    infa_home_key = Config.PREDEFINED_ENV_VARIABLES_ATTRIBUTE.INFA_HOME
    infa_home = os.environ.get(infa_home_key)
    if is_none(infa_home):
        raise MissingEnvironmentVariable("the {0} is not set".format(infa_home_key))

    ld_lib_path_name = get_LIBRARY_PATH_NAME()
    if ld_lib_path_name:
        existing_ld_lib_path_value = os.environ.get(ld_lib_path_name)
        infa_ld_lib_path = "{0}/server/bin:{1}/services/shared/bin".format(infa_home, infa_home)
        os.environ.update({ld_lib_path_name: "{0}:{1}".format(infa_ld_lib_path, existing_ld_lib_path_value)})

    if is_none(encrypt_type):
        command = "{infa_home}/server/bin/pmpasswd {passwd} ".format(infa_home=infa_home, passwd=passwd)
    elif encrypt_type is not None and encrypt_type.upper() in ('CRYPT_DATA', 'CRYPT_SYSTEM'):
        command = "{infa_home}/server/bin/pmpasswd {passwd} -e {encrypt_type}".format(infa_home=infa_home,
                                                                                     passwd=passwd,
                                                                                     encrypt_type=encrypt_type.upper())
    else:
        errmsg = "{0} is not supported in pmpasswd command".format(encrypt_type)
        mainLogger.error(errmsg)
        raise UnsupportedEncryptionType(errmsg)

    mainLogger.debug(os.environ)
    mainLogger.info(command)

    cmd_result = run_cmd(command, env=os.environ)
    mainLogger.debug(cmd_result)

    stdout = cmd_result.stdout # type: str
    stderr = cmd_result.stderr # type: str
    msg = None
    if cmd_result.retcode == 0:
        msg = stdout[stdout.index("-->") + 3 : stdout.index("<--")]
    else:
        msg = stderr + " " + stdout[stdout.index("usage:"): ]

    pmpasswdResult = namedtuple("pmpasswdResult", ['retcode', 'stdout'])

    return pmpasswdResult(cmd_result.retcode, msg)

