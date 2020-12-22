from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers.spider import SpiderListHelper


class Command(ScrapycwCommand):

    def run(self, args, opts):
        return SpiderListHelper(opts.project, self.cmdline_settings).get_response()

    def short_desc(self):
        return "List of Spider"

    def long_desc(self):
        return "List of Spider"

    def syntax(self):
        return "[option]"
