import os


def write_once(filename, data):

    if os.path.exists(filename):
        os.remove(filename)

    pid_dir = os.path.dirname(filename)
    if not os.path.exists(pid_dir):
        os.makedirs(pid_dir)

    with open(filename, 'w+', encoding='utf-8') as f:
        f.write(data)

    return True
