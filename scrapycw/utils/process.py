import importlib
import inspect
import os
import platform
import json
import time
import sys
import subprocess
import optparse

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, current_dir)
    from scrapy.utils.conf import closest_scrapy_cfg
    project_dir = os.path.dirname(closest_scrapy_cfg())
    sys.path.append(project_dir)

from scrapycw.utils.file_uilts import write_once
from scrapycw.utils.exception import ScrapycwCommandParamMissingException, ScrapycwNotSupportSystemException, ScrapycwArgsMustCanSerializationException
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
        sys.exit(0)

    sys.stdout.flush()
    sys.stderr.flush()

    with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr .fileno())
    return True



def __run_main(func, args, has_return_data, return_file_name, error_file_name, pid_file_name):
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
            "error": e.name,
            "message": e.message
        }
        write_once(error_file_name, json.dumps(error_obj))


def __run_in_windows(func, args, has_return_data, pid_file_name, return_file_name, error_file_name):
    cmd = ['python', os.path.abspath(__file__), 
        "--module", inspect.getmodule(func).__name__,
        "--func", func.__qualname__,
        "--pid_file_name", pid_file_name,
        "--return_file_name", return_file_name,
        "--error_file_name", error_file_name,
    ]

    if args:
        cmd.append("--args")
        cmd.append(json.dumps(args))

    if has_return_data:
        cmd.append("--has_return_data")
    subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # subprocess.Popen(cmd)


def __run_daemon_windows(func, args, has_return_data, return_file_name, error_file_name, pid_file_name):
    __run_main(func, args, has_return_data, return_file_name, error_file_name, pid_file_name)


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

if __name__ == "__main__":
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

    __run_daemon_windows(target_func, args, has_return_data, return_file_name, error_file_name, pid_file_name)
