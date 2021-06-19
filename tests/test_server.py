from _pytest.config import ExitCode
from tests.conftest import current_dir


def test_server(testdir):
    testdir.makepyfile("""
        import os
        import sys
        sys.path.insert(0, "{}")

        from tests.pytest_run_subprocess.test_server_subprocess import pytest_run_server
        pytest_run_server()
    """.format(current_dir))
    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)
