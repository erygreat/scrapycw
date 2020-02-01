import socket
import telnetlib

from scrapycw.settings import TELNET_TIMEOUT
from scrapycw.utils.exception import ScrapycwException


class ScrapycwTelnetException(ScrapycwException):
    pass


class ScrapycwAuthenticationFailException(ScrapycwTelnetException):
    pass


class Telnet:

    PATTERN_CARRIAGE_RETURN = "\\r\\r\\r\\n"

    def __init__(self, host, port=0, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.__conn = None
        self.__sock = None

    def connect(self):
        try:
            self.__conn = telnetlib.Telnet(host=self.host, port=self.port, timeout=TELNET_TIMEOUT)
            self.__sock = self.__conn.get_socket()
        except ConnectionRefusedError as e:
            raise ScrapycwTelnetException(str(e))

        try:
            # 输入用户名
            self.__conn.read_until(b"Username:", timeout=TELNET_TIMEOUT)
            self.__sock.send(self.username.encode("utf-8") + b"\r\n")
            self.__sock.send(telnetlib.IAC + telnetlib.DO + telnetlib.ECHO)

            # 输入密码
            buf = self.__sock.recv(50)
            self.__sock.send(self.password.encode("utf-8") + b"\r\n")
            self.__sock.send(telnetlib.IAC + telnetlib.DONT + telnetlib.ECHO)

            # 获取输入结果
            buf = self.__sock.recv(50)
            if str(buf).find("Authentication failed") != -1:
                self.__conn.close()
                raise ScrapycwAuthenticationFailException("Scrapy Authentication failed")
        except ConnectionResetError as e:
            raise ScrapycwTelnetException(str(e))
        except socket.timeout as e:
            raise ScrapycwTelnetException(str(e))

    def command(self, content=""):
        try:
            if self.__conn is None:
                raise ScrapycwTelnetException("Telnet don't connect, please connect it")
            self.__conn.write(content.encode() + b"\r\n")
            data = self.__conn.read_until(">>>".encode(), timeout=TELNET_TIMEOUT)
            data = str(data)
            # 去除命令回显
            index = data.find(self.PATTERN_CARRIAGE_RETURN)
            data = data[index + 8:]

            # 去除 >>> 的显示
            index = data.rfind(self.PATTERN_CARRIAGE_RETURN)
            data = data[:index]

            # 将所有换行字符改为换行
            data = data.replace(self.PATTERN_CARRIAGE_RETURN, "\r\n")

            return data if data is not None else None
        except ConnectionResetError as e:
            raise ScrapycwTelnetException(str(e))
        except socket.timeout as e:
            raise ScrapycwTelnetException(str(e))

    def close(self):
        self.__conn.close()
        self.__conn = None


if __name__ == "__main__":
    try:
        telnet = Telnet("127.0.0.1", 6024, "scrapy", '2fc85472fcb534e3')
        telnet.connect()
        print(telnet.command("est()"))
        telnet.close()
    except ScrapycwTelnetException as e:
        print(e.message)

#
# if __name__ == "__main__":
#     tn = telnetlib.Telnet(host="127.0.0.1", port=6023,)
#     sock = tn.get_socket()
#     # 输入用户名
#     buf = tn.read_until(b"Username:")
#     sock.send(b"scrapy\r\n")
#     sock.send(telnetlib.IAC + telnetlib.DO + telnetlib.ECHO)
#
#     # 输入密码
#     buf = sock.recv(50)
#     sock.send(b"c4146cb487affde7\r\n")
#     sock.send(telnetlib.IAC + telnetlib.DONT + telnetlib.ECHO)
#
#     # 获取输入结果
#     buf = sock.recv(50)
#     if str(buf).find("Authentication failed") != -1:
#         print("Authentication failed")
#         sock.close()
#         sys.exit(1)
#
#     print("密码正确")
#
#     sock.send(b"len(engine.slot.inprogress)\r" + telnetlib.BINARY)
#     buf = sock.recv(10*1024)
#     print(buf)
#
#     sock.send(b"engine.slot.closing\r" + telnetlib.BINARY)
#     buf = sock.recv(10*1024)
#     print(buf)
#
#     sock.send(b"len(engine.downloader.active)\r" + telnetlib.BINARY)
#     buf = sock.recv(10*1024)
#     print(buf)
#     sock.close()
