import os
import time

from scrapycw.utils.exception import ScrapycwReadException


def write_once(filename, data):
    """
    向文件中写入数据，如果没有文件则创建，覆盖原有数据
    :params filename 文件名称
    :params data 文件数据
    """

    if os.path.exists(filename):
        os.remove(filename)

    pid_dir = os.path.dirname(filename)
    if not os.path.exists(pid_dir):
        os.makedirs(pid_dir)

    with open(filename, 'w+', encoding='utf-8') as f:
        f.write(data)

    return True


def read_until_or_timeout(filename, timeout=5000):
    """
    读取文件直到文件读取完成或者超时
    :params filename 文件名称
    :params timeout 超时时间，单位为毫秒
    """
    start_time = time.time()
    while True:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = f.read()
                if data:
                    return data
        except FileNotFoundError:
            if time.time() - start_time > timeout:
                raise ScrapycwReadException("读取文件超时!")
            time.sleep(0.01)


def read_until_once_or_timeout(filename_and_types, timeout=5000):
    """
    :params filename_and_types 文件和类型列表 [{
        "filename": "xxxx.error",
        "type": "error",
    }, {
        "filename": "xxxx.data",
        "type": "data",
    }]
    :return [类型, 文件数据]
    """
    if len(filename_and_types) == 0:
        raise ScrapycwReadException("请输入文件!")
    start_time = time.time()
    while True:
        for filename_and_type in filename_and_types:
            filename = filename_and_type['filename']
            type = filename_and_type['type']
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    return type, f.read()
            except FileNotFoundError:
                pass
        if time.time() - start_time > timeout:
            raise ScrapycwReadException("读取文件超时!")
        time.sleep(0.01)


def remove_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)