from scrapy.settings import Settings
from scrapy.utils.conf import get_config


class ScrapycwHelperException(Exception):

    def __init__(self, message):
        self.message = message

class Helper:

    param_project = ""
    project = None
    settings = None

    def get_value(self):
        pass

    def get_json(self):
        pass

    def __init__(self, project="default", cmdline_settings=None):
        if cmdline_settings is None:
            cmdline_settings = {}
        self.param_project = project
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
