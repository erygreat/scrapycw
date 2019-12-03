from optparse import OptionGroup

from scrapy.exceptions import UsageError
from scrapy.utils.conf import arglist_to_dict


class ScrapycwCommand:

    crawler_process = None
    can_print = False
    can_crawl_log_print = False

    def __init__(self):
        self.settings = None  # set in scrapy.cmdline

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
            self.settings.setdict(arglist_to_dict(opts.set), priority='cmdline')
        except ValueError:
            raise UsageError("Invalid -s value, use -s NAME=VALUE", print_help=False)

