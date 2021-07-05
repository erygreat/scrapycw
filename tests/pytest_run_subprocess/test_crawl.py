
import datetime
import time
import json
from scrapycw.utils.scrapycw import init_django_env
from scrapycw.commands.crawl import Command
from scrapycw.helpers.job import JobHelper


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__



def pytest_crawl_spiders_has_log():
    init_django_env()
    from scrapycw.web.app.models import SpiderJob
    opts = Dict()
    opts['project'] = "default"
    opts['spargs'] = {}
    result = Command().run(["ip_taobao"], opts)
    model = SpiderJob.objects.filter(job_id=result.data['job_id']).get()
    assert(model is not None)
    assert(model.job_id == result.data['job_id'])
    assert(model.spider == "ip_taobao")
    assert(model.project == "default")
    assert(model.status == SpiderJob.STATUS.RUNNING)
    assert(model.log_file is not None)
    assert(datetime.datetime.now() - model.start_time < datetime.timedelta(seconds=5))
    assert(model.end_time == None)
    assert(model.close_reason == None)
    assert(model.stats == None)
    assert(model.log_info == None)
    assert(model.page_count == None)
    assert(model.item_count == None)

    start_time = time.time()
    while True:
        model = SpiderJob.objects.filter(job_id=result.data['job_id']).get()
        if model.status == SpiderJob.STATUS.CLOSED:
            assert(model.status == SpiderJob.STATUS.CLOSED)
            assert(model.end_time is not None)
            assert(model.close_reason == JobHelper.CLOSE_REASON.FINISHED)
            assert(json.loads(model.stats)['downloader/response_count'] == 1)
            assert(json.loads(model.log_info)['pages'] == 1)
            assert(model.page_count == 1)
            assert(model.item_count == 1 or model.item_count == 0)
            assert(model.updated_time > model.created_time)
            return
        elif time.time() - start_time > 30:
            assert(False)
        else:
            time.sleep(10)


def pytest_crawl_spiders():
    init_django_env()
    from scrapycw.web.app.models import SpiderJob
    opts = Dict()
    opts['project'] = "default"
    opts['spargs'] = {}
    result = Command().run(["baidu"], opts)
    model = SpiderJob.objects.filter(job_id=result.data['job_id']).get()
    assert(model is not None)
    assert(model.job_id == result.data['job_id'])
    assert(model.spider == "baidu")
    assert(model.project == "default")
    assert(model.status == SpiderJob.STATUS.RUNNING)
    assert(model.log_file == None)
    assert(datetime.datetime.now() - model.start_time < datetime.timedelta(seconds=5))
    assert(model.end_time == None)
    assert(model.close_reason == None)
    assert(model.stats == None)
    assert(model.log_info == None)
    assert(model.page_count == None)
    assert(model.item_count == None)

    start_time = time.time()
    while True:
        model = SpiderJob.objects.filter(job_id=result.data['job_id']).get()
        if model.status == SpiderJob.STATUS.CLOSED:
            assert(model.status == SpiderJob.STATUS.CLOSED)
            assert(model.end_time is not None)
            assert(model.end_time - model.start_time > datetime.timedelta(seconds=5))
            assert(model.close_reason == JobHelper.DEFAULT_CLOSE_REASON)
            assert(model.stats == None)
            assert(model.log_info == None)
            assert(model.page_count == None)
            assert(model.item_count == None)
            assert(model.updated_time > model.created_time)
            return
        elif time.time() - start_time > 2 * 60:
            assert(False)
        else:
            time.sleep(10)