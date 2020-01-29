from scrapy.crawler import CrawlerRunner

from scrapycw.helpers import Helper, ScrapycwHelperException


class SpiderListHelper(Helper):

    def get_value(self):
        spiders = []
        if self.project is None:
            raise ScrapycwHelperException("Project not find: {}".format(self.param_project))
        crawler_process = CrawlerRunner(self.settings)
        for s in sorted(crawler_process.spider_loader.list()):
            spiders.append(s)
        return spiders

    def get_json(self):
        spiders = []
        try:
            values = self.get_value()
        except ScrapycwHelperException as e:
            return {
                "success": False,
                "message": e.message
            }

        for s in values:
            spiders.append({"name": s})
        return {
            "success": True,
            "message": None,
            "spiders": spiders,
            "project": self.project
        }
