from scrapy.utils.conf import get_config

from scrapycw.commands import ScrapycwCommand


class Command(ScrapycwCommand):

    can_print = True

    def run(self, args, opts):
        spiders = []
        for s in sorted(self.crawler_process.spider_loader.list()):
            spiders.append({"name": s})
        return {
            "status": "success",
            "spiders": spiders,
            "project": opts.project
        }

    def short_desc(self):
        return "List of Spider"

    def long_desc(self):
        return "List of Spider"

    def syntax(self):
        return "[option]"
