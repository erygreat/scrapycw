from abc import abstractmethod
import os
from scrapycw.utils.file_uilts import write_once
from scrapycw.utils.exception import ScrapycwDaemonProcessException
from scrapycw.utils.process import run_in_daemon
import sys
import psutil

from scrapycw import settings
from scrapycw.commands import ScrapycwCommand, ScrapycwCommandException
from scrapycw.core.error_code import RESPONSE_CODE
from scrapycw.django_manage import main as django_main
from scrapycw.settings import SERVER_PID_FILENAME
from scrapycw.utils.constant import Constant
from scrapycw.utils.network import port_is_used
from scrapycw.utils.pid import get_pid_by_file, kill_pid


class Command(ScrapycwCommand):

    can_print_result = False

    pid_file = SERVER_PID_FILENAME

    SUB_COMMAND = ["start", "restart", "stop"]

    def syntax(self):
        return "<start|restart|stop> [options]"

    def run(self, args, opts):
        if len(args) == 0:
            sub_command = "start"
        else:
            sub_command = args[0]

        if sub_command not in self.SUB_COMMAND:
            sub_command_str = "|".join(self.SUB_COMMAND)
            raise ScrapycwCommandException(
                code=RESPONSE_CODE.NOT_SUPPORT_SUB_COMMAND,
                message="Can't find sub command {}, you can us {}".format(sub_command, sub_command_str)
            )

        if sub_command == "start":
            return self.__start(args, opts)
        elif sub_command == "stop":
            return self.__stop(args, opts)
        elif sub_command == "restart":
            self.__stop(args, opts)
            print()
            self.__start(args, opts)

    def __stop(self, args, opts):
        print("stop web server...")
        pid = get_pid_by_file(self.pid_file)
        if pid is None:
            print("pid file '{}' is not exist, can\'t close".format(self.pid_file))
            return
        pid = int(pid)

        is_project = False
        proc = None
        children_pids = []
        for _proc in psutil.process_iter():
            if pid == _proc.pid:
                cmdline = _proc.cmdline()
                cmdline = " ".join(cmdline)
                if cmdline.find(Constant.PROJECT_NAME) > -1:
                    is_project = True
                proc = _proc
            if _proc.parent() is not None and _proc.parent().pid == pid:
                children_pids.append(_proc.pid)

        if proc is None:
            print('don\'t have pid "{}" '.format(pid))
            return

        if not is_project:
            print('pid "{}" is not {} web service'.format(pid, Constant.PROJECT_NAME))
            return

        if kill_pid(pid):
            print("关闭进程成功! 进程ID: {}".format(pid))
        else:
            print("没有该进程! 进程ID: {}".format(pid))

        for children_pid in children_pids:
            if kill_pid(children_pid):
                print("关闭进程成功! 进程ID: {}".format(children_pid))
            else:
                print("没有该进程! 进程ID: {}".format(children_pid))

        os.remove(self.pid_file)
        print("关闭web service 完成")

    def __start(self, args, opts):
        sys.argv = []
        sys.argv.append(os.path.abspath(os.path.dirname(__file__)) + "/../django_manage.py")
        sys.argv.append("runserver")
        sys.argv.append("{}:{}".format(opts.host, opts.port))

        can_use_port = not port_is_used(opts.port)
        print("start web service ...")

        if not can_use_port:
            print("port:{} is used".format(opts.port))
            return

        # TODO 简化、抽取创建守护进程流程，修改为只使用一次fork，主进程基本上会很快死掉，不存在僵尸进程的问题
        if opts.daemon:
            try:
                run_in_daemon(Command.__start_server, has_return_data=True)
            except ScrapycwDaemonProcessException as e:
                print("启动后台服务进程失败，失败原因: {}".format(e.message))
                return
        else:
            ppid = os.getpid()
            write_once(self.pid_file, ppid)
            Command.__start_server()

            print("start web service finish!")

    @staticmethod
    def __start_server(callback):
        callback("开启后台服务进程成功!")
        django_main()

    def short_desc(self):
        return "Run Web Service"

    def long_desc(self):
        return "Run Web Service"

    def add_options(self, parser):
        ScrapycwCommand.add_options(self, parser)
        parser.add_option("--port", metavar="<PORT>", help="web服务端口", default=settings.SERVER_PORT, type="int")
        parser.add_option("--host", metavar="<HOST>", help="监听的IP地址，当为0时表示完全公开", default=settings.SERVER_HOST)
        parser.add_option("--daemon", metavar="True", action="store_true", help="是否通过守护线程的方式启动", default=False)
