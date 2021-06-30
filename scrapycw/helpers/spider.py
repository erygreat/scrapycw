import json
import os
import nanoid
import time

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.extensions.telnet import TelnetConsole

from scrapycw.utils.scrapycw import get_scrapy_settings
from scrapycw.utils import process
from scrapycw.utils.json_encoder import ScrapySettingEncoder
from scrapycw.helpers import Helper, ScrapycwHelperException
from scrapycw.helpers.project import ProjectHelper
from scrapycw.core.error_code import RESPONSE_CODE
from scrapycw.web.app.models import SpiderJob

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
            "cmdline_settings": self.cmdline_settings,
        }
        spider_pid, data = process.run_in_daemon(SpiderHelper.run_spider, args=run_spider_args, has_return_data=True)
        return self.__handler_spider_data(data, spname, spargs, spider_pid)

    def __handler_spider_data(self, data, spname, spargs, spider_pid):
        job_id = data['job_id']
        log_file = data['log_file']
        telnet_username = data['telnet_username']
        telnet_password = data['telnet_password']
        telnet_host = data['telnet_host']
        telnet_port = data['telnet_port']
        log_file = data['log_file']
        start_time = data['start_time']
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        settings = data['settings']
        self.__save_job(job_id, self.project, spname, spargs, self.cmdline_settings, telnet_username, telnet_password, telnet_host, telnet_port, log_file, start_time, settings)
        # self.__register_job_listen(job_id, spider_pid)
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

    def __save_job(self, job_id, project, spname, spargs, cmdline_settings, telnet_username, telnet_password, telnet_host, telnet_port, log_file, start_time, settings):
        job_model = SpiderJob(
            job_id=job_id,
            project=project,
            spider=spname,
            spargs=spargs,
            cmdline_settings=cmdline_settings,
            telnet_username=telnet_username,
            telnet_password=telnet_password,
            telnet_host=telnet_host,
            telnet_port=telnet_port,
            status=SpiderJob.STATUS.RUNNING,
            log_file=log_file,
            start_time=start_time,
            settings=settings,
        )
        job_model.save()

    # def __register_job_listen(self, job_id, spider_pid):
    #     _, data = process.run_in_daemon(SpiderHelper.listen_job, args={ "job_id": job_id, "pid": spider_pid }, has_return_data=True)
    #     print(data)

    # @staticmethod
    # def listen_job(args, callback=None):
    #     job_id = args['job_id']
    #     pid = args['pid']
        # 获取进程创建时间，用来做后续是否是对应进程时比对
        # spider_process_create_time = process.create_time()
        # if spider_process_create_time:

        # callback({})
        # model = SpiderJob.objects.get(job_id=job_id)
        # callback({"success": is_running(pid), "job_name": model.spider})

        # while True:
        #     if not is_running(pid):
        #         break
        #     else:
        #         time.sleep(SPIDER_LISTEN_LOOP_TIME)

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
            raise ScrapycwHelperException(code=RESPONSE_CODE.SPIDER_NOT_FIND, message="爬虫没有找到: {}".format(spname))

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
