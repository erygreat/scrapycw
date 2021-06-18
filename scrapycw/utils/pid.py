import os
from scrapycw.utils.file_uilts import write_once
import time
import psutil


def get_pid_by_file(pid_file):
    if not os.path.exists(pid_file):
        return None
    with open(pid_file, 'r', encoding='utf-8') as f:
        pid = f.read()
    return pid


def kill_pid(pid, timeout=5):
    proc = None
    for _proc in psutil.process_iter():
        if pid == _proc.pid:
            proc = _proc
            break
    if not proc:
        return True

    start_time = time.time()
    try:
        proc.kill()
        while is_running(pid):
            if time.time() - start_time > timeout:
                return False
            time.sleep(0.01)
        return True
    except OSError:
        return False


def is_running(pid):
    for _proc in psutil.process_iter():
        if pid == _proc.pid:
            return True
    return False
