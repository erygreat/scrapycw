import os
import django


def get_root_dir():
    return os.path.dirname(os.path.dirname(__file__))


def init_django_env():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapycw.web.settings')
    django.setup()
