from scrapy.utils.conf import get_config

from scrapycw.commands import ScrapycwCommand


class Command(ScrapycwCommand):

    def run(self, args, opts):
        # sorted(self.crawler_process.spider_loader.list()
        self.prn_obj(self.crawler_process)

    def short_desc(self):
        return "List of Spider"

    def long_desc(self):
        return "List of Spider"

    def prn_obj(self, obj):
        print(dir(obj))
        print(obj)
