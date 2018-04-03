# -*- coding:utf-8 -*-
import re


def convert_options(helpdoc):
    b = re.split("\n{1,}", helpdoc)
    b = b[1:len(b) - 1]
    f_name = b[0].strip()
    func_name = f_name[0].lower() + f_name[1:]
    out = "def " + func_name + "("
    for i in b[1:]:
        # print(i)
        if i.startswith("<"):
            temp = i[2:i.index('|')]
            if temp.startswith("UserName") or temp.startswith("Password") or temp.startswith("DomainName"):
                out += temp + ": str = None,\n"
            else:
                out += temp + ": str,\n"
        if i.startswith("["):
            temp = i[3:i.index('|')]
            if temp.startswith("ResilienceTimeout"):
                out += temp + ": int = None,\n"
            elif temp.startswith("SecurityDomain"):
                out += temp + ": str = \"Native\" ,\n"
            else:
                out += temp + ": str = None,\n"
    out += ") -> "
    out += " namedtuple(\"" + f_name + "Result\", ['retcode', 'stdout', 'stderr']):\n"
    out += "    subcmd = \"" + f_name + "\""

    return out


def get_options(helpdoc):
    b = re.split("\n{1,}", helpdoc)
    b = b[1:len(b) - 1]
    f_name = b[0].strip()
    func_name = f_name[0].lower() + f_name[1:]
    out = "    options = ["
    for i in b[1:]:
        # print(i)
        if i.startswith("<"):
            out += "\"" + i[2:i.index('|')] + "\","
        if i.startswith("["):
            out += "\"" + i[3:i.index('|')] + "\","
    out += "]\n"
    others = """
    cmd = _checking_infacmd_env_and_ret_base_cmd(domainname=DomainName, username=UserName, password=Password, cmd=base_cmd, subcmd=subcmd)
    options_value_dict = locals()
    for option in options:
        cmd = _assemble_command_options(cmd, option, options_value_dict.get(option))

    mainLogger.debug(cmd)
    res = run_cmd(cmd, env=os.environ)
    mainLogger.info(res)
    stdout = res.stdout # type: str
    stderr = res.stderr # type: str
    if res.retcode == 0:
        pass
    else:
        stderr += stdout
    {result_name}Result = namedtuple(\"{cmdResult}Result\", ['retcode', 'stdout', 'stderr'])
    return {result_name_1}Result(res.retcode, stdout, stderr)
    """.format(result_name=func_name, cmdResult=f_name, result_name_1=func_name)
    out += others
    return out


helpdoc = """
ListBackupFiles 

<-DomainName|-dn> domain_name

[<-SecurityDomain|-sdn> security_domain]

<-UserName|-un> user_name

<-Password|-pd> password

<-ServiceName|-sn> service_name

[<-ResilienceTimeout|-re> timeout_period_in_seconds]
"""

print(convert_options(helpdoc))
print(get_options(helpdoc))
