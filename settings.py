SERVER_PORT = 2312
SERVER_HOST = "localhost"

SCRAPY_DEFAULT_PROJECT = "default"

try:
    from scrapycw_settings import *
except ImportError:
    pass
