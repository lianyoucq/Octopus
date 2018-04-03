# -*- coding:utf-8 -*-
import logging.config
import os
import logging
from octopus.common.path_utils import get_work_dir

LOG_CONF_FILE = os.path.join(get_work_dir(), "log.conf")
logging.config.fileConfig(LOG_CONF_FILE)

rootLogger = logging.getLogger("root")
mainLogger = logging.getLogger("main")

# Import the log level
# from logging import DEBUG, INFO, WARNING, ERROR, FATAL, CRITICAL
