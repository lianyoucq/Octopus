# -*- coding:utf-8 -*-
import os
import platform
import select
import shlex
import subprocess
import sys
from collections import namedtuple
from datetime import datetime
from octopus.exceptions import UnkownOSTypeException
from octopus.common.logger import rootLogger
from config import Config
from octopus.database.perftrace import Perftrace

if Config.PERFTRACE:
    perfTrace = Perftrace()


def os_type() -> str:
    """uname_result(system='Linux',
                    node='udid.sleety.com',
                    release='4.10.0-42-generic',
                    version='#46~16.04.1-Ubuntu SMP Mon Dec 4 15:57:59 UTC 2017',
                    machine='x86_64',
                    processor='x86_64')
    """
    uname = platform.uname()
    return uname.system


def shell_suffix():
    if os.name == "posix":
        return '.sh'
    elif os.name == "nt":
        return ".bat"
    else:
        raise UnkownOSTypeException("The OS type: {0} is not unknown".format(os.name))


def get_LIBRARY_PATH_NAME():
    """
    Windows is no need to set it
    :return:
    """
    if os_type() in ("Linux", "SunOS"):
        return "LD_LIBRARY_PATH"
    elif os_type() == "AIX":
        return "LIBPATH"
    elif os_type() == "HP-UX":
        return "SHLIB_PATH"
    else:
        return None


def timeit_cmd_decorate(func):
    def wrapper(cmd, *args, **kwargs):
        if Config.PERFTRACE:
            start_time = datetime.now()
            result = func(cmd, *args, **kwargs)
            end_time = datetime.now()
            delta_time = end_time - start_time
            total_seconds = delta_time.total_seconds()
            rootLogger.debug("##### the function {0} costs {1} seconds".format(cmd, total_seconds))

            perfTrace.insert(cmd=cmd, cost=total_seconds, retcode=result.retcode, executing_date=start_time,
                             comments=result.stderr)
        else:
            result = func(cmd, *args, **kwargs)
        return result

    return wrapper


@timeit_cmd_decorate
def run_cmd(cmd: str, env=None, live=False, readsize=10) -> namedtuple("CommandResult",
                                                                       ['retcode', "stdout", "stderr"]):
    """运行系统命令
    :param cmd: 命令
    :param env: 环境变量
    :param live: 实时模式
    :param readsize: 缓冲区大小
    :return: tuple
    """
    # readsize = 1024
    cmdargs = shlex.split(cmd)
    p = subprocess.Popen(cmdargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

    stdout = b''
    stderr = b''
    rpipes = [p.stdout, p.stderr]
    while True:
        rfd, wfd, efd = select.select(rpipes, [], rpipes, 1)

        if p.stdout in rfd:
            dat = os.read(p.stdout.fileno(), readsize)
            if live:
                sys.stdout.buffer.write(dat)
            stdout += dat
            if dat == b'':
                rpipes.remove(p.stdout)
        if p.stderr in rfd:
            dat = os.read(p.stderr.fileno(), readsize)
            stderr += dat
            if live:
                sys.stdout.buffer.write(dat)
            if dat == b'':
                rpipes.remove(p.stderr)
        # only break out if we've emptied the pipes, or there is nothing to
        # read from and the process has finished.
        if (not rpipes or not rfd) and p.poll() is not None:
            break
        # Calling wait while there are still pipes to read can cause a lock
        elif not rpipes and p.poll() is None:
            p.wait()
    p.communicate()
    output = namedtuple("CommandResult", ['retcode', "stdout", "stderr"])
    return output(retcode=p.returncode, stdout=stdout.decode(), stderr=stderr.decode())

# import threading
#
# class Cmd(threading.Thread):
#     def __init__(self, cmd: str, env=None,  live=False, readsize=10):
#         self.cmd_output = namedtuple("CommandResult", ['retcode', "stdout", "stderr"])
#         self.cmd = cmd
#         self.env = env
#         self.live = live
#         self.readsize = readsize
#         threading.Thread.__init__(self)
#
#     def run(self):
#         self.cmd_output = run_cmd(self.cmd, env=self.env, live=self.live, readsize=self.readsize)


def is_none(value: str, treat_space_as_none=True) -> bool:
    if value is None:
        return True
    if treat_space_as_none and value.rstrip().rstrip() == "":
        return True
    return False