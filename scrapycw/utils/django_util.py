import os
import django

def init_django_env():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapycw.web.settings')
    django.setup()
