import json
import math
import time
import django
from datetime import timedelta

from typing import Union
from scrapycw.utils.logger_parser import ScrapyLoggerParser
from scrapycw.utils.telnet import ScrapycwTelnetException, Telnet
from scrapycw.web.app.models import SpiderJob
from scrapycw.utils.json_encoder import DatetimeJsonEncoder
from scrapycw.core.error_code import RESPONSE_CODE
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
                "closed_reason": job.stats.closed_reason_or_none(),
                "log_file": model.log_file,
                "job_start_time": model.job_start_time,
                "job_end_time": model.job_end_time,
            })
        return { 
            "count": query.count(),
            "data": results
        }
class JobStatsHelper(Helper):

    running_stats = None

    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id
        try:
            model = SpiderJob.objects.get(job_id=self.job_id)
        except SpiderJob.DoesNotExist:
            raise ScrapycwJobException(code=RESPONSE_CODE.JOB_NOT_FIND, message="任务未找到，任务ID: [{}]".format(self.job_id))
        self.job_model = model
        self.telnet_host = model.telnet_host
        self.telnet_port = model.telnet_port
        self.telnet_username = model.telnet_username
        self.telnet_password = model.telnet_password
        self.log_path = model.log_file
        self.telnet = Telnet(self.telnet_host, self.telnet_port, self.telnet_username, self.telnet_password)
        self.log_info = self.parse_log()

    def parse_log(self):
        if not self.log_path:
            return {}

        log_format = self.settings.get("LOG_FORMAT")
        log_date_format = self.settings.get("LOG_DATEFORMAT")
        parser = ScrapyLoggerParser(
            filename=self.log_path,
            format=log_format,
            log_date_format=log_date_format,
            telnet_password=self.telnet_password
        )
        log_info = parser.execute()
        return log_info if log_info else {}

    def is_running(self):
        try:
            return self.telnet.command_once("engine.running")
        except ScrapycwTelnetException:
            return False

    def end_time_or_none(self):
        end_time = self.job_model.end_time
        if end_time:
            return end_time
        return self.log_info.get('end_time', None)

    def closed_reason_or_none(self):
        close_reason = self.job_model.close_reason
        if close_reason:
            return close_reason
        return self.log_info.get('close_reason', None)

    def __stats_db(self) -> Union[dict, None]:
        stats = self.job_model.stats
        if stats:
            return json.loads(stats)
        else:
            return None

    def __stats_log(self) -> Union[dict, None]:
        return self.log_info.get("spider_stats", None)

    def __stats_running(self) -> Union[dict, None]:
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

    def __stats_running_cached(self) -> Union[dict, None]:
        if not self.running_stats:
            self.running_stats = self.__stats_running()
        return self.running_stats

    def spider_stats(self):
        stats = self.__stats_db()
        if stats:
            return stats

        stats = self.__stats_log()
        if stats:
            return stats

        stats = self.__stats_running()
        if stats:
            return stats

        return None

    def pages(self):
        if self.job_model.page_count:
            return self.job_model.page_count

        stats = self.__stats_running_cached()
        if stats:
            return stats.get("response_received_count", 0)

        if self.log_info:
            return self.log_info.get("pages", 0)

        return None

    def items(self):
        if self.job_model.item_count:
            return self.job_model.item_count

        stats = self.__stats_running_cached()
        if stats:
            return stats.get("item_scraped_count", 0)

        elif self.log_info:
            return self.log_info.get("items", 0)
        return None


class JobHelper(Helper):
    class CLOSE_REASON:

        UNKOWN = "unkown"
        FINISHED = "finished"

    DEFAULT_CLOSE_REASON = CLOSE_REASON.UNKOWN

    def __init__(self, job_id):
        super().__init__()
        self.job_id = job_id
        try:
            SpiderJob.objects.get(job_id=self.job_id)
        except SpiderJob.DoesNotExist:
            self.logger.info("没有查询到任务 {}".format(self.job_id))
            raise ScrapycwJobException(code=RESPONSE_CODE.JOB_NOT_FIND, message="任务未找到，任务ID: [{}]".format(self.job_id))
        self.stats = JobStatsHelper(job_id)

    def handler_when_close(self):
        try:
            self.__handler_when_close()
        except Exception as e:
            self.logger.error(e)

    def __handler_when_close(self):
        end_time = self.stats.end_time_or_none()
        if not end_time:
            end_time = django.utils.timezone.now()

        close_reason = self.stats.closed_reason_or_none()
        if not close_reason:
            close_reason = self.DEFAULT_CLOSE_REASON

        spider_stats = self.stats.spider_stats()
        pages = self.stats.pages()
        items = self.stats.items()

        SpiderJob.objects.filter(job_id=self.job_id).update(
            end_time=end_time,
            close_reason=close_reason,
            stats=json.dumps(spider_stats, cls=DatetimeJsonEncoder) if spider_stats else None,
            log_info=json.dumps(self.stats.log_info, cls=DatetimeJsonEncoder) if self.stats.log_info else None,
            page_count=pages,
            item_count=items,
            status=SpiderJob.STATUS.CLOSED,
            updated_time=django.utils.timezone.now()
        )

    def is_running(self):
        return self.stats.is_running()

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
            "end_time": self.stats.end_time_or_none(),
            "closed_reason": self.stats.closed_reason_or_none(),
            "pages": self.stats.pages(),
            "items": self.stats.items(),
            "runtime": self.get_runtime(),
            "status": self.get_status()
        }

        if is_parse_settings:
            results["settings"] = self.settings

        if is_parse_stats:
            results["stats"] = self.stats.spider_stats()
            results["est"] = self.get_running_est()

        if is_parse_log:
            results["log"] = self.log_info

        return results