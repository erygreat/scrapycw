from datetime import datetime, timedelta
import json
import math
import time

from typing import Union
from scrapycw.utils.logger_parser import ScrapyLoggerParser
from scrapycw.utils.telnet import ScrapycwTelnetException, Telnet
from scrapycw.web.api.models import SpiderJob
from scrapycw.core.error_code import ERROR_CODE
from scrapycw.core.exception import ScrapycwException
from scrapycw.helpers import Helper


class ScrapycwJobException(ScrapycwException):
    pass


class JobStatus:
    RUNNING = "running"
    PAUSED = "paused"
    CLOSING = "closing"
    CLOSED = "closed"


class CloseReason:
    """
    SCRAPY 常见的关闭原因，但是由于关闭原因可以由用户自己设置，因此关闭原因并不是只有这几种。
    """
    FINISHED = "finished"
    SHUTDOWN = "shutdown"
    CANCELLED = "cancelled"


class JobListHelper(Helper):

    def __init__(self):
        super().__init__()
    
    def get(self, offset=0, limit=10, spname=None, project=None):
        query = SpiderJob.objects
        if spname:
            query = query.filter(spider=spname, project=project)
        models = query.all()[offset:limit]
        results = []
        for model in models:
            job = JobHelper(job_id=model.job_id)
            results.append({
                "id": model.id,
                "job_id": model.job_id,
                "project": model.project,
                "spider": model.spider,
                "telnet_username": model.telnet_username,
                "telnet_password": model.telnet_password,
                "telnet_host": model.telnet_host,
                "telnet_port": model.telnet_port,
                "status": job.get_status(),
                "closed_reason": job.get_closed_reason(),
                "log_file": model.log_file,
                "job_start_time": model.job_start_time,
                "job_end_time": model.job_end_time,
            })
        return { 
            "count": query.count(),
            "data": results
        }


class JobHelper(Helper):

    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id
        try:
            model = SpiderJob.objects.get(job_id=self.job_id)
        except SpiderJob.DoesNotExist:
            raise ScrapycwJobException(
                code=ERROR_CODE.JOB_ID_NOT_FIND,
                message="Don't have job id: [{}]".format(self.job_id)
            )
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
        # TODO 等到定时任务建立后改为尝试查日志，如果没有查询数据库字段
        self.log_info = self.parse_log()

    def telnet_command(self, command):
        self.telnet.connect()
        result = self.telnet.command(command)
        self.telnet.close()
        return result

    def stop(self):
        self.telnet.connect()
        self.telnet.command("engine.stop()")
        self.telnet.read_util_close()

    def pause(self):
        self.telnet_command("engine.pause()")

    def unpause(self):
        self.telnet_command("engine.unpause()")

    def get_running_stats(self) -> Union[dict, None]:
        try:
            self.telnet.connect()
            self.telnet.command("import json")
            self.telnet.command("import datetime")
            stats = self.telnet.command("stats.get_stats()")
            self.telnet.close()
            import datetime  # noqa # pylint: disable=unused-import
            return eval(stats)
        except ScrapycwTelnetException:
            return None

    def get_stats(self):
        running_stats = self.get_running_stats()
        if running_stats:
            return running_stats
        elif self.log_info:
            return self.log_info.get("spider_stats", None)
        else:
            return None

    def get_running_est(self):
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
        except ScrapycwTelnetException:
            return None

    def parse_log(self):
        log_format = self.settings.get("LOG_FORMAT")
        log_date_format = self.settings.get("LOG_DATEFORMAT")
        parser = ScrapyLoggerParser(
            filename=self.log_path,
            format=log_format,
            log_date_format=log_date_format,
            telnet_password=self.telnet_password
        )
        return parser.execute()
    
    def get_status(self):
        if self.log_info and self.log_info.get("is_close"):
            return JobStatus.CLOSED
        try:
            self.telnet.connect()
            if self.telnet.command("engine.paused"):
                return JobStatus.PAUSED
            elif self.telnet.command("engine.running"):
                return JobStatus.RUNNING
            elif self.telnet.command("slot.closing"):
                return JobStatus.CLOSING
            self.telnet.close()
        except ScrapycwException:
            pass
        return JobStatus.CLOSED
    
    def get_closed_reason(self):
        return self.log_info.get('close_reason') if self.log_info else None

    def get_start_time(self):
        # 开始时间, 运行中连接telent查询，运行完成查询数据库
        try:
            self.telnet.connect()
            start_timestamp = self.telnet.command("engine.start_time")
            start_time = math.floor(float(start_timestamp))
            self.telnet.close()
            return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
        except ScrapycwTelnetException:
            return self.start_time

    def get_runtime(self):
        # 运行时间, 运行中连接telent查询，运行完成查询日志
        try:
            self.telnet.connect()
            start_timestamp = self.telnet.command("engine.start_time")
            runtime = math.floor(time.time() - float(start_timestamp))
            self.telnet.close()
            return timedelta(seconds=runtime)
        except ScrapycwTelnetException:
            return self.log_info.get('continuous_time') if self.log_info else None

    def get_end_time(self):
        return self.log_info.get('end_time') if self.log_info else None

    def get_pages(self):
        stats = self.get_running_stats()
        if stats:
            return stats.get("response_received_count", 0)
        if self.log_info:
            return self.log_info.get("pages")
        else:
            return None

    def get_items(self):
        stats = self.get_running_stats()
        if stats:
            return stats.get("item_scraped_count", 0)
        elif self.log_info:
            return self.log_info.get("items")
        return None
class JobStopHelper(JobHelper):
    def get(self):
        try:
            self.stop()
            return {
                "status": JobStatus.CLOSING
            }
        except ScrapycwTelnetException as e:
            e.data = {
                "status": JobStatus.CLOSED,
            }
            raise e


class JobPauseHelper(JobHelper):
    def get(self):
        try:
            self.pause()
            return {
                "status": JobStatus.PAUSED
            }
        except ScrapycwTelnetException as e:
            e.data = {"status": JobStatus.CLOSED}
            raise e


class JobUnauseHelper(JobHelper):
    def get(self):
        try:
            self.unpause()
            return {
                "status": JobStatus.RUNNING,
            }
        except ScrapycwTelnetException as e:
            e.data = {"status": JobStatus.CLOSED}
            raise e


class JobStatusHelper(JobHelper):

    def get(self, is_parse_settings=True, is_parse_stats=True, is_parse_log=True):
        results ={
            "job_id": self.job_id,
            "project": self.project,
            "spider": self.spider,
            "log_filename": self.log_path,
            "start_time": self.get_start_time(),
            "end_time": self.get_end_time(),
            "closed_reason": self.get_closed_reason(),
            "pages": self.get_pages(),
            "items": self.get_items(),
            "runtime": self.get_runtime(),
            "status": self.get_status()
        }

        if is_parse_settings:
            results["settings"] = self.settings

        if is_parse_stats:
            results["stats"] = self.get_stats()
            results["est"] = self.get_running_est()

        if is_parse_log:
            results["log"] = self.log_info

        return results
