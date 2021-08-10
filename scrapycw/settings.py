import logging
import os
import datetime
import sys

from scrapy.utils.conf import closest_scrapy_cfg

__BASE_URL = os.path.dirname(closest_scrapy_cfg())
sys.path.append(__BASE_URL)

# 服务器运行端口
SERVER_PORT = 2312
# 服务器支持的IP
SERVER_HOST = "localhost"
# PID存储文件名
SERVER_PID_FILENAME = None

# scrapy默认项目
SCRAPY_DEFAULT_PROJECT = "default"
# 运行时存储位置
RUNTIME_PATH = os.path.join(__BASE_URL, "runtime_scrapycw")

# Telnet链接超时时间
TELNET_TIMEOUT = 10
# 每次运行时都会初始化项目数据库、文件等内容
INIT_EACH_RUN = False

# 处理的爬虫日志的最大大小
HANDLE_LOG_MAXIMUM_SIZE = 500 * 1024 * 1024
# 处理日志和输出时是否使用当前时区时间（Scrapy 使用的是 UTC, 因此显示的时间都会差对应时区，见 https://github.com/scrapy/scrapy/issues/2992）
HANDLE_LOG_USE_TIMEZONE = True
# 开启守护进程超时时间
START_DAEMON_TIMEOUT = 30

# 临时文件路径
TEMP_FILE_DIR = None

# scrapycw 日志文件所在目录
LOGGING_FILE = None
LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

# 每隔该秒数检测一下爬虫是否存在的心跳
SPIDER_LISTEN_LOOP_TIME = 10

try:
    from scrapycw_settings import *  # type: ignore # noqa
except ImportError:
    pass

SERVER_PID_FILENAME = SERVER_PID_FILENAME if SERVER_PID_FILENAME else os.path.join(RUNTIME_PATH, "server.pid")
TEMP_FILE_DIR = TEMP_FILE_DIR if TEMP_FILE_DIR else os.path.join(RUNTIME_PATH, "temps")

DEFAULT_LOG_PATH = os.path.join(RUNTIME_PATH, "logs")
LOGGING_FILE = LOGGING_FILE if LOGGING_FILE else os.path.join(DEFAULT_LOG_PATH, "scrapycw_{}.log".format(datetime.date.today().strftime("%y%m%d")))
