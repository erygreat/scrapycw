import os
import sys

from scrapy.utils.conf import closest_scrapy_cfg
from scrapycw.settings import SCRAPY_DEFAULT_PROJECT
from scrapycw.core.exception import ScrapycwException
from scrapycw.utils.scrapycw import get_scrapy_settings
from scrapycw.core.scrapycw_object import ScrapycwObject


class ScrapycwHelperException(ScrapycwException):
    pass


class Helper(ScrapycwObject):
    pass


class SettingsHelper(Helper):

    param_project = ""
    project = None
    settings = None
    cmdline_settings = None

    def __init__(self, project=SCRAPY_DEFAULT_PROJECT, cmdline_settings=None):
        project_dir = os.path.dirname(closest_scrapy_cfg())
        sys.path.append(project_dir)
        self.param_project = project
        self.cmdline_settings = cmdline_settings
        if cmdline_settings is None:
            cmdline_settings = {}
        self.settings = self._get_settings(project)
        if self.settings:
            self.settings.setdict(cmdline_settings, priority='cmdline')

    def _get_settings(self, project):
        settings = get_scrapy_settings(project)
        if settings:
            self.project = project
        return settings
