import os

SERVER_PORT = 2312
SERVER_HOST = "localhost"

SCRAPY_DEFAULT_PROJECT = "default"

__BASE_URL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RUNTIME_PATH = os.path.join(__BASE_URL, "runtime_scrapycw")
PID_FILENAME = "server.pid"

try:
    from scrapycw_settings import *
except ImportError:
    pass

PID_FILENAME = os.path.join(RUNTIME_PATH, PID_FILENAME)
