from scrapy.settings import Settings
from scrapy.utils.conf import get_config


def get_scrapy_settings(project):

    config = get_config()

    for _project, setting_dir in config.items('settings'):
        if project == _project:
            settings = Settings()
            settings.setmodule(setting_dir, priority='project')
            return settings
    return None