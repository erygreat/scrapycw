import datetime
import os
import sys
import time

from scrapy.extensions.telnet import TelnetConsole

from scrapycw.helpers import Helper, ScrapycwHelperException
from scrapycw.scrapyrewrite.crawler import CustomCrawlerProcess
from scrapycw.settings import SCRAPY_DEFAULT_PROJECT
from scrapycw.utils import random
from scrapycw.web.api.models import SpiderJob


class CrawlHelper(Helper):

    def __init__(self, spname, spargs=None, project=SCRAPY_DEFAULT_PROJECT, cmdline_settings=None):
        if spargs is None:
            spargs = {}
        self.spname = spname
        self.spargs = spargs
        super().__init__(project=project, cmdline_settings=cmdline_settings)

    def get_value(self):
        if self.spname is None:
            raise ScrapycwHelperException("Spider not null")
        if self.project is None:
            raise ScrapycwHelperException("Project not find: {}".format(self.param_project))
        process = CustomCrawlerProcess(self.settings)
        try:
            process.crawl(self.spname, **self.spargs)
        except KeyError as e:
            raise ScrapycwHelperException("Spider not found: {}".format(self.spname))

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
            spider=self.spname,
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
        pid = self.__run_spider(process, job_id)
        if pid:
            return {
                "job_id": job_id,
                "project": self.project,
                "spider": self.spname,
                "log_file": log_path,
                "telnet": {
                    "host": telnet_middleware.host,
                    "port": telnet_middleware.port.port,
                    "username": telnet_middleware.username,
                    "password": telnet_middleware.password
                }
            }

    def get_json(self):
        try:
            return self.get_value()
        except ScrapycwHelperException as e:
            return {
                "success": False,
                "message": e.message,
                "project": self.project,
                "spider": self.spname,
            }

    def __run_spider(self, process, job_id):
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
