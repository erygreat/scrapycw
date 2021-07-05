import json
import django

from typing import Union
from scrapycw.utils.json_encoder import DatetimeJsonEncoder
from scrapycw.utils.logger_parser import ScrapyLoggerParser
from scrapycw.utils.telnet import ScrapycwTelnetException, Telnet
from scrapycw.web.app.models import SpiderJob
from scrapycw.core.error_code import RESPONSE_CODE
from scrapycw.core.exception import ScrapycwException
from scrapycw.helpers import Helper


class ScrapycwJobException(ScrapycwException):
    pass


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
