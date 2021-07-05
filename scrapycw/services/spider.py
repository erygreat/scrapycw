from scrapycw.core.exception import ScrapycwException
from scrapycw.services import BaseService
from scrapycw.helpers import ScrapycwHelperException
from scrapycw.utils.response import Response
from scrapycw.helpers.spider import SpiderHelper
from scrapycw.helpers.job import JobHelper



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
            return Response(data=JobHelper(job_id=job_id).pause())
        except ScrapycwException as e:
            return Response(success=False, message=e.message, code=e.code, data=e.data)