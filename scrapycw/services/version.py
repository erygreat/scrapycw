from scrapycw.services import BaseService
from scrapycw.utils.response import Response
from scrapycw.helpers.version import version


class Service(BaseService):

    @classmethod
    def version(cls):
        return Response(data=version())
