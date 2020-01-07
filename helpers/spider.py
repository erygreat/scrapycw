from scrapy.crawler import CrawlerRunner

from scrapycw.helpers import Helper, ScrapycwHelperException
from scrapycw.settings import SCRAPY_DEFAULT_PROJECT
from scrapycw.web.api.models import SpiderJob


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


class SpiderRefreshStatusHelper(Helper):

    load_settings = False

    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id

    def get_value(self):
        model = SpiderJob.objects.filter(job_id=self.job_id).get()
        print(self.job_id)

