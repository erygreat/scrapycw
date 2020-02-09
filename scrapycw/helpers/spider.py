import datetime
import os
import sys
import time

from scrapy.crawler import CrawlerRunner
from scrapy.extensions.telnet import TelnetConsole
from scrapycw.web.api.models import SpiderJob

from scrapycw.helpers import Helper, ScrapycwHelperException
from scrapycw.scrapyrewrite.crawler import CustomCrawlerProcess
from scrapycw.utils import random


class SpiderHelper(Helper):

    def crawl(self, spname, spargs=None):
        try:
            return self._crawl(spname, spargs)
        except ScrapycwHelperException as e:
            return {
                "success": False,
                "message": e.message,
                "project": self.project,
                "spider": spname,
            }

    def _crawl(self, spname, spargs=None):
        if spname is None:
            raise ScrapycwHelperException("Spider not null")

        if self.project is None:
            raise ScrapycwHelperException("Project not find: {}".format(self.param_project))

        process = CustomCrawlerProcess(self.settings)
        try:
            process.crawl(spname, **spargs)
        except KeyError as e:
            raise ScrapycwHelperException("Spider not found: {}".format(spname))

        # 获取Scrapy Telnet
        telnet_middleware = None
        crawl = None
        for _crawl in process.crawlers:
            crawl = _crawl

        for mv in crawl.extensions.middlewares:
            if isinstance(mv, TelnetConsole):
                telnet_middleware = mv

        # 生成唯一标识
        job_id = "{}_{}".format(time.strftime("%Y%m%d_%H%M%S", time.localtime()), random.rand_str(6))

        # 获取日志文件
        log_path = crawl.settings.get("LOG_FILE", None)
        if log_path is not None:
            log_path = os.path.abspath(log_path)
        job_model = SpiderJob(
            job_id=job_id,
            project=self.project,
            spider=spname,
            telnet_username=telnet_middleware.username,
            telnet_password=telnet_middleware.password,
            telnet_host=telnet_middleware.host,
            telnet_port=telnet_middleware.port.port,
            status=SpiderJob.STATUS.RUNNING,
            log_file=log_path,
            job_start_time=datetime.datetime.now()
        )
        job_model.save()
        # 开始运行
        pid = self.__run_spider(process)
        if pid:
            return {
                "job_id": job_id,
                "project": self.project,
                "spider": spname,
                "log_file": log_path,
                "telnet": {
                    "host": telnet_middleware.host,
                    "port": telnet_middleware.port.port,
                    "username": telnet_middleware.username,
                    "password": telnet_middleware.password
                },
                "message": None
            }

    def __run_spider(self, process):
        # TODO 后续尝试将现在fork子进程修改为通过命令行创建爬虫（应该坑很多），目前的方式存在潜在BUG，fork的进程会同时创建一个新的django的socket。需要验证是否存在问题
        pid = os.fork()
        if pid:
            return pid
        os.chdir('/')
        os.umask(0)
        os.setsid()

        _pid = os.fork()
        # with open('/dev/ttys000') as read_null, open('/dev/ttys000', 'w') as write_null:
        with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
            os.dup2(read_null.fileno(), sys.stdin.fileno())
            os.dup2(write_null.fileno(), sys.stdout.fileno())
            os.dup2(write_null.fileno(), sys.stderr.fileno())

        if _pid:
            sys.exit(0)

        sys.stdout.flush()
        sys.stderr.flush()
        process.start()

        return pid

    def list(self):
        try:
            return {
                "success": True,
                "message": None,
                "spiders": self._list(),
                "project": self.project
            }
        except ScrapycwHelperException as e:
            return {
                "success": False,
                "message": e.message
            }

    def _list(self):
        spiders = []
        if self.project is None:
            raise ScrapycwHelperException("Project not find: {}".format(self.param_project))
        crawler_process = CrawlerRunner(self.settings)
        for s in sorted(crawler_process.spider_loader.list()):
            spiders.append(s)
        return spiders
