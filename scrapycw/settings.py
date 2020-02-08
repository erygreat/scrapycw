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

# PID存储文件名m
PID_FILENAME = "server.pid"
# Telnet链接超时时间
TELNET_TIMEOUT = 10
# 每次运行时都会初始化项目数据库、文件等内容
INIT_EACH_RUN = True

try:
    from scrapycw_settings import *
except ImportError:
    pass

PID_FILENAME = os.path.join(RUNTIME_PATH, PID_FILENAME)
