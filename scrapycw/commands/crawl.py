from scrapy.exceptions import UsageError
from scrapy.utils.conf import arglist_to_dict

from scrapycw.core.error_code import RESPONSE_CODE
from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.spider import SpiderRunnerHelper
from scrapycw.utils.response import Response


class Command(ScrapycwCommand):

    def run(self, args, opts):
        if len(args) == 0:
            return Response(
                success=False,
                message="Please enter spider name",
                data={
                    "project": opts.project,
                },
                code=RESPONSE_CODE.NOT_ENTER_SPIDER_NAME
            )
        spname = args[0]
        return SpiderRunnerHelper(
            project=opts.project,
            cmdline_settings=self.cmdline_settings
        ).get_response(
            spname=spname,
            spargs=opts.spargs
        )

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
