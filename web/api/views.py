import json

from django.http import HttpResponse

from scrapycw.helpers.crawl import CrawlHelper
from scrapycw.helpers.project import ProjectListHelper
from scrapycw.helpers.spider import SpiderListHelper
from scrapycw.settings import SCRAPY_DEFAULT_PROJECT


def project_list(request):
    result = ProjectListHelper().get_json()
    return HttpResponse(json.dumps(result), content_type='application/json')


def spider_list(request):
    project = request.GET.get("project", SCRAPY_DEFAULT_PROJECT)
    result = SpiderListHelper(project=project).get_json()
    return HttpResponse(json.dumps(result), content_type='application/json')


def crawl(request):
    project = request.GET.get("project", SCRAPY_DEFAULT_PROJECT)
    spname = request.GET.get("spider")
    body = json.loads(request.body)
    spargs = body.get("spargs")
    settings = body.get("settings")
    result = CrawlHelper(spname=spname, project=project, spargs=spargs, cmdline_settings=settings).get_json()
    return HttpResponse(json.dumps(result), content_type='application/json')
