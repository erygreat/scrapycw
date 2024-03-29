
import datetime
import time
import json
from scrapycw.utils.scrapycw import init_django_env
init_django_env()

# flake8: noqa
from scrapycw.commands.crawl import Command as CrawlCommand
from scrapycw.commands.pause import Command as PauseCommand
from scrapycw.commands.unpause import Command as UnPauseCommand
from scrapycw.commands.stop import Command as StopCommand
from scrapycw.helpers.job import JobHelper, JobStatsHelper
from scrapycw.web.app.models import SpiderJob


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def pytest_crawl_spiders_has_log():
    opts = Dict()
    opts['project'] = "default"
    opts['spargs'] = {}
    result = CrawlCommand().run(["ip_taobao"], opts)
    model = SpiderJob.objects.filter(job_id=result.data['job_id']).get()
    assert(model is not None)
    assert(model.job_id == result.data['job_id'])
    assert(model.spider == "ip_taobao")
    assert(model.project == "default")
    assert(model.status == SpiderJob.STATUS.RUNNING)
    assert(model.log_file is not None)
    assert(datetime.datetime.now() - model.start_time < datetime.timedelta(seconds=5))
    assert(model.end_time is None)
    assert(model.close_reason is None)
    assert(model.stats is None)
    assert(model.log_info is None)
    assert(model.page_count is None)
    assert(model.item_count is None)

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
    opts = Dict()
    opts['project'] = "default"
    opts['spargs'] = {}
    # 启动爬虫
    result = CrawlCommand().run(["baidu"], opts)
    model = SpiderJob.objects.filter(job_id=result.data['job_id']).get()
    assert(model is not None)
    assert(model.job_id == result.data['job_id'])
    assert(model.spider == "baidu")
    assert(model.project == "default")
    assert(model.status == SpiderJob.STATUS.RUNNING)
    assert(model.log_file is None)
    assert(datetime.datetime.now() - model.start_time < datetime.timedelta(seconds=5))
    assert(model.end_time is None)
    assert(model.close_reason is None)
    assert(model.stats is None)
    assert(model.log_info is None)
    assert(model.page_count is None)
    assert(model.item_count is None)

    start_time = time.time()
    while True:
        model = SpiderJob.objects.filter(job_id=result.data['job_id']).get()
        if model.status == SpiderJob.STATUS.CLOSED:
            assert(model.status == SpiderJob.STATUS.CLOSED)
            assert(model.end_time is not None)
            assert(model.end_time - model.start_time > datetime.timedelta(seconds=5))
            assert(model.close_reason == JobHelper.DEFAULT_CLOSE_REASON)
            assert(model.stats is None)
            assert(model.log_info is None)
            assert(model.page_count is None)
            assert(model.item_count is None)
            assert(model.updated_time > model.created_time)
            return
        elif time.time() - start_time > 2 * 60:
            assert(False)
        else:
            time.sleep(10)


def pytest_pause_spider():
    opts = Dict()
    opts['project'] = "default"
    opts['spargs'] = {}
    # 启动爬虫
    result = CrawlCommand().run(["baidu_log"], opts)
    model = SpiderJob.objects.filter(job_id=result.data['job_id']).get()
    job_id = model.job_id
    assert(not JobStatsHelper(job_id=job_id).is_paused())
    assert(JobStatsHelper(job_id=job_id).is_running())
    # 暂停爬虫
    result = PauseCommand().run([job_id], {})
    assert(result.success)
    assert(result['data']['status'] == "paused")
    assert(JobStatsHelper(job_id=job_id).is_paused())
    assert(JobStatsHelper(job_id=job_id).is_running())
    # 取消爬虫暂停
    result = UnPauseCommand().run([job_id], {})
    assert(result.success)
    assert(result['data']['status'] == "running")
    assert(not JobStatsHelper(job_id=job_id).is_paused())
    assert(JobStatsHelper(job_id=job_id).is_running())
    # 关闭爬虫
    result = StopCommand().run([job_id], {})
    assert(result.success)
    assert(result['data']['status'] == "closing")
    assert(not JobStatsHelper(job_id=job_id).is_running())
    # 等待爬虫关闭
    start_time = time.time()
    while True:
        model = SpiderJob.objects.filter(job_id=job_id).get()
        if model.status == SpiderJob.STATUS.CLOSED:
            assert(model.status == SpiderJob.STATUS.CLOSED)
            assert(model.close_reason == JobHelper.CLOSE_REASON.SHUTDOWN)
            return
        elif time.time() - start_time > 2 * 60:
            assert(False)
        else:
            time.sleep(10)
