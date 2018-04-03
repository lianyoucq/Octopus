# -*- coding:utf-8 -*-


"""
connect

-r <repository_name>

{-d <domain_name> |

 {-h <portal_host_name>

  -o <portal_port_number>}}

[{ <user_name>

[-s <user_security_domain>]

[-x <password> |

 -X <password_environment_variable>]} |

-u <connect_without_user_in_kerberos_mode>]

[-t <client_resilience>]
"""


def connect(repository_name, user_name, encrypted_passwd, security_domain="Native"):
    """

    :param repository_name:
    :param user_name:
    :param encrypted_passwd:
    :param security_domain:
    :return:
    """
    commands = """
    connect
    -r <repository_name>
    {-d <domain_name> |
     {-h <portal_host_name>
      -o <portal_port_number>}}
    [{ <user_name>
    [-s <user_security_domain>]
     -X <password_environment_variable>]} |
    -u <connect_without_user_in_kerberos_mode>]
    """
