import logging
import telnetlib
from time import sleep

from scrapycw.utils.exception import ScrapycwException


class ScrapycwTelnetException(ScrapycwException):
    pass


class Telnet:

    def __init__(self, host, port=0, username=None, password=None, log_level=0):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.__conn = None
        self.err_message = None
        self.log_level = log_level

    def connect(self):
        # try:
        self.__conn = telnetlib.Telnet(host=self.host, port=self.port)
        # except ConnectionRefusedError as e:
        #     self.err_message = e
        #     return False
        self.__conn.set_debuglevel(self.log_level)
        if self.username:
            self.command("Username:", self.username)
        if self.username and self.password:
            self.command("Password:", self.password)
        return True

    def command(self, flag=None, content=""):
        if self.__conn is None:
            raise ScrapycwTelnetException("Telnet don't connect, please connect it")
        data = None
        if flag:
            data = self.__conn.read_until(flag.encode())
        self.__conn.write(content.encode() + b"\n")
        return data if data is not None else None

    def close(self):
        self.__conn.close()
        self.__conn = None


if __name__ == "__main__":
    telnet = Telnet("127.0.0.1", 6023, "scrapy", 'be2447b3dbb59139', log_level=logging.DEBUG)
    if telnet.connect():
        # telnet.command(content="hello")
        telnet.close()
    else:
        print(telnet.err_message)

    # telnet = Telnet("127.0.0.1", "6023", "scrapy", "18964c4c0bf0cfe0")
    # if telnet.connect():
    #     telnet.command("$", "hello")
    #     telnet.close()
    # else:
    #     print(telnet.err_message)
