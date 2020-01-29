import inspect
import json
import optparse
import os
import re
import sys
import time
import django

from scrapy.exceptions import UsageError
from scrapy.utils.misc import walk_modules
from scrapy.utils.project import inside_project

from scrapycw.commands import ScrapycwCommand
from scrapycw.utils.constant import Constant

_SCRAPYCW_COMMAND_CLASS = "scrapycw.commands"


def run():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapycw.web.settings')
    django.setup()

    argv = sys.argv
    # 判断是否在项目中, 如果不在项目中则退出
    if not inside_project():
        _print_not_in_project()
        sys.exit(2)
    # 获取对应命令，如果没有传入命令或者命令不存在则退出
    name = get_command_name(argv)
    if not name:
        _print_commands()
        sys.exit(3)
    if name not in _get_command_objs(_SCRAPYCW_COMMAND_CLASS):
        _print_unknown_command(name)
        sys.exit(4)
    # 获取对应命令，并解析
    cmds = _get_command_objs(_SCRAPYCW_COMMAND_CLASS)
    cmd = cmds[name]
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter())
    parser.usage = "{} %s %s".format(Constant.PROJECT_NAME) % (name, cmd.syntax())
    parser.description = cmd.long_desc()
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[1:])
    # 获取命令行setting
    _run_print_help(parser, cmd.process_options, args, opts)
    # 运行命令
    result = _run_print_help(parser, cmd.run, args, opts)

    if cmd.can_print_result:
        print(json.dumps(result))

    sys.exit(0)


def get_command_name(argv):
    """
    获取command名称，选择第一个不为中划线开头的命令
    :param argv: 请求参数
    :return: command名称
    """
    i = 0
    for arg in argv[1:]:
        if not arg.startswith('-'):
            del argv[i]
            return arg
        i += 1


def _iter_command_classes(module_name):
    for module in walk_modules(module_name):
        for obj in vars(module).values():
            if inspect.isclass(obj) and issubclass(obj, ScrapycwCommand) and obj.__module__ == module.__name__ and not obj == ScrapycwCommand:
                yield obj


def _get_command_objs(module_name):
    cmds = {}
    for cls_name in _iter_command_classes(module_name):
        cmd_name = cls_name.__module__.split('.')[-1]
        cmds[cmd_name] = cls_name()
    return cmds


def _run_print_help(parser, func, *args, **opts):
    try:
        return func(*args, **opts)
    except UsageError as e:
        if str(e):
            parser.error(str(e))
        if e.print_help:
            parser.print_help()
        sys.exit(2)

def _print_commands():
    print("Usage:")
    print("  {} <command> [options] [args]\n".format(Constant.PROJECT_NAME))
    print("Available commands:")
    cmds = _get_command_objs(_SCRAPYCW_COMMAND_CLASS)
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-15s %s" % (cmdname, cmdclass.short_desc()))
    print()
    print('Use "{} <command> -h" to see more info about a command'.format(Constant.PROJECT_NAME))


def _print_not_in_project():
    print("Don't in scrapy project")


def _print_unknown_command(cmdname):
    print("Unknown command: %s\n" % cmdname)
    print('Use "{}" to see available commands'.format(Constant.PROJECT_NAME))


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(run())
