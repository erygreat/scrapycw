from scrapy.exceptions import UsageError
from scrapy.utils.conf import arglist_to_dict

from scrapycw.commands import ScrapycwCommand
from scrapycw.services.spider import Service


class Command(ScrapycwCommand):

    def run(self, args, opts):
        if len(args) == 0:
            raise UsageError()
        spname = args[0]
        return Service.run(project=opts.project, spname=spname, cmdline_settings=self.cmdline_settings, spargs=opts.spargs)

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
