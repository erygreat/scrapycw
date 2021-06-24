import logging
import os

from scrapy.utils.conf import closest_scrapy_cfg

__BASE_URL = os.path.dirname(closest_scrapy_cfg())

# 服务器运行端口
SERVER_PORT = 2312
# 服务器支持的IP
SERVER_HOST = "localhost"

# scrapy默认项目
SCRAPY_DEFAULT_PROJECT = "default"
# 运行时存储位置
RUNTIME_PATH = os.path.join(__BASE_URL, "runtime_scrapycw")

# PID存储文件名
SERVER_PID_FILENAME = None
# Telnet链接超时时间
TELNET_TIMEOUT = 10
# 每次运行时都会初始化项目数据库、文件等内容
INIT_EACH_RUN = False

# 处理的日志的最大大小
HANDLE_LOG_MAXIMUM_SIZE = 500 * 1024 * 1024
# HANDLE_LOG_MAXIMUM_SIZE = 4 * 1024
SPIDER_RUN_CACHE_DIR = None
# 启动爬虫超时时间
RUN_SPIDER_TIMEOUT = 60 * 1000

# 临时文件路径
TEMP_FILE_DIR = None

# 开启守护进程超时时间
START_DAEMON_TIMEOUT = 5000

IS_DEV = True
# 日志文件所在目录
LOGGING_FILE = os.path.join(RUNTIME_PATH, "log/info.log");
LOGGERG_LEVEL = logging.DEBUG

try:
    from scrapycw_settings import * # noqa # pylint: disable=unused-import
except ImportError:
    pass

if not SERVER_PID_FILENAME:
    SERVER_PID_FILENAME = os.path.join(RUNTIME_PATH, "server.pid")

if not SPIDER_RUN_CACHE_DIR:
    SPIDER_RUN_CACHE_DIR = os.path.join(RUNTIME_PATH, "spider_crawl")

if not TEMP_FILE_DIR:
    TEMP_FILE_DIR = os.path.join(RUNTIME_PATH, "temps")
