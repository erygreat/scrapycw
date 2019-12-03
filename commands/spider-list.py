from scrapy.utils.conf import get_config

from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.spider import SpiderListHelper


class Command(ScrapycwCommand):

    can_print = True

    def run(self, args, opts):
        return SpiderListHelper(opts.project, self.cmdline_settings).get_json()

    def short_desc(self):
        return "List of Spider"

    def long_desc(self):
        return "List of Spider"

    def syntax(self):
        return "[option]"
