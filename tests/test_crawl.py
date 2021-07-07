from scrapycw.services.job import Service
from _pytest.config import ExitCode
from tests.conftest import current_dir
import random


def test_crawl_has_log(testdir):
    testdir.makepyfile("""
        import os
        import sys
        current_dir = "{}"
        sys.path.insert(0, current_dir)
        from scrapy.utils.conf import closest_scrapy_cfg
        project_dir = os.path.dirname(closest_scrapy_cfg(current_dir))
        os.chdir(project_dir)

        from tests.pytest_run_subprocess.test_crawl import pytest_crawl_spiders_has_log
        pytest_crawl_spiders_has_log()
    """.format(current_dir))
    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)


def test_crawl(testdir):
    testdir.makepyfile("""
        import os
        import sys
        current_dir = "{}"
        sys.path.insert(0, current_dir)
        from scrapy.utils.conf import closest_scrapy_cfg
        project_dir = os.path.dirname(closest_scrapy_cfg(current_dir))
        os.chdir(project_dir)

        from tests.pytest_run_subprocess.test_crawl import pytest_crawl_spiders
        pytest_crawl_spiders()
    """.format(current_dir))
    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)


def test_pause(testdir):
    testdir.makepyfile("""
        import os
        import sys
        current_dir = "{}"
        sys.path.insert(0, current_dir)
        from scrapy.utils.conf import closest_scrapy_cfg
        project_dir = os.path.dirname(closest_scrapy_cfg(current_dir))
        os.chdir(project_dir)

        from tests.pytest_run_subprocess.test_crawl import pytest_pause_spider
        pytest_pause_spider()
    """.format(current_dir))
    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)

def test_jobs():
    response = Service.jobs(spider="baidu")
    jobs = response.data['jobs']
    assert(len(jobs) > 0)
    assert(response.data['count'] > 0)
    for job in jobs:
        assert(job['status'] == "closed")
        assert(job['close_reason'] == "unknown")

    response = Service.jobs(status="running")
    jobs = response.data['jobs']
    for job in jobs:
        assert(job['status'] == "running")
        assert(job['close_reason'] is None)

    response = Service.jobs(close_reason="shutdown")
    jobs = response.data['jobs']
    for job in jobs:
        assert(job['status'] == "closed")
        assert(job['close_reason'] == "shutdown")

def test_job_stats():
    response = Service.jobs()
    jobs = response.data['jobs']
    for job in jobs:
        job_id = job['job_id']
        has_settings = random.random() > 0.5
        has_log = random.random() > 0.5
        has_est = random.random() > 0.5
        has_stats = random.random() > 0.5
        stats = Service.stats(job_id=job_id, is_parse_settings=has_settings, is_parse_log=has_log, is_parse_stats=has_stats, is_parse_est=has_est)
        assert(stats['data']['status'] == "closed")
        if has_settings:
            assert(stats['data'].get("settings", None) != None)
        else:
            assert(stats['data'].get("settings", None) == None)

        if has_log:
            assert(stats['data'].get("log_info", None) != None)
        else:
            assert(stats['data'].get("log_info", None) == None)

        if has_est:
            if stats['data']['status'] == "running":
                assert(stats['data'].get("est", None) != None)
            else:
                assert(stats['data'].get("est", None) == None)
        else:
            assert(stats['data'].get("est", None) == None)

        if not has_stats:
            assert(stats['data'].get("stats", None) == None)
