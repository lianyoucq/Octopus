# -*- coding:utf-8 -*-
import os, sys
from config import Config
import config

def get_current_real_path(path="."):
    return os.path.realpath(path)


def get_root_dir():
    current_file_path =  os.path.dirname(os.path.abspath(__file__))
    return current_file_path[:-15]


def get_work_dir():
    return os.path.join(get_root_dir(), 'workdir')


def get_backup_dir(backup_path: str=None, domain_name: str=None) -> str:
    """
    获取Domain备份目录
    如果backup_path是一个绝对路径的目录，那么就使用这个目录存储【不存在，会尝试创建此目录】
    如果domain_name存在，那么会存储到domain_name子目录里，否则存储到backup_path或者当前工作目录里。
    :param backup_path: 绝对路径的目录
    :param domain_name: domain name
    :return: 备份路径
    """
    if backup_path is not None and os.path.isabs(backup_path) and os.path.isdir(backup_path):
        backup_folder = backup_path
    else:
        backup_folder = get_work_dir()

    if domain_name is not None:
        backup_folder = os.path.join(backup_folder, domain_name)
        if not os.path.exists(backup_folder):
            os.mkdir(backup_folder)
        return backup_folder

    return get_work_dir()


def get_test_resources_dir():
    return os.path.join(os.path.join(get_root_dir(), "tests"),  "resources")
