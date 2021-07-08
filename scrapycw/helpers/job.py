import json
import django

from typing import Union
from scrapycw.utils.json_encoder import DatetimeJsonEncoder
from scrapycw.utils.logger_parser import ScrapyLoggerParser
from scrapycw.utils.telnet import ScrapycwTelnetException, Telnet
from scrapycw.utils.scrapycw import current_time
from scrapycw.web.app.models import SpiderJob
from scrapycw.core.error_code import RESPONSE_CODE
from scrapycw.core.exception import ScrapycwException
from scrapycw.helpers import Helper


class ScrapycwJobException(ScrapycwException):
    pass


class JobTelnetHelper(Helper):

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.telnet = Telnet(self.host, self.port, self.username, self.password)

    def is_running(self):
        try:
            return self.telnet.command_once("engine.running")
        except ScrapycwTelnetException:
            return False

    def is_paused(self):
        try:
            return self.telnet.command_once("engine.paused")
        except ScrapycwTelnetException:
            return False

    def is_closing(self):
        try:
            return self.telnet.command_once("slot.closing")
        except ScrapycwTelnetException:
            return False


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
        self.project = model.project
        self.settings = json.loads(model.settings)
        self.spider = model.spider
        self.telnet_host = model.telnet_host
        self.telnet_port = model.telnet_port
        self.telnet_username = model.telnet_username
        self.telnet_password = model.telnet_password
        self.telnet_helper = JobTelnetHelper(self.telnet_host, self.telnet_port, self.telnet_username, self.telnet_password)
        self.telnet = self.telnet_helper.telnet
        self.log_path = model.log_file
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
        return self.telnet_helper.is_running()

    def is_paused(self):
        return self.telnet_helper.is_paused()

    def is_closing(self):
        return self.telnet_helper.is_closing()

    def start_time(self):
        return self.job_model.start_time

    def end_time_or_none(self):
        end_time = self.job_model.end_time
        if end_time:
            return end_time
        return self.log_info.get('end_time', None)

    def runtime(self):
        # 如果日志中有运行时间，则直接用日志中的
        runtime = self.log_info.get('continuous_time', None)
        if runtime:
            return runtime
        # 如果日志中没有运行时间，但是已经结束，则用结束时间减去开始时间
        end_time = self.end_time_or_none()
        start_time = self.start_time()
        if end_time:
            return end_time - start_time

        # 如果还没有结束，则用当前时间减去开始时间
        return current_time() - start_time

    def status(self):
        if self.job_model.status == SpiderJob.STATUS.CLOSED:
            return JobHelper.JOB_STATUS.CLOSED

        if self.is_closing():
            return JobHelper.JOB_STATUS.CLOSING

        if self.is_paused():
            return JobHelper.JOB_STATUS.PAUSED

        if self.is_running():
            return JobHelper.JOB_STATUS.RUNNING

        return JobHelper.JOB_STATUS.CLOSED

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

    def spider_running_est(self):
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

    def self_stats(self):
        return {
            "job_id": self.job_id,
            "project": self.project,
            "spider": self.spider,
            "log_path": self.log_path,
            "start_time": self.start_time(),
            "end_time": self.end_time_or_none(),
            "closed_reason": self.closed_reason_or_none(),
            "pages": self.pages(),
            "items": self.items(),
            "runtime": self.runtime(),
            "status": self.status(),
        }


class JobHelper(Helper):
    class CLOSE_REASON:

        UNKNOWN = "unknown"
        FINISHED = "finished"
        SHUTDOWN = "shutdown"

    class JOB_STATUS:

        PAUSED = "paused"
        CLOSED = "closed"
        RUNNING = "running"
        CLOSING = "closing"

    DEFAULT_CLOSE_REASON = CLOSE_REASON.UNKNOWN

    def __init__(self, job_id):
        self.job_id = job_id
        try:
            model = SpiderJob.objects.get(job_id=self.job_id)
        except SpiderJob.DoesNotExist:
            self.logger.info("没有查询到任务 {}".format(self.job_id))
            raise ScrapycwJobException(code=RESPONSE_CODE.JOB_NOT_FIND, message="任务未找到，任务ID: [{}]".format(self.job_id))
        self.telnet_host = model.telnet_host
        self.telnet_port = model.telnet_port
        self.telnet_username = model.telnet_username
        self.telnet_password = model.telnet_password
        self.telnet = JobTelnetHelper(self.telnet_host, self.telnet_port, self.telnet_username, self.telnet_password).telnet
        self.stats = JobStatsHelper(job_id)

    def handler_when_close(self):
        try:
            self.stats = JobStatsHelper(self.job_id)
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

    def stop(self):
        self.telnet.command_once("engine.stop()")

    def unpause(self):
        self.telnet.command_once("engine.unpause()")

    def pause(self):
        self.telnet.command_once("engine.pause()")
