import json

from django.http import HttpResponse

from scrapycw.helpers.job import JobHelper
from scrapycw.helpers.project import ProjectHelper
from scrapycw.helpers.spider import SpiderHelper
from scrapycw.settings import SCRAPY_DEFAULT_PROJECT


def projects(request):
    result = ProjectHelper().list()
    return HttpResponse(json.dumps(result), content_type='application/json')


def spiders(request):
    project = request.GET.get("project", SCRAPY_DEFAULT_PROJECT)
    result = SpiderHelper(project=project).list()
    return HttpResponse(json.dumps(result), content_type='application/json')

def all_spiders(request):
    result = ProjectHelper().list()
    spider_result = []
    projects = result['projects']
    for project in projects:
        spider_obj = SpiderHelper(project=project).list()
        spider_result.append({
            "project": project,
            "spiders": spider_obj['spiders']
        })
    data = {
        "success": True,
        "message": None,
        "data": spider_result
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

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
