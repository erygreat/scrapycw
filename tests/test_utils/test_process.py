from _pytest.config import ExitCode
from tests.conftest import current_dir


def test_process_1(testdir):
    testdir.makepyfile("""
        import os
        import sys
        sys.path.insert(0, "{}")
        from tests.pytest_run_subprocess.test_process import pytest_run_daemon_1
        pytest_run_daemon_1()
    """.format(current_dir))

    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)


def test_process_2(testdir):
    testdir.makepyfile("""
        import os
        import sys
        sys.path.insert(0, "{}")
        from tests.pytest_run_subprocess.test_process import pytest_run_daemon_2
        pytest_run_daemon_2()
    """.format(current_dir))

    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)


def test_process_3(testdir):
    testdir.makepyfile("""
        import os
        import sys
        sys.path.insert(0, "{}")
        from tests.pytest_run_subprocess.test_process import pytest_run_daemon_3
        pytest_run_daemon_3()
    """.format(current_dir))

    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)


def test_process_4(testdir):
    testdir.makepyfile("""
        import os
        import sys
        sys.path.insert(0, "{}")
        from tests.pytest_run_subprocess.test_process import pytest_run_daemon_exception
        pytest_run_daemon_exception()
    """.format(current_dir))

    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)


def test_process_5(testdir):
    testdir.makepyfile("""
        import os
        import sys
        sys.path.insert(0, "{}")
        from tests.pytest_run_subprocess.test_process import pytest_run_daemon_exception_normal
        pytest_run_daemon_exception_normal()
    """.format(current_dir))

    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)


def test_process_6(testdir):
    testdir.makepyfile("""
        import os
        import sys
        sys.path.insert(0, "{}")
        from tests.pytest_run_subprocess.test_process import pytest_run_daemon_static_method
        pytest_run_daemon_static_method()
    """.format(current_dir))

    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)


def test_process_7(testdir):
    testdir.makepyfile("""
        import os
        import sys
        sys.path.insert(0, "{}")
        from tests.pytest_run_subprocess.test_process import pytest_is_running
        pytest_is_running()
    """.format(current_dir))

    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)


def test_process_8(testdir):
    testdir.makepyfile("""
        import os
        import sys
        sys.path.insert(0, "{}")
        from tests.pytest_run_subprocess.test_process import pytest_kill
        pytest_kill()
    """.format(current_dir))

    r = testdir.runpytest_subprocess()
    assert(r.ret == ExitCode.NO_TESTS_COLLECTED)
