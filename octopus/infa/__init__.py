# -*- coding:utf-8 -*-
import os
import re
from config import Config
from octopus.exceptions import MissingEnvironmentVariable
from octopus.common import shell_suffix, is_none

ignored_cmd_messages = ["\n*Command ran successfully.\n*",
                        "User \[.*\] of security domain \[.*\] has permission on the following domain objects:\n*"]


def strip_ignored_cmd_messages(messages) -> str:
    for ignored_cmd_message in ignored_cmd_messages:
        messages = re.sub(ignored_cmd_message, "", messages)

    return messages


def _assemble_command_options(commands: str, option_name, option_value) -> str:
    if option_value is not None:
        if type(option_value) == bool:
            if option_value:
                commands = "{0} -{1}".format(commands, option_name)
        else:
            commands = "{0} -{1} \'{2}\'".format(commands, option_name, option_value)
    return commands


def _checking_infacmd_env_and_ret_base_cmd(domainname, username, password, cmd, subcmd, verify_username_password=True):
    infa_home_key = Config.PREDEFINED_ENV_VARIABLES_ATTRIBUTE.INFA_HOME
    infa_default_domain_key = Config.PREDEFINED_ENV_VARIABLES_ATTRIBUTE.INFA_DEFAULT_DOMAIN
    infa_home = os.environ.get(infa_home_key)
    infa_default_domain = os.environ.get(infa_default_domain_key)

    if verify_username_password:
        infa_default_domain_password_key = Config.PREDEFINED_ENV_VARIABLES_ATTRIBUTE.INFA_DEFAULT_DOMAIN_PASSWORD
        infa_default_domain_user_key = Config.PREDEFINED_ENV_VARIABLES_ATTRIBUTE.INFA_DEFAULT_DOMAIN_USER
        infa_default_domain_password = os.environ.get(infa_default_domain_password_key)
        infa_default_domain_user = os.environ.get(infa_default_domain_user_key)

    exceptions = ""
    if is_none(infa_home):
        exceptions = infa_home_key
    if is_none(domainname) and is_none(infa_default_domain):
        exceptions += " INFA_DEFAULT_DOMAIN or domainName , "
    if verify_username_password and (is_none(username) or is_none(password)) and (
            is_none(infa_default_domain_user) or is_none(infa_default_domain_password)):
        exceptions += " INFA_DEFAULT_DOMAIN_USER/userName or INFA_DEFAULT_DOMAIN_PASSWORD/password"

    if not is_none(exceptions, treat_space_as_none=True):
        raise MissingEnvironmentVariable(exceptions + " is missing")

    return "{0}/server/bin/infacmd{1} {2} {3} ".format(infa_home, shell_suffix(), cmd, subcmd)
