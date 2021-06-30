from _pytest.config import ExitCode
from tests.conftest import current_dir


def test_crawl(testdir):
    testdir.makepyfile("""
        import os
        import sys
        sys.path.insert(0, "{}")

        from tests.pytest_run_subprocess.test_crawl import pytest_crawl_spiders
        pytest_crawl_spiders()
    """.format(current_dir))
    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)
