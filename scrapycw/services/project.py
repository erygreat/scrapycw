from scrapycw.services import BaseService
from scrapycw.utils.response import Response
from scrapycw.helpers.project import ProjectHelper


class Service(BaseService):

    @classmethod
    def list(cls):
        return Response(data=ProjectHelper().list())
