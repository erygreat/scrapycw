import socket


def port_is_used(port, host="localhost"):
    """
    判断端口是否已经被使用
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        return True
    except Exception:
        return False
