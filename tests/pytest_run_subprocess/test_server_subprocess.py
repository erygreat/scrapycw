from _pytest.config import ExitCode
from scrapycw import settings
from scrapycw.commands.server import Command

import time
import requests
import pytest


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def pytest_run_server():
    opts = Dict()
    opts['daemon'] = True
    opts['port'] = settings.SERVER_PORT
    opts['host'] = settings.SERVER_HOST

    Command().run(["start"], opts)

    print("服务进程加载!")
    time.sleep(3)
    response = requests.get("http://localhost:2312/i/ping")
    assert(response.status_code == 200)
    print("请求数据成功!")

    Command().run(["stop"], None)

    print("服务进程关闭!")
    time.sleep(3)
    try:
        response = requests.get("http://localhost:2312/i/ping")
        assert(False)
    except requests.exceptions.ConnectionError:
        assert(True)

    print("服务进程已关闭!")