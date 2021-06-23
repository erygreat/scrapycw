from scrapycw.helpers.project import ProjectHelper
from scrapy.crawler import CrawlerRunner
from scrapycw.helpers import Helper, ScrapycwHelperException
from scrapycw.core.error_code import RESPONSE_CODE

class SpiderHelper(Helper):

    def list(self):
        if not self.param_project:
            return self._all_list()
        elif self.project:
            return {
                "spiders": self._list_by_settings(self.settings),
                "project": self.project
            }
        else:
            raise ScrapycwHelperException(code=RESPONSE_CODE.PROJECT_NOT_FIND, message="Project not find: {}".format(self.param_project))

    def all_list(self):
        projects = ProjectHelper().list()
        spiders = []
        for project in projects:
            settings = self._get_settings(project)
            spiders.append({
                "project": project,
                "spiders": self._list_by_settings(settings)
            })
        return spiders

    def _list_by_settings(self, settings):
        crawler_process = CrawlerRunner(settings)
        spiders = []
        for s in sorted(crawler_process.spider_loader.list()):
            spiders.append(s)
        return spiders
