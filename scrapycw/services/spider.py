from scrapycw.web.app.models import SpiderJob
from scrapycw.utils.telnet import ScrapycwTelnetException
from scrapycw.core.exception import ScrapycwException
from scrapycw.services import BaseService
from scrapycw.helpers import ScrapycwHelperException
from scrapycw.utils.response import Response
from scrapycw.helpers.spider import SpiderHelper
from scrapycw.helpers.job import JobHelper, JobTelnetHelper


class Service(BaseService):

    @classmethod
    def list(cls, project):
        if project:
            try:
                return Response(data=SpiderHelper(project=project).list())
            except ScrapycwHelperException as e:
                return Response(success=False, message=e.message, code=e.code)
        else:
            return Response(data=SpiderHelper().all_list())

    @classmethod
    def run(cls, project, spname, cmdline_settings, spargs):
        try:
            data = SpiderHelper(project=project, cmdline_settings=cmdline_settings).crawl(spname=spname, spargs=spargs)
            return Response(data=data)
        except ScrapycwException as e:
            return Response(success=False, message=e.message, code=e.code)

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
    def job_status(cls, job_id, job_model_status):
        if job_model_status == SpiderJob.STATUS.CLOSED:
            return JobHelper.JOB_STATUS.CLOSED
        elif job_model_status == SpiderJob.STATUS.RUNNING:
            return JobHelper.JOB_STATUS.PAUSED if JobTelnetHelper(job_id).is_paused() else JobHelper.JOB_STATUS.RUNNING
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
            "status": cls.job_status(model.job_id, model.status),
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
