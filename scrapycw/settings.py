import logging
import os
import datetime

from scrapy.utils.conf import closest_scrapy_cfg

__BASE_URL = os.path.dirname(closest_scrapy_cfg())

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
# 爬虫运行时缓存文件目录
SPIDER_RUN_CACHE_DIR = None
# 启动爬虫超时时间
RUN_SPIDER_TIMEOUT = 60

# 临时文件路径
TEMP_FILE_DIR = None

# 开启守护进程超时时间
START_DAEMON_TIMEOUT = 30

IS_DEV = True
# scrapycw 日志文件所在目录
LOGGING_FILE = None
LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

SPIDER_LISTEN_LOOP_TIME = 10

try:
    from scrapycw_settings import * # noqa # pylint: disable=unused-import
except ImportError:
    pass

SERVER_PID_FILENAME = SERVER_PID_FILENAME if SERVER_PID_FILENAME else os.path.join(RUNTIME_PATH, "server.pid")
SPIDER_RUN_CACHE_DIR = SPIDER_RUN_CACHE_DIR if SPIDER_RUN_CACHE_DIR else os.path.join(RUNTIME_PATH, "spider_crawl")
TEMP_FILE_DIR = TEMP_FILE_DIR if TEMP_FILE_DIR else os.path.join(RUNTIME_PATH, "temps")

DEFAULT_LOG_PATH = os.path.join(RUNTIME_PATH, "log")
current_date = datetime.date.today().strftime("%y%m%d")
LOGGING_FILE = LOGGING_FILE if LOGGING_FILE else os.path.join(DEFAULT_LOG_PATH, "scrapycw_{}.log".format(current_date))