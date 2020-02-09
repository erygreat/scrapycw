from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.spider import SpiderHelper


class Command(ScrapycwCommand):

    def run(self, args, opts):
        return SpiderHelper(opts.project, self.cmdline_settings).list()

    def short_desc(self):
        return "List of Spider"

    def long_desc(self):
        return "List of Spider"

    def syntax(self):
        return "[option]"
