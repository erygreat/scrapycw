from datetime import datetime
import os
import django
from scrapy.settings import Settings
from scrapy.utils.conf import get_config
from scrapycw.settings import HANDLE_LOG_USE_TIMEZONE


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


def dict_from_class(cls, baseClass=object):
    class A(baseClass):
        pass
    _excluded_keys = set(A.__dict__.keys())
    return dict((key, value) for (key, value) in cls.__dict__.items() if key not in _excluded_keys)


def value_from_class(cls, baseClass=object):
    return [x for x in dict_from_class(cls, baseClass).values()]


def current_time():
    if HANDLE_LOG_USE_TIMEZONE:
        return datetime.now()
    else:
        return datetime.utcnow()
