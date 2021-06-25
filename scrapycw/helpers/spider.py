import json
import os
import nanoid
import time

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.extensions.telnet import TelnetConsole

from scrapycw.utils.scpraycw import get_scrapy_settings
from scrapycw.utils.process import run_in_daemon
from scrapycw.utils.json_encoder import ScrapySettingEncoder
from scrapycw.helpers import Helper, ScrapycwHelperException
from scrapycw.helpers.project import ProjectHelper
from scrapycw.core.error_code import RESPONSE_CODE
from scrapycw.web.api.models import SpiderJob

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

    def crawl(self, spname, spargs):
        if not spname:
            raise ScrapycwHelperException(code=RESPONSE_CODE.NOT_ENTER_SPIDER_NAME, message="请输入爬虫名称！")

        if not self.project:
            raise ScrapycwHelperException(code=RESPONSE_CODE.PROJECT_NOT_FIND, message="没有项目[{}]".format(self.param_project))

        run_spider_args = {
            "project": self.project,
            "spname": spname,
            "spargs": spargs,
            "cmdline_settings": self.cmdline_settings
        }
        _, data = run_in_daemon(SpiderHelper.run_spider, args=run_spider_args, has_return_data=True)
        return self.__handler_spider_data(data, spname, spargs)

    def __handler_spider_data(self, data, spname, spargs):
        job_id = data['job_id']
        log_file = data['log_file']
        telnet_username = data['telnet_username']
        telnet_password = data['telnet_password']
        telnet_host = data['telnet_host']
        telnet_port = data['telnet_port']
        settings = data['settings']
        start_time = data['start_time']
        # TODO 保存到数据库中
        # job_model = SpiderJob(
        #     job_id=job_id,
        #     project=self.project,
        #     spider=spname,
        #     spargs=spargs,
        #     telnet_username=telnet_username,
        #     telnet_password=telnet_password,
        #     telnet_host=telnet_host,
        #     telnet_port=telnet_port,
        #     status=SpiderJob.STATUS.RUNNING,
        #     log_file=log_file,
        #     start_time=start_time,
        #     cmdline_settings=self.cmdline_settings,
        #     settings=settings,
        # )
        # job_model.save()
        return {
            "job_id": job_id,
            "project": self.project,
            "spider": spname,
            "log_file": log_file,
            "telnet": {
                "host": telnet_host,
                "port": telnet_port,
                "username": telnet_username,
                "password": telnet_password
            }
        }

    @staticmethod
    def run_spider(args, callback=None):
        project = args['project']
        cmdline_settings = args['cmdline_settings']
        spname = args['spname']
        spargs = args['spargs']
        # 获取 settings
        settings = get_scrapy_settings(project)
        if settings:
            settings.setdict(cmdline_settings, priority='cmdline')
        if not settings:
            raise ScrapycwHelperException(code=RESPONSE_CODE.PROJECT_NOT_FIND, message="没有项目[{}]".format(project))

        # 获取爬虫进程
        process = CrawlerProcess(settings)
        try:
            process.crawl(spname, **spargs)
        except KeyError:
            raise ScrapycwHelperException(code=RESPONSE_CODE.SPIDER_NOT_FIND, message="Spider not found: {}".format(spname))

        crawl = None
        for _crawl in process.crawlers:
            crawl = _crawl
        if not crawl:
            raise ScrapycwHelperException(code=RESPONSE_CODE.SPIDER_CODE_HAVE_BUG, message="爬虫启动失败，请检查爬虫代码是否正确，引入的依赖文件是否存在!")

        # 获取 Telnet 拓展信息
        telnet_middleware = None
        for mv in crawl.extensions.middlewares:
            if isinstance(mv, TelnetConsole):
                telnet_middleware = mv

        # 将爬虫信息发送回主进程
        log_path = crawl.settings.get("LOG_FILE", None)
        if log_path:
            log_path = os.path.abspath(log_path)

        settings_str = json.dumps({key: value for key, value in settings.items()}, cls=ScrapySettingEncoder)
        job_id = "{}_{}".format(time.strftime("%Y%m%d_%H%M%S", time.localtime()), nanoid.generate(size=12))
        callback({
            "job_id": job_id,
            "spider": spname,
            "telnet_username": telnet_middleware.username,
            "telnet_password": telnet_middleware.password,
            "telnet_host": telnet_middleware.host,
            "telnet_port": telnet_middleware.port.port,
            "status": SpiderJob.STATUS.RUNNING,
            "settings": settings_str,
            "log_file": log_path,
            "start_time": time.time(),
        })

        if process:
            process.start()
