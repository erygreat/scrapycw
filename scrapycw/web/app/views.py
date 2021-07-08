import json

from django.http import HttpResponse

# from scrapycw.helpers.job import JobStopHelper, JobPauseHelper, JobUnauseHelper
from scrapycw.services.project import Service as ProjectService
# from scrapycw.services.spider import Service as SpiderService
# from scrapycw.helpers.spider import SpiderListHelper
# from scrapycw.settings import SCRAPY_DEFAULT_PROJECT
# from scrapycw.utils.response import Response


def projects(request):
    result = ProjectService.list()
    return HttpResponse(json.dumps(result), content_type='application/json')


# def spiders(request):
#     project = request.GET.get("project", SCRAPY_DEFAULT_PROJECT)
#     result = SpiderListHelper(project=project).get_response()
#     return HttpResponse(json.dumps(result), content_type='application/json')


# def all_spiders(request):
#     result = ProjectListHelper().get()
#     spider_result = []
#     projects = result['projects']
#     for project in projects:
#         spider_obj = SpiderListHelper(project=project).get()
#         spider_result.append({
#             "project": project,
#             "spiders": spider_obj['spiders']
#         })
#     data = Response(data=spider_result)
#     return HttpResponse(json.dumps(data), content_type='application/json')


# def crawl(request):
#     project = request.GET.get("project", SCRAPY_DEFAULT_PROJECT)
#     spname = request.GET.get("spider")
#     try:
#         body = json.loads(request.body)
#         spargs = body.get("spargs")
#         settings = body.get("settings")
#     except Exception:
#         pass

#     if not spargs:
#         spargs = {}
#     if not settings:
#         settings = {}

#     result = SpiderRunnerHelper(project=project, cmdline_settings=settings).get_response(spname=spname, spargs=spargs)
#     return HttpResponse(json.dumps(result), content_type='application/json')


# def stop(request):
#     job_id = request.GET.get("job_id")
#     result = JobStopHelper(job_id=job_id).stop()
#     return HttpResponse(json.dumps(result), content_type='application/json')


# def pause(request):
#     job_id = request.GET.get("job_id")
#     result = JobPauseHelper(job_id=job_id).pause()
#     return HttpResponse(json.dumps(result), content_type='application/json')


# def unpause(request):
#     job_id = request.GET.get("job_id")
#     result = JobUnauseHelper(job_id=job_id).unpause()
#     return HttpResponse(json.dumps(result), content_type='application/json')


def ping(request):
    return HttpResponse(json.dumps({"message": "ok"}), content_type="application/json")
