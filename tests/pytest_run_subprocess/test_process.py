from scrapycw.utils.exception import ScrapycwDaemonProcessException
from scrapycw.utils.process import is_running, kill_process, run_in_daemon
import time


def hello(callback):
    callback("hello")
    time.sleep(10)


def hello2():
    time.sleep(10)


def hello3(args, callback):
    host = args['host']
    port = args['port']
    callback("IP: {}, 端口号: {}".format(host, port))
    time.sleep(10)


def hello_exception():
    raise Exception("这是一个Error")


def hello_exception_normal(callback):
    raise Exception("这是一个Error")


class Demo1:
    class Demo2:
        @staticmethod
        def hello(callback):
            callback("hello")
            time.sleep(10)


def pytest_run_daemon_1():
    start_time = time.time()
    pid, result = run_in_daemon(hello, has_return_data=True)
    assert(pid > 0)
    assert(result == 'hello')
    assert(time.time() - start_time < 10)


def pytest_run_daemon_2():
    start_time = time.time()
    pid = run_in_daemon(hello2, has_return_data=False)
    assert(pid > 0)
    assert(time.time() - start_time < 10)


def pytest_run_daemon_3():
    start_time = time.time()
    pid, result = run_in_daemon(hello3, args={
        "host": "127.0.0.1",
        "port": 80
    }, has_return_data=True)
    assert(pid > 0)
    assert(result == 'IP: 127.0.0.1, 端口号: 80')
    assert(time.time() - start_time < 10)


def pytest_run_daemon_exception():
    pid = run_in_daemon(hello_exception)
    assert(pid > 0)


def pytest_run_daemon_exception_normal():
    try:
        pid = run_in_daemon(hello_exception_normal, has_return_data=True)
        assert(pid > 0)
    except ScrapycwDaemonProcessException:
        assert(True)


def pytest_run_daemon_static_method():
    start_time = time.time()
    pid, result = run_in_daemon(Demo1.Demo2.hello, has_return_data=True)
    assert(pid > 0)
    assert(result == 'hello')
    assert(time.time() - start_time < 10)


def pytest_is_running():
    pid, result = run_in_daemon(hello, has_return_data=True)
    flag = is_running(pid)
    assert(flag)


def pytest_kill():
    start_time = time.time()
    pid, result = run_in_daemon(hello, has_return_data=True)
    assert(pid > 0)
    assert(result == 'hello')
    flag = is_running(pid)
    assert(flag)
    kill_flag = kill_process(pid)
    assert(kill_flag)
    flag = is_running(pid)
    assert(not flag)
    assert(time.time() - start_time < 10)
