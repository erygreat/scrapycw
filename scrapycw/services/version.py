from scrapycw.utils.response import Response
from scrapycw.helpers.version import version


class Service:
    @classmethod
    def version(cls):
        return Response(data=version())
