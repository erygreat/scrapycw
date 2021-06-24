from scrapy.exceptions import UsageError
from scrapy.utils.conf import arglist_to_dict
from scrapycw.core.slogger import getLogger

from scrapycw.settings import SCRAPY_DEFAULT_PROJECT
from scrapycw.core.exception import ScrapycwException


class ScrapycwCommandException(ScrapycwException):
    pass


class ScrapycwCommand:

    cmdline_settings = {}

    can_print_result = True
    can_crawl_log_print = False

    logger = None

    def __init__(self, name):
        self.logger = getLogger(name)

    def syntax(self):
        return "[options]"

    def run(self, args, opts):
        pass

    def short_desc(self):
        pass

    def long_desc(self):
        pass

    def add_options(self, parser):
        """
        Populate option parse with options available for this command
        """
        parser.add_option("-p", "--project", action="store", help="项目名称，默认为'default'", default=SCRAPY_DEFAULT_PROJECT)
        parser.add_option("-s", "--set", action="append", default=[], metavar="NAME=VALUE", help="set/override setting (may be repeated)")

    def process_options(self, args, opts):
        try:
            self.cmdline_settings = arglist_to_dict(opts.set if hasattr(opts, "set") else [])
        except ValueError:
            raise UsageError("Invalid -s value, use -s NAME=VALUE", print_help=False)
