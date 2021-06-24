import datetime
import json
import math
import os
import platform
import subprocess
import sys
import time
from scrapy.crawler import CrawlerRunner
from scrapy.extensions.telnet import TelnetConsole
from scrapycw.helpers import Helper, ScrapycwHelperException
from scrapycw.core.error_code import RESPONSE_CODE
from scrapycw.scrapyrewrite.crawler import CustomCrawlerProcess
from scrapycw.scripts.windows_run_spider import get_spider_windows_run_script_path
from scrapycw.settings import RUN_SPIDER_TIMEOUT, SPIDER_RUN_CACHE_DIR
from scrapycw.utils import rand
from scrapycw.utils.json_encoder import DatetimeJsonEncoder, ScrapySettingEncoder
from scrapycw.web.api.models import SpiderJob
from scrapycw.helpers.project import ProjectHelper
from scrapy.crawler import CrawlerRunner
from scrapycw.helpers import Helper, ScrapycwHelperException
from scrapycw.core.error_code import RESPONSE_CODE

class SpiderListHelper(Helper):

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

class SpiderRunnerHelper(Helper):
    
    def get(self, spname, spargs=None):
        try:
            return self._crawl(spname, spargs)
        except ScrapycwHelperException as e:
            e.data = {
                "project": self.project,
                "spider": spname,
            }
            raise e

    def _crawl(self, spname, spargs=None):
        if spname is None:
            raise ScrapycwHelperException(
                code=RESPONSE_CODE.NOT_ENTER_SPIDER_NAME,
                message="请输入爬虫名称！"
            )

        if self.project is None:
            raise ScrapycwHelperException(
                code=RESPONSE_CODE.PROJECT_NOT_FIND,
                message="Project not find: {}".format(self.param_project)
            )
        return self._run(spname, spargs)

    def get_job_id(self):
        return "{}_{}".format(time.strftime("%Y%m%d_%H%M%S", time.localtime()), rand.rand_str(6))

    def _run(self, spname, spargs=None):
        job_id = self.get_job_id()
        if platform.system() == "Linux" or platform.system() == "Darwin":
            runner = LinuxSpiderRunner(spname, spargs, self.project, self.settings, job_id, self.cmdline_settings)
        elif platform.system() == "Windows":
            runner = WindowsSpiderRunner(spname, spargs, self.project, self.settings, job_id, self.cmdline_settings)
        else:
            raise ScrapycwHelperException(
                code=RESPONSE_CODE.NOT_SUPPORT_SYSTEM,
                message="未知操作系统: {}".format(platform.system())
            )
        return runner.run()
class SpiderRunner():

    def __init__(self, spname, spargs, project, settings, job_id, cmdline_settings):
        self.spname = spname
        self.spargs = spargs
        self.settings = settings
        self.cmdline_settings = cmdline_settings
        self.project = project
        self.job_id = job_id

    def get_spider_process(self):
        process = CustomCrawlerProcess(self.settings)
        try:
            process.crawl(self.spname, **self.spargs)
        except KeyError:
            raise ScrapycwHelperException( code=RESPONSE_CODE.SPIDER_NOT_FIND, message="Spider not found: {}".format(self.spname))

        telnet_middleware = None
        crawl = None
        for _crawl in process.crawlers:
            crawl = _crawl
        if not crawl:
            raise ScrapycwHelperException(
                code=RESPONSE_CODE.SPIDER_CODE_HAVE_BUG,
                message="爬虫启动失败，请检查爬虫代码是否正确，引入的依赖文件是否存在!"
            )

        for mv in crawl.extensions.middlewares:
            if isinstance(mv, TelnetConsole):
                telnet_middleware = mv

        # 获取日志文件
        log_path = crawl.settings.get("LOG_FILE", None)
        if log_path is not None:
            log_path = os.path.abspath(log_path)
        settings_str = json.dumps({key: value for key, value in self.settings.items()}, cls=ScrapySettingEncoder)
        return process, {
            "job_id": self.job_id,
            "spider": self.spname,
            "telnet_username": telnet_middleware.username,
            "telnet_password": telnet_middleware.password,
            "telnet_host": telnet_middleware.host,
            "telnet_port": telnet_middleware.port.port,
            "status": SpiderJob.STATUS.RUNNING,
            "settings": settings_str,
            "log_file": log_path,
            "job_start_time": datetime.datetime.now(),
        }

    def start_process(self, process):
        if process:
            process.start()

    def handler_spider_info(self, run_info):
        job_id = run_info['job_id']
        spname = run_info['spider']
        log_file = run_info['log_file']
        telnet_username = run_info['telnet_username']
        telnet_password = run_info['telnet_password']
        telnet_host = run_info['telnet_host']
        telnet_port = run_info['telnet_port']
        job_model = SpiderJob(
            job_id=job_id,
            project=self.project,
            spider=spname,
            telnet_username=telnet_username,
            telnet_password=telnet_password,
            telnet_host=telnet_host,
            telnet_port=telnet_port,
            status=SpiderJob.STATUS.RUNNING,
            settings=run_info['settings'],
            log_file=log_file,
            job_start_time=datetime.datetime.now()
        )
        job_model.save()
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

class LinuxSpiderRunner(SpiderRunner):

    def run(self):
        process, spider_info = self.get_spider_process()
        pid = self.__start_process(process)
        if pid and spider_info:
            return self.handler_spider_info(spider_info)
        else:
            return None
    
    def __start_process(self, process):
        pid = os.fork()
        if pid:
            return pid
        os.chdir('/')
        os.umask(0)
        os.setsid()

        _pid = os.fork()
        with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
            os.dup2(read_null.fileno(), sys.stdin.fileno())
            os.dup2(write_null.fileno(), sys.stdout.fileno())
            os.dup2(write_null.fileno(), sys.stderr.fileno())

        if _pid:
            sys.exit(0)
        self.start_process(process)
        return pid

class WindowsSpiderRunner(SpiderRunner):

    def run(self):
        cmd = ['python', get_spider_windows_run_script_path(), "--spname", self.spname, "--job_id", self.job_id, "--spargs", json.dumps(self.spargs), "--settings", json.dumps(self.cmdline_settings), "--project", self.project]
        subprocess.Popen(cmd)
        spider_info = self.__get_spider_info()
        return self.handler_spider_info(spider_info)

    def __get_job_id_filename(self):
        filename = os.path.join(SPIDER_RUN_CACHE_DIR, "{}.txt".format(self.job_id))
        if not os.path.exists(SPIDER_RUN_CACHE_DIR):
            os.makedirs(SPIDER_RUN_CACHE_DIR)
        return filename
        
    def __get_spider_info(self, timeout=RUN_SPIDER_TIMEOUT):
        for _ in range(math.floor(timeout / 100)):
            filename = self.__get_job_id_filename()
            if os.path.exists(filename):
                with open(filename) as file:
                    lines = file.read()
                    content = json.loads(lines)
                    if not content['success']:
                        raise ScrapycwHelperException(message=content['data']['message'], code=content['data']['code'], data=content['data']['data'])
                    else:
                        return content['data']
            time.sleep(0.1)
        raise ScrapycwHelperException(message="启动爬虫超时", code=RESPONSE_CODE.SPIDER_RUN_TIMEOUT)

    def start_spider(self):
        process = None
        try:
            process, spider_info = self.get_spider_process()
            info = { "success": True, "data": spider_info }
        except Exception as e:
            info = { "success": False, "data": e.__dict__ }
        filename = self.__get_job_id_filename()
        with open(filename,'w') as f:
            f.write(json.dumps(info,  cls=DatetimeJsonEncoder))
        self.start_process(process)
