from scrapycw.services.spider import Service
from _pytest.config import ExitCode
from tests.conftest import current_dir


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
    jobs = Service.jobs(spider="baidu")
    assert(len(jobs.data) > 0)
    for job in jobs.data:
        assert(job['status'] == "closed")
        assert(job['close_reason'] == "unknown")
    jobs = Service.jobs(status="running")
    for job in jobs.data:
        assert(job['status'] == "running")
        assert(job['close_reason'] is None)

    jobs = Service.jobs(close_reason="shutdown")
    for job in jobs.data:
        assert(job['status'] == "closed")
        assert(job['close_reason'] == "shutdown")