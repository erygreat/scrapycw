import os
import platform
import json
from scrapycw.utils.file_uilts import write_once
import time
import sys

from scrapycw.utils.exception import ScrapycwNotSupportSystemException, ScrapycwArgsMustCanSerializationException
from scrapycw.settings import TEMP_FILE_DIR


def run_in_daemon(func, args=None, has_return_data=False):
    try:
        json.dumps(args)
    except (TypeError, ValueError):
        raise ScrapycwArgsMustCanSerializationException("参数必须可以序列化，请检查参数!")

    temp_dir = TEMP_FILE_DIR
    pid_file_name = os.path.join(temp_dir, "{}.daemon.pid".format(time.time()))
    return_file_name = os.path.join(temp_dir, "{}.daemon.data".format(time.time()))
    error_file_name = os.path.join(temp_dir, "{}.daemon.error".format(time.time()))
    system_os = platform.system()

    if system_os == 'Darwin' or system_os == 'Linux':
        __run_in_linux(func, args, has_return_data, pid_file_name, return_file_name, error_file_name)
    elif system_os == 'Windows':
        __run_in_windows(func, args, has_return_data, pid_file_name, return_file_name, error_file_name)
    else:
        raise ScrapycwNotSupportSystemException("不支持的操作系统: {}".format(system_os))

    # TODO 等待 PID文件生成（需要处理超时）

    # TODO 等待响应数据生成（需要处理超时和没有响应数据）

    # 返回响应数据


def __run_in_windows(func, args, has_return_data, pid_file_name, return_file_name, error_file_name):
    if args is None:
        func()
    else:
        func(args)
    raise ScrapycwNotSupportSystemException("当前不支持 Windows 系统")


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
        sys.exit(0)

    sys.stdout.flush()
    sys.stderr.flush()

    with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr .fileno())
    return True


def __return_callback_wrapper(filename, error_filename):
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


def __run_in_linux(func, args, has_return_data, pid_file_name, return_file_name, error_file_name):
    is_daemon = __fork_daemon_in_linux()
    if not is_daemon:
        return
    else:
        # 保存PID
        ppid = os.getpid()
        write_once(pid_file_name, str(ppid))
        # 执行代码
        callback = __return_callback_wrapper(return_file_name, error_file_name)
        if args and has_return_data:
            func(args, callback)
        elif args and not has_return_data:
            func(args)
        elif not args and has_return_data:
            func(callback)
        else:
            func()
