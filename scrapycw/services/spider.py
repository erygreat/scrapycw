from scrapycw.services import BaseService
from scrapycw.helpers import ScrapycwHelperException
from scrapycw.utils.response import Response
from scrapycw.helpers.spider import SpiderHelper


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
