import json
import os
from scrapycw.settings import SPIDER_LISTEN_LOOP_TIME
from scrapycw.helpers.job import JobHelper
import nanoid
import time

from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.extensions.telnet import TelnetConsole

from scrapycw.utils.scrapycw import get_scrapy_settings
from scrapycw.utils import process
from scrapycw.utils.json_encoder import ScrapySettingEncoder
from scrapycw.helpers import ScrapycwHelperException, SettingsHelper
from scrapycw.helpers.project import ProjectHelper
from scrapycw.core.error_code import RESPONSE_CODE
from scrapycw.web.app.models import SpiderJob


class SpiderHelper(SettingsHelper):

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
        self.__register_job_listen(job_id, spider_pid)
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

    def __register_job_listen(self, job_id, spider_pid):
        process.run_in_daemon(SpiderHelper.listen_job, args={
            "job_id": job_id,
            "pid": spider_pid
        })

    @staticmethod
    def listen_job(args):
        job_id = args['job_id']
        pid = args['pid']
        SpiderHelper.logger.info("[监听爬虫]: 任务ID: {}, PID: {}".format(job_id, pid))

        # 获取进程创建时间，用来做后续是否是对应进程时进行对比
        process_create_time = process.create_time(pid)
        job_helper = JobHelper(job_id)
        if not process_create_time:
            SpiderHelper.logger.info("[爬虫已关闭]: 没有找到爬虫进程，任务ID: {}, PID: {}".format(job_id, pid))
            return job_helper.handler_when_close()

        # 防止启动的进程的ID不是这个 job 的
        if not job_helper.stats.is_running():
            SpiderHelper.logger.info("[爬虫已关闭]: 无法连接爬虫Telnet或Telnet显示已关闭，任务ID: {}, PID: {}".format(job_id, pid))
            return job_helper.handler_when_close()

        while True:
            if process.is_running(pid, process_create_time):
                SpiderHelper.logger.debug("[爬虫正在运行中]: 任务ID: {}, PID: {}".format(job_id, pid))
                time.sleep(SPIDER_LISTEN_LOOP_TIME)
            else:
                SpiderHelper.logger.info("[爬虫已关闭]: 任务ID: {}, PID: {}".format(job_id, pid))
                return job_helper.handler_when_close()

    @staticmethod
    def run_spider(args, callback=None):
        project = args['project']
        cmdline_settings = args['cmdline_settings']
        spname = args['spname']
        spargs = args['spargs']
        SpiderHelper.logger.info("[启动爬虫]: 项目名称: {}, 爬虫名称: {}".format(project, spname))

        # 获取 Settings
        settings = get_scrapy_settings(project)
        if settings:
            settings.setdict(cmdline_settings, priority='cmdline')
        if not settings:
            raise ScrapycwHelperException(code=RESPONSE_CODE.PROJECT_NOT_FIND, message="[爬虫启动失败]: 没有项目[{}]".format(project))

        # 获取爬虫进程
        process = CrawlerProcess(settings)
        try:
            process.crawl(spname, **spargs)
        except KeyError:
            raise ScrapycwHelperException(code=RESPONSE_CODE.SPIDER_NOT_FIND, message="[爬虫启动失败]: 爬虫没有找到: {}".format(spname))

        crawl = None
        for _crawl in process.crawlers:
            crawl = _crawl
        if not crawl:
            SpiderHelper.logger.warning("[爬虫启动失败]: 项目名称: {}, 爬虫名称: {}, 请检查爬虫代码是否正确，引入的依赖文件是否存在!".format(project, spname))
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
