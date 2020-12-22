import os
import sys

from scrapy.utils.conf import closest_scrapy_cfg
from scrapycw.settings import SCRAPY_DEFAULT_PROJECT
from scrapycw.core.exception import ScrapycwException
from scrapycw.core.response import Response
from scrapycw.utils.scrapy_util import get_scrapy_settings
from scrapycw.utils.django_env import init_django_env
init_django_env()
class ScrapycwHelperException(ScrapycwException):
    pass


class Helper:

    param_project = ""
    project = None
    settings = None
    cmdline_settings = None

    def get(self):
        pass

    def get_response(self, **options):
        try:
            return Response(data=self.get(**options))
        except ScrapycwException as e:
            return Response(
                success=False,
                data=e.data,
                code=e.code,
                message=e.message
            )

    def __init__(self, project=SCRAPY_DEFAULT_PROJECT, cmdline_settings=None):
        project_dir = os.path.dirname(closest_scrapy_cfg())
        sys.path.append(project_dir)
        self.param_project = project
        self.cmdline_settings = cmdline_settings
        if cmdline_settings is None:
            cmdline_settings = {}
        self.settings = self.__get_settings(project)
        if self.settings is not None:
            self.settings.setdict(cmdline_settings, priority='cmdline')

    def __get_settings(self, project):
        settings = get_scrapy_settings(project)
        if settings:
            self.project = project
        return settings
