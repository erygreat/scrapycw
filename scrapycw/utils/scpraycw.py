import os
import django
from scrapy.settings import Settings
from scrapy.utils.conf import get_config


def get_root_dir():
    return os.path.dirname(os.path.dirname(__file__))


def init_django_env():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapycw.web.settings')
    django.setup()


def get_scrapy_settings(project):
    config = get_config()
    for _project, setting_dir in config.items('settings'):
        if project == _project:
            settings = Settings()
            settings.setmodule(setting_dir, priority='project')
            return settings
    return None