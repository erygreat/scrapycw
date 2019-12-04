import json

from django.http import HttpResponse

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
