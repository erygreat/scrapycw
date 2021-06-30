
from scrapycw.utils.scrapycw import init_django_env
from scrapycw.commands.crawl import Command


class Dict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


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