from scrapycw.web.app.models import SpiderJob
from scrapycw.utils.telnet import ScrapycwTelnetException
from scrapycw.core.exception import ScrapycwException
from scrapycw.services import BaseService
from scrapycw.utils.response import Response
from scrapycw.helpers.job import JobHelper, JobStatsHelper, JobTelnetHelper


class Service(BaseService):

    @classmethod
    def pause(cls, job_id):
        try:
            JobHelper(job_id=job_id).pause()
            return Response(data={
                "status": JobHelper.JOB_STATUS.PAUSED
            })
        except ScrapycwTelnetException as e:
            return Response(
                success=False,
                message=e.message,
                code=e.code,
                data={
                    "status": JobHelper.JOB_STATUS.CLOSED
                }
            )
        except ScrapycwException as e:
            return Response(success=False, message=e.message, code=e.code)

    @classmethod
    def unpause(cls, job_id):
        try:
            JobHelper(job_id=job_id).unpause()
            return Response(data={
                "status": JobHelper.JOB_STATUS.RUNNING
            })
        except ScrapycwTelnetException as e:
            return Response(
                success=False,
                message=e.message,
                code=e.code,
                data={
                    "status": JobHelper.JOB_STATUS.CLOSED
                }
            )
        except ScrapycwException as e:
            return Response(success=False, message=e.message, code=e.code)

    @classmethod
    def stop(cls, job_id):
        try:
            JobHelper(job_id=job_id).stop()
            return Response(data={
                "status": JobHelper.JOB_STATUS.CLOSING
            })
        except ScrapycwTelnetException as e:
            return Response(
                success=False,
                message=e.message,
                code=e.code,
                data={
                    "status": JobHelper.JOB_STATUS.CLOSED
                }
            )
        except ScrapycwException as e:
            return Response(success=False, message=e.message, code=e.code)
    
    @classmethod
    def __status(cls, job_model):
        if job_model.status == SpiderJob.STATUS.CLOSED:
            return JobHelper.JOB_STATUS.CLOSED
        elif job_model.status == SpiderJob.STATUS.RUNNING:
            telnet_helper = JobTelnetHelper(job_model.telnet_host, job_model.telnet_port, job_model.telnet_username, job_model.telnet_password)
            if telnet_helper.is_paused():
                return JobHelper.JOB_STATUS.PAUSED
            elif telnet_helper.is_closing():
                return JobHelper.JOB_STATUS.CLOSING
            else:
                return JobHelper.JOB_STATUS.RUNNING
        else:
            return None

    @classmethod
    def jobs(cls, offset=0, limit=10, spider=None, project=None, status=None, close_reason=None):
        filter_args = {}
        if spider:
            filter_args['spider'] = spider

        if project:
            filter_args['project'] = project

        if status and status == JobHelper.JOB_STATUS.RUNNING:
            filter_args['status'] = SpiderJob.STATUS.RUNNING
        elif status and status == JobHelper.JOB_STATUS.CLOSED:
            filter_args['status'] = SpiderJob.STATUS.CLOSED

        if close_reason:
            filter_args['close_reason'] = close_reason

        query = SpiderJob.objects.filter(**filter_args)

        models = query.order_by("-id").all()[offset: limit]
        count = query.count()

        jobs = [{
            "job_id": model.job_id,
            "project": model.project,
            "spider": model.spider,
            "telnet": {
                "username": model.telnet_username,
                "password": model.telnet_password,
                "host": model.telnet_host,
                "port": model.telnet_port
            },
            "status": cls.__status(model),
            "start_time": model.start_time,
            "end_time": model.end_time,
            "close_reason": model.close_reason,
            "page_count": model.page_count,
            "item_count": model.item_count,
            "created_time": model.created_time,
            "updated_time": model.updated_time,
        } for model in models]
        return Response(data={
            "jobs": jobs,
            "offset": offset,
            "limit": limit,
            "count": count
        })

    @classmethod
    def stats(cls, job_id, is_parse_settings=False, is_parse_log=False, is_parse_stats=False, is_parse_est=False):
        helper = JobStatsHelper(job_id=job_id)
        result = helper.self_stats()
        if is_parse_settings:
            result['settings'] = helper.settings

        if is_parse_log:
            result['log_info'] = helper.log_info

        if is_parse_stats:
            result['stats'] = helper.spider_stats()

        if is_parse_est:
            result['est'] = helper.spider_running_est()

        return Response(data = result)