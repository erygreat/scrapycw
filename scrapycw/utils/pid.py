import errno
import os
import signal
import time
import platform

def write_pid_file(pid_file, pid=os.getpid()):
    if os.path.exists(pid_file):
        os.remove(pid_file)

    pid_dir = os.path.dirname(pid_file)
    if not os.path.exists(pid_dir):
        os.makedirs(pid_dir)

    with open(pid_file, 'w+', encoding='utf-8') as f:
        f.write(str(pid))

    return str(pid)


def get_pid_by_file(pid_file):
    if not os.path.exists(pid_file):
        return None
    with open(pid_file, 'r', encoding='utf-8') as f:
        pid = f.read()
    return pid


def is_running(pid):
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            return False
    return True
