import os
import sys

from scrapy.settings import Settings
from scrapy.utils.conf import get_config, closest_scrapy_cfg
from scrapycw.settings import SCRAPY_DEFAULT_PROJECT
from scrapycw.utils.exception import ScrapycwException


class ScrapycwHelperException(ScrapycwException):
    pass


class Helper:

    param_project = ""
    project = None
    settings = None

    def get_value(self):
        pass

    def get_json(self):
        pass

    def __init__(self, project=SCRAPY_DEFAULT_PROJECT, cmdline_settings=None):
        project_dir = os.path.dirname(closest_scrapy_cfg())
        sys.path.append(project_dir)
        self.param_project = project
        if cmdline_settings is None:
            cmdline_settings = {}
        self.settings = self.__get_settings(project)
        if self.settings is not None:
            self.settings.setdict(cmdline_settings, priority='cmdline')

    def __get_settings(self, project):
        config = get_config()
        for _project, dir in config.items('settings'):
            if project == _project:
                self.project = project
                settings = Settings()
                settings.setmodule(dir, priority='project')
                return settings
        return None
