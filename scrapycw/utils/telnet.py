import json
import socket
import telnetlib

from scrapycw.settings import TELNET_TIMEOUT
from scrapycw.core.exception import ScrapycwException
from scrapycw.core.error_code import RESPONSE_CODE


class ScrapycwTelnetException(ScrapycwException):
    pass


class ScrapycwAuthenticationFailException(ScrapycwTelnetException):
    pass


class ScrapycwTelnetNotConnectionException(ScrapycwTelnetException):
    pass


class Telnet:

    PATTERN_CARRIAGE_RETURN = "\\r\\r\\r\\n"

    def __init__(self, host: str, port: int = 0, username: str = None, password: str = None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.__conn = None
        self.__sock = None

    def connect(self):
        try:
            self.__connect()
        except ConnectionRefusedError as e:
            raise ScrapycwTelnetException(
                RESPONSE_CODE.TELNET_CONNECTION_REFUSED_ERROR, e)
        except ConnectionResetError as e:
            raise ScrapycwTelnetException(
                RESPONSE_CODE.TELNET_CONNECTION_RESET_ERROR, e)
        except socket.timeout as e:
            raise ScrapycwTelnetException(
                RESPONSE_CODE.TELNET_CONNECTION_TIMEOUT, e)

    def __connect(self):
        """
         输入用户名和密码登录 scrapy telnet, 并创建sock连接
         TODO 需要将其中对 DONT WILL DO WONT等操作改为自动识别, 以及对 Telnet 设置做自动解析
        :return:
        :exception ConnectionRefusedError 连接被拒绝(没有该telnet)
        :exception ConnectionResetError 连接被重置(该telnet被关闭)
        :exception socket.timeout 链接超时(该telnet无法连接上)
        :exception ScrapycwAuthenticationFailException 权限验证失败，用户名或密码错误
        """
        self.__conn = telnetlib.Telnet(
            host=self.host, port=self.port, timeout=TELNET_TIMEOUT)
        self.__sock = self.__conn.get_socket()

        # 输入用户名
        self.__conn.read_until(b"Username:", timeout=TELNET_TIMEOUT)
        self.__conn.write(self.username.encode("utf-8") + b"\r\n")
        self.__sock.send(telnetlib.IAC + telnetlib.DO + telnetlib.ECHO)

        # 输入密码
        buf = self.__sock.recv(50)
        self.__sock.send(self.password.encode("utf-8") + b"\r\n")
        self.__sock.send(telnetlib.IAC + telnetlib.DONT + telnetlib.ECHO)

        # telnet设置
        self.__sock.send(b'\xff\xfd\x03\xff\xfb"\xff\xfa"\x03\x01\x03\x00\x03b\x03\x04\x02\x0f\x05\x02\x14\x07b\x1c\x08\x02\x04\tB\x1a\n\x02\x7f\x0b\x02\x15\x0c\x02\x17\r\x02\x12\x0e\x02\x16\x0f\x02\x11\x10\x02\x13\x11\x00\xff\xff\x12\x00\xff\xff\xff\xf0\xff\xfb\x1f\xff\xfa\x1f\x00\xcc\x00,\xff\xf0\xff\xfb\x03\xff\xfd\x01')
        self.__sock.send(b'\xff\xfa"\x01\x06\xff\xf0')

        # 获取输入结果
        buf = self.__sock.recv(50)
        if str(buf).find("Authentication failed") != -1:
            self.__conn.close()
            raise ScrapycwAuthenticationFailException(
                RESPONSE_CODE.TELNET_AUTHENTICATION_FAIL, "Telnet Authentication failed")

    def command(self, content: str = "", auto_change_type: bool = True):
        """
        执行命令

        :param content: 需要执行的命令
        :param auto_change_type: 自动将结果转换为响应的类型
        :return: 执行结果
        :exception ScrapycwTelnetNotConnectionException telnet没有连接
        :exception ConnectionResetError 连接被重置(该telnet被关闭)
        :exception socket.timeout 链接超时(该telnet无法连接上)
        """
        if self.__conn is None:
            raise ScrapycwTelnetNotConnectionException(
                RESPONSE_CODE.TELNET_NOT_CONNECT, "Telnet don't connect, please connect it")
        self.__conn.write(content.encode() + b"\r\n")
        data = self.__conn.read_until(">>>".encode(), timeout=TELNET_TIMEOUT)
        data = str(data)
        # 去除命令回显
        index = data.find(self.PATTERN_CARRIAGE_RETURN)
        data = data[index + 8:]

        # 去除 >>> 的显示
        index = data.rfind(">>>")
        data = data[:index]

        # 去除多余的回车换行
        index = data.rfind(self.PATTERN_CARRIAGE_RETURN)
        data = data[:index]

        # 将所有换行字符改为换行
        # data = data.replace(self.PATTERN_CARRIAGE_RETURN, "\r\n")
        if auto_change_type:
            return self.change_type(data)
        return data

    def read_util_close(self):
        if self.__conn is None:
            raise ScrapycwTelnetNotConnectionException(
                RESPONSE_CODE.TELNET_NOT_CONNECT, "Telnet don't connect, please connect it")
        self.__conn.close()
        return self.__conn.read_all()

    def change_type(self, data: str):
        """
        将data自动识别类型并转换为对应类型
        :param data: 需要转换的内容
        :return: 转换后的结果
        """
        if data == "":
            return data
        try:
            return json.loads(data)
        except Exception:
            pass

        try:
            return eval(data)
        except Exception:
            pass

        return data

    def close(self):
        self.__sock.close()
        self.__conn = None

    def command_once(self, command):
        self.connect()
        result = self.command(command)
        self.close()
        return result

if __name__ == "__main__":
    try:
        telnet = Telnet("127.0.0.1", 6028, "scrapy", '35f1140c8926e689')
        telnet.connect()
        print(telnet.command("est()"))
        telnet.close()
    except ScrapycwAuthenticationFailException:
        print("用户名或密码错误!")
    except socket.timeout:
        print("连接超时，可能telnet已关闭")
    except ConnectionResetError:
        print("连接被重置，可能telnet已关闭")
    except ConnectionRefusedError:
        print("连接被拒绝，该端口未被使用")
    except ScrapycwTelnetNotConnectionException:
        print("telnet未连接")
    except ScrapycwTelnetException as e:
        print(e.message)
