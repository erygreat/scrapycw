from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import UsageError
from scrapy.extensions.telnet import TelnetConsole
from scrapy.settings import Settings
from scrapy.utils.conf import get_config, arglist_to_dict

from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers import ScrapycwHelperException


class Command(ScrapycwCommand):

    can_crawl_log_print = True

    def run(self, args, opts):
        settings = self.__get_settings(opts.project)
        if settings is None:
            raise ScrapycwHelperException("Project not find: {}".format(opts.project))
        spname = args[0]

        process = CrawlerProcess(settings)
        process.crawl(spname, **opts.spargs)

        # 获取Scrapy Telnet
        telnet_middleware = None
        for crawl in process.crawlers:
            for mv in crawl.extensions.middlewares:
                if isinstance(mv, TelnetConsole):
                    telnet_middleware = mv

        # 开启
        print("host: {}, port: {}, username: {}, password: {}".format(telnet_middleware.host, telnet_middleware.port.port, telnet_middleware.username, telnet_middleware.password))
        process.start()
        print("host: {}, port: {}, username: {}, password: {}".format(telnet_middleware.host, telnet_middleware.port.port, telnet_middleware.username, telnet_middleware.password))

    def short_desc(self):
        return "Run Spider"

    def long_desc(self):
        return "Run Spider"

    def syntax(self):
        return "<spider-name> [option] "

    def add_options(self, parser):
        ScrapycwCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")

    def process_options(self, args, opts):
        ScrapycwCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)

    def __get_settings(self, project):
        config = get_config()
        for _project, dir in config.items('settings'):
            if project == _project:
                self.project = project
                settings = Settings()
                settings.setmodule(dir, priority='project')
                return settings
        return None
