import socket


def port_is_used(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("localhost", port))
        return True
    except:
        return False

