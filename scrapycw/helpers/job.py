import json
import math

import time

from scrapycw.helpers import Helper
from scrapycw.utils.exception import ScrapycwException
from scrapycw.utils.logger_parser import ScrapyLoggerParser
from scrapycw.utils.telnet import ScrapycwTelnetException, Telnet
from scrapycw.web.api.models import SpiderJob


class ScrapycwJobException(ScrapycwException):
    pass


class JobStatus:
    CLOSED = "closed"
    CLOSING = "closing"
    PAUSED = "paused"
    RUNNING = "running"


class JobHelper(Helper):

    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id
        try:
            model = SpiderJob.objects.get(job_id=self.job_id)
        except SpiderJob.DoesNotExist:
            raise ScrapycwJobException("Don't have job id: [{}]".format(self.job_id))
        self.model = model
        self.telnet_host = model.telnet_host
        self.telnet_port = model.telnet_port
        self.telnet_username = model.telnet_username
        self.telnet_password = model.telnet_password
        self.log_path = model.log_file
        self.project = model.project
        self.spider = model.spider
        self.start_time = model.job_start_time
        self.telnet = Telnet(self.telnet_host, self.telnet_port, self.telnet_username, self.telnet_password)
        self.settings = json.loads(model.settings)

    def telnet_command(self, command):
        self.telnet.connect()
        result = self.telnet.command(command)
        self.telnet.close()
        return result

    def stop(self):
        try:
            self.telnet.connect()
            self.telnet.command("engine.stop()")
            self.telnet.read_util_close()
            return {"success": True, "message": "Finish", "status": JobStatus.CLOSING}
        except ScrapycwTelnetException as e:
            return {"success": False, "message": "Spider is Closed: {}".format(e.message), "status": JobStatus.CLOSED}

    def pause(self):
        try:
            self.telnet_command("engine.pause()")
            return {"success": True, "message": "Finish", "status": JobStatus.PAUSED}
        except ScrapycwTelnetException as e:
            return {"success": False, "message": "Spider is Closed: {}".format(e.message), "status": JobStatus.CLOSED}

    def unpause(self):
        try:
            self.telnet_command("engine.unpause()")
            return {"success": True, "message": "Finish", "status": JobStatus.RUNNING}
        except ScrapycwTelnetException as e:
            return {"success": False, "message": "Spider is Closed: {}".format(e.message), "status": JobStatus.CLOSED}

    def __get_running_stats(self):
        try:
            self.telnet.connect()
            self.telnet.command("import json")
            self.telnet.command("import datetime")
            # stats = self.telnet.command("json.dumps(stats.get_stats(), default=lambda obj: obj.strftime('%Y-%m-%d %H:%M:%S') if isinstance(obj, datetime.datetime) else None)")
            stats = self.telnet.command("stats.get_stats()")
            self.telnet.close()
            import datetime
            return eval(stats)
        except ScrapycwTelnetException as e:
            return None

    def __get_running_est(self):
        try:
            est = {}
            telnet = self.telnet
            telnet.connect()
            telnet.command("from time import time")
            est['time() - engine.start_time'] = telnet.command("time() - engine.start_time")
            est['engine.has_capacity()'] = telnet.command("engine.has_capacity()")
            est['len(engine.downloader.active)'] = telnet.command("len(engine.downloader.active)")
            est['engine.scraper.is_idle()'] = telnet.command("engine.scraper.is_idle()")
            est['engine.spider.name'] = telnet.command("engine.spider.name")
            est['engine.spider_is_idle(engine.spider)'] = telnet.command("engine.spider_is_idle(engine.spider)")
            est['engine.slot.closing'] = telnet.command("engine.slot.closing")
            est['len(engine.slot.inprogress)'] = telnet.command("len(engine.slot.inprogress)")
            est['len(engine.slot.scheduler.dqs or [])'] = telnet.command("len(engine.slot.scheduler.dqs or [])")
            est['len(engine.slot.scheduler.mqs)'] = telnet.command("len(engine.slot.scheduler.mqs)")
            est['len(engine.scraper.slot.queue)'] = telnet.command("len(engine.scraper.slot.queue)")
            est['len(engine.scraper.slot.active)'] = telnet.command("len(engine.scraper.slot.active)")
            est['engine.scraper.slot.active_size'] = telnet.command("engine.scraper.slot.active_size")
            est['engine.scraper.slot.itemproc_size'] = telnet.command("engine.scraper.slot.itemproc_size")
            est['engine.scraper.slot.needs_backout()'] = telnet.command("engine.scraper.slot.needs_backout()")
            telnet.close()
            return est
        except ScrapycwTelnetException as e:
            return None

    def __parse_log(self):
        log_format = self.settings.get("LOG_FORMAT")
        log_date_format = self.settings.get("LOG_DATEFORMAT")
        parser = ScrapyLoggerParser(self.log_path, format=log_format, log_date_format=log_date_format,
                                    telnet_password=self.telnet_password)
        return parser.execute()

    def status(self, parse_settings, parse_stats, parse_log):
        log_info = self.__parse_log()
        running_stats = self.__get_running_stats()
        results = {"base": {
            "job_id": self.job_id,
            "project": self.project,
            "spider": self.spider,
            "log_path": self.log_path,
            "start_time": self.start_time,
            "end_time": log_info.get('end_time'),
            "status": JobStatus.CLOSED if log_info.get("is_close") else None,
            "finish_reason": log_info.get('close_reason'),
            "pages": log_info.get("pages"),
            "items": log_info.get("items"),
            "runtime": log_info.get('continuous_time'),
        }}
        if parse_settings:
            results["settings"] = self.settings

        if parse_stats:
            results["stats"] = running_stats if running_stats else log_info.get("spider_stats", None),

        if parse_stats:
            results["est"] = self.__get_running_est()

        if parse_log:
            results["log"] = log_info
        telnet = self.telnet

        try:
            self.telnet.connect()
            # 开始时间
            start_timestamp = telnet.command("engine.start_time")
            start_time = math.floor(float(start_timestamp))
            start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
            results["base"]["start_time"] = start_time
            # 运行时间
            runtime = time.time() - float(start_timestamp)
            results["base"]["runtime"] = runtime
            # 当前状态
            if telnet.command("engine.paused"):
                results["base"]['status'] = JobStatus.PAUSED
            elif telnet.command("engine.running"):
                results["base"]['status'] = JobStatus.RUNNING
            elif telnet.command("slot.closing"):
                results["base"]['status'] = JobStatus.CLOSING

            telnet.close()
        except ScrapycwTelnetException:
            results['base']['status'] = JobStatus.CLOSED

        return results
