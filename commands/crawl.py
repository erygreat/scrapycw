import datetime
import os
import sys
import time

from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import UsageError
from scrapy.extensions.telnet import TelnetConsole
from scrapy.settings import Settings
from scrapy.utils.conf import get_config, arglist_to_dict

from scrapycw.commands import ScrapycwCommand
from scrapycw.helpers import ScrapycwHelperException
from scrapycw.utils import random
from scrapycw.web.api.models import SpiderJob


class Command(ScrapycwCommand):

    can_crawl_log_print = True

    def run(self, args, opts):
        settings = self.__get_settings(opts.project)
        if settings is None:
            raise ScrapycwHelperException("Project not find: {}".format(opts.project))
        spname = args[0]

        settings.setdict(self.cmdline_settings, priority='cmdline')
        process = CrawlerProcess(settings)
        process.crawl(spname, **opts.spargs)

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
        pid = self.run_spider(process)
        log_path = os.path.abspath(crawl.settings.get("LOG_FILE"))
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
                }
            }

    def run_spider(self, process):
        pid = os.fork()
        if pid:
            return pid

        os.chdir('/')
        os.umask(0)
        os.setsid()

        _pid = os.fork()
        if _pid:
            sys.exit(0)

        sys.stdout.flush()
        sys.stderr.flush()

        with open('/dev/null') as read_null, open('/dev/null', 'w') as write_null:
            os.dup2(read_null.fileno(), sys.stdin.fileno())
            os.dup2(write_null.fileno(), sys.stdout.fileno())
            os.dup2(write_null.fileno(), sys.stderr.fileno())
        process.start()
        return pid

    def short_desc(self):
        return "Run Spider"

    def long_desc(self):
        return "Run Spider"

    def syntax(self):
        return "<spider-name> [option] "

    def add_options(self, parser):
        ScrapycwCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set spider argument (may be repeated)")

    def process_options(self, args, opts):
        ScrapycwCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)

    def __get_settings(self, project):
        config = get_config()
        for _project, dir in config.items('settings'):
            if project == _project:
                self.project = project
                settings = Settings()
                settings.setmodule(dir, priority='project')
                return settings
        return None
