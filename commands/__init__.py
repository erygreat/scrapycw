import sys
from optparse import OptionGroup

from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import UsageError
from scrapy.settings import Settings
from scrapy.utils.conf import arglist_to_dict, get_config
from scrapy.utils.project import get_project_settings


class ScrapycwCommand:

    cmdline_settings = {}

    can_print = False
    can_crawl_log_print = False

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
        group = OptionGroup(parser, "Global Options")
        group.add_option("-p", "--project", action="store", help="the project name, default value is 'default'", default="default")
        # group.add_option("--pidfile", metavar="FILE", help="write process ID to FILE")
        group.add_option("-s", "--set", action="append", default=[], metavar="NAME=VALUE", help="set/override setting (may be repeated)")

        parser.add_option_group(group)

    def process_options(self, args, opts):
        try:
            self.cmdline_settings = arglist_to_dict(opts.set)
        except ValueError:
            raise UsageError("Invalid -s value, use -s NAME=VALUE", print_help=False)
