from scrapy.exceptions import UsageError
from scrapy.utils.conf import arglist_to_dict

from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.crawl import CrawlHelper


class Command(ScrapycwCommand):

    def run(self, args, opts):
        if len(args) == 0:
            return {
                "success": False,
                "message": "Please enter spider name",
                "project": opts.project,
            }
        spname = args[0]
        return CrawlHelper(spname=spname, spargs=opts.spargs, project=opts.project, cmdline_settings=self.cmdline_settings).get_json()

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
