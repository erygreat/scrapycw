import os
from scrapycw.utils.file_utils import read_until_once_or_timeout, read_until_or_timeout, write_once
from scrapycw.core.exception import ScrapycwReadException


def test_write():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "file_utils.txt")
    write_once(filename, "hello world")

    data = read_until_or_timeout(filename, 1)
    assert(data == 'hello world')


def test_read_timeout():
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), "file_utils_not_exist.txt")
    try:
        read_until_or_timeout(filename, 3)
        assert(False)
    except ScrapycwReadException as e:
        assert(e.message == '读取文件超时!')


def test_read_filename_and_types_1():
    try:
        read_until_once_or_timeout([], 1)
        assert(False)
    except ScrapycwReadException as e:
        assert(e.message == '请输入文件!')


def test_read_filename_and_types_2():
    filename1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "file_utils_not_exist_1.txt")
    filename2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "file_utils_not_exist_2.txt")
    try:
        read_until_once_or_timeout([
            {
                "type": "error",
                "filename": filename1
            },
            {
                "type": "data",
                "filename": filename2
            }
        ], 1)
        assert(False)
    except ScrapycwReadException as e:
        assert(e.message == '读取文件超时!')


def test_read_filename_and_types_3():
    filename1 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "file_utils_not_exist_1.txt")
    filename2 = os.path.join(os.path.dirname(os.path.realpath(__file__)), "file_utils_2.txt")
    data = "filename2 hello world"
    write_once(filename2, data)

    try:
        type, file_data = read_until_once_or_timeout([
            {
                "type": "error",
                "filename": filename1
            },
            {
                "type": "data",
                "filename": filename2
            }
        ], 1)
        assert(type == 'data')
        assert(data == file_data)
    except ScrapycwReadException as e:
        assert(e.message == '读取文件超时!')
