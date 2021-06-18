import json

from django.http import HttpResponse

from scrapycw.helpers.job import JobHelper
from scrapycw.helpers.project import ProjectHelper
from scrapycw.helpers.spider import SpiderHelper
from scrapycw.settings import SCRAPY_DEFAULT_PROJECT


def project_list(request):
    result = ProjectHelper().list()
    return HttpResponse(json.dumps(result), content_type='application/json')


def spider_list(request):
    project = request.GET.get("project", SCRAPY_DEFAULT_PROJECT)
    result = SpiderHelper(project=project).list()
    return HttpResponse(json.dumps(result), content_type='application/json')


def crawl(request):
    project = request.GET.get("project", SCRAPY_DEFAULT_PROJECT)
    spname = request.GET.get("spider")
    try:
        body = json.loads(request.body)
        spargs = body.get("spargs")
        settings = body.get("settings")
    except:
        spargs = {}
        settings = {}

    result = SpiderHelper(project=project, cmdline_settings=settings).crawl(spname=spname, spargs=spargs)
    return HttpResponse(json.dumps(result), content_type='application/json')


def stop(request):
    job_id = request.GET.get("job_id")
    result = JobHelper(job_id=job_id).stop()
    return HttpResponse(json.dumps(result), content_type='application/json')


def pause(request):
    job_id = request.GET.get("job_id")
    result = JobHelper(job_id=job_id).pause()
    return HttpResponse(json.dumps(result), content_type='application/json')


def unpause(request):
    job_id = request.GET.get("job_id")
    result = JobHelper(job_id=job_id).unpause()
    return HttpResponse(json.dumps(result), content_type='application/json')


def ping(request):
    return HttpResponse(json.dumps({"message": "ok"}), content_type="application/json")