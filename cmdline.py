import inspect
import optparse
import sys

from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import UsageError
from scrapy.settings import Settings
from scrapy.utils.conf import get_config
from scrapy.utils.misc import walk_modules
from scrapy.utils.project import inside_project, get_project_settings

from scrapycw.commands import ScrapycwCommand


_SCRAPYCW_COMMAND_CLASS = "scrapycw.commands"


def run():
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
    parser.usage = "scrapycw %s %s" % (name, cmd.syntax())
    parser.description = cmd.long_desc()
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[1:])
    settings = _get_settings(opts)
    cmd.settings = settings

    _run_print_help(parser, cmd.process_options, args, opts)
    cmd.crawler_process = CrawlerProcess(settings, cmd.can_crawl_log_print)
    result = _run_print_help(parser, cmd.run, args, opts)

    if cmd.can_print:
        print(result)

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


def _get_settings(opts):
    if hasattr(opts, "project"):
        config = get_config()
        for project, dir in config.items('settings'):
            if project == opts.project:
                settings = Settings()
                settings.setmodule(dir, priority='project')
                return settings
        print("don't have {} project".format(opts.project))
        sys.exit(2)
    else:
        return get_project_settings()


def _print_commands():
    print("Usage:")
    print("  scrapycw <command> [options] [args]\n")
    print("Available commands:")
    cmds = _get_command_objs(_SCRAPYCW_COMMAND_CLASS)
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-15s %s" % (cmdname, cmdclass.short_desc()))
    print()
    print('Use "scrapycw <command> -h" to see more info about a command')


def _print_not_in_project():
    print("Don't in scrapy project")


def _print_unknown_command(cmdname):
    print("Unknown command: %s\n" % cmdname)
    print('Use "scrapycw" to see available commands')
