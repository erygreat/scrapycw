from scrapy.crawler import CrawlerProcess, CrawlerRunner

from scrapycw.helpers import Helper, ScrapycwHelperException


class SpiderListHelper(Helper):

    def get_value(self):
        spiders = []
        if self.project is None:
            raise ScrapycwHelperException("没有查询到项目：{}".format(self.param_project))
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
                "status": False,
                "message": e.message
            }

        for s in values:
            spiders.append({"name": s})
        return {
            "status": "success",
            "spiders": spiders,
            "project": self.project
        }
