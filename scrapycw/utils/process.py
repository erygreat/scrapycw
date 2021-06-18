import importlib
import inspect
import os
import platform
import json
import time
import sys
import subprocess
import optparse
import nanoid
import psutil

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, current_dir)
    from scrapy.utils.conf import closest_scrapy_cfg
    project_dir = os.path.dirname(closest_scrapy_cfg())
    sys.path.append(project_dir)

from scrapycw.utils.file_utils import read_until_once_or_timeout, read_until_or_timeout, remove_file_if_exists, write_once
from scrapycw.utils.exception import ScrapycwCommandParamMissingException, ScrapycwDaemonProcessException, ScrapycwDaemonStartTimeoutException, ScrapycwNotSupportSystemException, ScrapycwArgsMustCanSerializationException, ScrapycwReadException
from scrapycw.settings import START_DAEMON_TIMEOUT, TEMP_FILE_DIR


def run_in_daemon(func, args=None, has_return_data=False):
    """
    启动守护进程，支持Windows、Linux、MacOS
    :params func 执行的函数，必须是静态函数
    :params args 函数的参数
    :params has_return_data 是否有需要从守护进程获取的数据，如果有，主进程会等待数据，另外如果需要显示错误，也需要使用该参数
    :example
    ```
    class Demo1:
        @staticmethod
        def hello(args, callback):
            '''
            :params args 传递的参数，如果传递过来的有这个参数，才能有这个参数
            :params callback 可以向主进程发送数据，只能使用一次，如果 has_return_data 为 True 时才有这个参数，否则不可以有这个参数
            '''
            callback("子进程启动成功!");
            with open(args['filename'], 'w+', encoding='utf-8') as f:
                f.write(args['data'])

        def main(self):
            pid, result = run_in_daemon(Demo.hello, args={
                "filename": "/path/filename.txt",
                "data": "hello world"
            }, has_return_data=True)
    ```
    :example
    ```
    class Demo2:
        @staticmethod
        def hello(args):
            '''
            :params args 传递的参数，如果传递过来的有这个参数，才能有这个参数
            '''
            with open(args['filename'], 'w+', encoding='utf-8') as f:
                f.write(args['data'])

        def main(self):
            pid = run_in_daemon(Demo.hello, args={
                "filename": "/path/filename.txt",
                "data": "hello world"
            }, has_return_data=False)
    ```
    :example
    ```
    class Demo3:
        @staticmethod
        def hello():
            print("hello world")

        def main(self):
            pid = run_in_daemon(Demo.hello)
    ```
    """
    # 检查序列化
    try:
        json.dumps(args)
    except (TypeError, ValueError):
        raise ScrapycwArgsMustCanSerializationException("参数必须可以序列化，请检查参数!")

    # 获取数据存储路径
    temp_dir = TEMP_FILE_DIR
    file_key = str(time.time()) + "." + nanoid.generate(size=12)
    pid_file_name = os.path.join(temp_dir, "{}.daemon.pid".format(file_key))
    return_file_name = os.path.join(temp_dir, "{}.daemon.data".format(file_key))
    error_file_name = os.path.join(temp_dir, "{}.daemon.error".format(file_key))

    # 检查操作系统，并启动守护进程运行后台代码
    system_os = platform.system()
    if system_os == 'Darwin' or system_os == 'Linux':
        __run_in_linux(func, args, has_return_data, pid_file_name, return_file_name, error_file_name)
    elif system_os == 'Windows':
        __run_in_windows(func, args, has_return_data, pid_file_name, return_file_name, error_file_name)
    else:
        raise ScrapycwNotSupportSystemException("不支持的操作系统: {}".format(system_os))

    # 等待 PID 文件生成（守护进程创建完成）
    try:
        pid = read_until_or_timeout(pid_file_name, START_DAEMON_TIMEOUT)
        pid = int(pid)
    except ScrapycwReadException:
        raise ScrapycwDaemonStartTimeoutException("启动守护进程超时!")

    if not has_return_data:
        remove_file_if_exists(pid_file_name)
        remove_file_if_exists(error_file_name)
        remove_file_if_exists(return_file_name)
        return pid

    # 等待响应数据生成
    try:
        type, data = read_until_once_or_timeout([
            {
                'type': "error",
                'filename': error_file_name,
            },
            {
                'type': 'data',
                'filename': return_file_name
            }
        ], START_DAEMON_TIMEOUT)
        data = json.loads(data)
        if type == 'error':
            raise ScrapycwDaemonProcessException('守护进程运行异常, {}'.format(data['message']))
    except ScrapycwReadException:
        raise ScrapycwDaemonStartTimeoutException("读取守护进程数据超时!")

    remove_file_if_exists(pid_file_name)
    remove_file_if_exists(error_file_name)
    remove_file_if_exists(return_file_name)
    return pid, data


def __run_in_linux(func, args, has_return_data, pid_file_name, return_file_name, error_file_name):
    is_daemon = __fork_daemon_in_linux()
    if not is_daemon:
        return
    else:
        __run_main(func, args, has_return_data, pid_file_name, return_file_name, error_file_name)


def __fork_daemon_in_linux():
    """
    创建一个后台进程，在Linux，如果是主进程，返回 False，如果是后台进程，返回 True
    """
    pid = os.fork()
    if pid:
        return False
    os.umask(0)
    os.setsid()

    _pid = os.fork()
    if _pid:
        os._exit(0)

    sys.stdout.flush()
    sys.stderr.flush()

    with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr .fileno())
    return True


def __run_main(func, args, has_return_data, pid_file_name, return_file_name, error_file_name):
    # 保存PID
    ppid = os.getpid()
    write_once(pid_file_name, str(ppid))
    # 执行代码
    callback = __return_callback_wrapper(return_file_name, error_file_name)
    try:
        if args and has_return_data:
            func(args, callback)
        elif args and not has_return_data:
            func(args)
        elif not args and has_return_data:
            func(callback)
        else:
            func()
    except Exception as e:
        error_obj = {
            "error": e.name if getattr(e, "name", None) else str(e),
            "message": e.message if getattr(e, "message", None) else str(e),
        }
        write_once(error_file_name, json.dumps(error_obj))
    os._exit(0)


def __run_in_windows(func, args, has_return_data, pid_file_name, return_file_name, error_file_name):

    cmd = ['python', os.path.abspath(__file__), "--module", inspect.getmodule(func).__name__, "--func", func.__qualname__, "--pid_file_name", pid_file_name, "--return_file_name", return_file_name, "--error_file_name", error_file_name]

    if args:
        cmd.append("--args")
        cmd.append(json.dumps(args))

    if has_return_data:
        cmd.append("--has_return_data")
    subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def __run_daemon_windows(func, args, has_return_data, pid_file_name, return_file_name, error_file_name):
    __run_main(func, args, has_return_data, pid_file_name, return_file_name, error_file_name)


def __return_callback_wrapper(filename, error_filename):
    """
    获取守护进程发送消息回调，使用闭包来解决使用指定文件问题
    """
    def callback(value):
        try:
            write_once(filename, json.dumps(value))
        except (TypeError, ValueError):
            error_obj = {
                "error": ScrapycwArgsMustCanSerializationException.__name__,
                "message": "运行输出内容必须可以序列化"
            }
            write_once(error_filename, json.dumps(error_obj))
    return callback


def is_running(pid):
    """
    进程是否在运行
    :params pid 进程ID
    """
    for _proc in psutil.process_iter():
        if pid == _proc.pid:
            return True
    return False


def kill_process(pid, timeout=5000):
    """
    关闭进程
    :params pid 进程ID
    :params timeout 关闭超时时间, 单位毫秒
    """
    proc = None
    for _proc in psutil.process_iter():
        if pid == _proc.pid:
            proc = _proc
            break
    if not proc:
        return True

    start_time = time.time() * 1000
    try:
        proc.kill()
        while is_running(pid):
            if time.time() * 1000 - start_time > timeout:
                return False
            time.sleep(0.01)
        return True
    except OSError:
        return False


if __name__ == "__main__":
    """
    Windows 守护进程启动代码
    TODO 这里存在一个问题，就是如果这下面代码出现了 ERROR，那么在其他地方是无法知道报了什么错的，因此需要找个地方对错误进行记录，不过考虑到代码都是内部使用的，所以相信内部代码不会写出这种问题，所以暂时先不解决，等到真的需要时在解决
    """
    if platform.system() != "Windows":
        sys.exit(0)

    argv = sys.argv
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter())
    group = optparse.OptionGroup(parser, "Global Options")
    group.add_option("--module", action="store")
    group.add_option("--func", action="store")
    group.add_option("--args", action="store")
    group.add_option("--pid_file_name", action="store")
    group.add_option("--return_file_name", action="store")
    group.add_option("--error_file_name", action="store")
    group.add_option("--has_return_data", action="store_true", default=False)
    parser.add_option_group(group)
    opts, args = parser.parse_args(args=argv[1:])
    module_name = opts.module
    function_name = opts.func
    args = opts.args
    has_return_data = opts.has_return_data
    return_file_name = opts.return_file_name
    error_file_name = opts.error_file_name
    pid_file_name = opts.pid_file_name
    if not module_name:
        raise ScrapycwCommandParamMissingException("请输入模块名称 --module")
    if not function_name:
        raise ScrapycwCommandParamMissingException("请输入函数名称 --func")
    if not return_file_name:
        raise ScrapycwCommandParamMissingException("请输入返回内容存储文件 --return_file_name")
    if not error_file_name:
        raise ScrapycwCommandParamMissingException("请输入错误数据存储文件 --error_file_name")
    if not pid_file_name:
        raise ScrapycwCommandParamMissingException("请输入pid存储文件 --pid_file_name")
    if opts.args:
        args = json.loads(args)

    function_names = function_name.split(".")
    target_module = importlib.import_module(module_name)
    target_func = target_module
    for function_name in function_names:
        target_func = getattr(target_func, function_name)

    __run_daemon_windows(target_func, args, has_return_data, pid_file_name, return_file_name, error_file_name)
