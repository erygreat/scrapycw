import datetime
import os
import re

from scrapycw.settings import HANDLE_LOG_MAXIMUM_SIZE
from scrapycw.core.exception import ScrapycwException
from scrapycw.core.error_code import RESPONSE_CODE


class ScrapycwLoggerParserException(ScrapycwException):
    pass


class FormatParser:
    format = None
    start = 0
    end = 0
    pattern = r""

    def __init__(self, *args, **kwargs):
        pass


class AsctimeFormatParser(FormatParser):
    format = "%(asctime)s"
    name = "asctime"
    DATE_PATTERNS = {
        "%y": r"\d{2}",
        "%Y": r"\d{4}",
        "%m": r"\d{2}",
        "%d": r"\d{1,2}",
        "%H": r"\d{1,2}",
        "%I": r"\d{2}",
        "%M": r"\d{2}",
        "%S": r"\d{2}",
        "%a": r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)",
        "%A": r"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)",
        "%b": r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",
        "%B": r"(?:January|February|March|April|May|June|July|August|September|October|November|December)",
        "%c": r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2} \d{2}:\d{2}:\d{2} \d{4}",
        "%j": r"\d{3}",
        "%p": r"(?:AM|PM)",
        "%U": r"\d{2}",
        "%w": r"[0-6]",
        "%W": r"\d{2}",
        "%x": r"\d{2}/\d{2}/\d{2}",
        "%X": r"\d{2}:\d{2}:\d{2}",
        "%%": r"%"
    }

    NOT_SUPPORT_PATTERNS = ["%x", "%X", "%z"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date_format = kwargs.get("date_format", '%Y-%m-%d %H:%M:%S')
        self.pattern = self.handle_date_pattern()

    def handle_date_pattern(self):
        date_pattern = self.date_format
        for value in self.NOT_SUPPORT_PATTERNS:
            if date_pattern.find(value) != -1:
                raise ScrapycwLoggerParserException(
                    RESPONSE_CODE.LOG_PARSER_DONT_SUPPORT_DATA_FORMAT, "不支持日期格式: {}".format(value))
        for key, value in self.DATE_PATTERNS.items():
            date_pattern = date_pattern.replace(key, value)
        return date_pattern


class LevelNameFormatParser(FormatParser):
    format = "%(levelname)s"
    name = "levelname"
    pattern = r"(?:DEBUG|INFO|WARNING|ERROR|CRITICAL)"


class MessageFormatParser(FormatParser):
    format = "%(message)s"
    name = "message"
    pattern = r".*"


class NameFormatParser(FormatParser):
    format = "%(name)s"
    name = "name"
    pattern = r".*?"


class LevelNoFormatParser(FormatParser):
    format = "%(levelno)s"
    name = "levelno"
    pattern = r"(?:10|20|30|40|50)"


class MsecsFormatParser(FormatParser):
    format = "%(msecs)d"
    name = "msecs"
    pattern = r"\d{1,4}"


class LineNoFormatParser(FormatParser):
    format = "%(lineno)d"
    name = "lineno"
    pattern = r"\d*"


class CreatedFormatParser(FormatParser):
    format = "%(created)f"
    name = "created"
    pattern = r"[\d|\.]+"


class RelativeCreatedFormatParser(FormatParser):
    format = "%(relativeCreated)d"
    name = "relativeCreated"
    pattern = r"\d+"


class FuncNameFormatParser(FormatParser):
    format = "%(funcName)s"
    name = "funcName"
    pattern = r"[\w|\<|\>]+?"


class ThreadFormatParser(FormatParser):
    format = "%(thread)d"
    name = "thread"
    pattern = r"\d+"


class ProcessFormatParser(FormatParser):
    format = "%(process)d"
    name = "process"
    pattern = r"\d+"


class ThreadNameParser(FormatParser):
    format = "%(threadName)s"
    name = "threadName"
    pattern = ".*?"


class ProcessNameParser(FormatParser):
    format = "%(processName)s"
    name = "processName"
    pattern = ".*?"


class ModuleParser(FormatParser):
    format = "%(module)s"
    name = "module"
    pattern = ".+?"


class FilenameParser(FormatParser):
    format = "%(filename)s"
    name = "filename"
    pattern = ".+?"


class PathnameParser(FormatParser):
    format = "%(pathname)s"
    name = "pathname"
    pattern = ".+?"

# FORMAT_ASCTIME = "%(asctime)s"                      # 日志时间, 如：2003-07-08 16:49:45,896
# FORMAT_CREATED = "%(created)f"                      # 日志时间，时间戳 time.time()
# FORMAT_RELATIVE_CREATED = "%(relativeCreated)d"     # 日志运行时间
# FORMAT_MSECS = "%(msecs)d"                          # 日志事件发生事件的毫秒部分
# FORMAT_LEVEL_NAME = "%(levelname)s"                 # 日志等级，例如：'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
# FORMAT_LEVEL_NO = "%(levelno)s"                     # 根据数字形式记录日志等级, 例如：10, 20, 30, 40, 50
# FORMAT_LINENO = "%(lineno)d"                        # 日志记录函数所在行号
# FORMAT_FUNC_NAME = "%(funcName)s"                   # 函数名
# FORMAT_THREAD = "%(thread)d"                        # 线程ID, threading.get_ident() / threading.current_thread().ident
# FORMAT_PROCESS = "%(process)d"                      # 进程ID, multiprocessing.current_process().ident
# FORMAT_THREAD_NAME = "%(threadName)s"               # 线程名称, threading.current_thread().getName()
# FORMAT_PROCESS_NAME = "%(processName)s"             # 线程名称, multiprocessing.current_process().name
# FORMAT_NAME = "%(name)s"                            # 日志处理器名称，默认为'root'
# FORMAT_MODULE = "%(module)s"                        # 所属模块, filename的名称部分，不包含后缀
# FORMAT_FILENAME = "%(filename)s"                    # 所属文件，filename的文件名，包含后缀
# FORMAT_PATHNAME = "%(pathname)s"                    # 文件全路径
# FORMAT_MESSAGE = "%(message)s"                      # 日志消息


class LoggerParser:
    handler_classes = [
        AsctimeFormatParser,
        CreatedFormatParser,
        RelativeCreatedFormatParser,
        MsecsFormatParser,
        LevelNameFormatParser,
        LevelNoFormatParser,
        LineNoFormatParser,
        FuncNameFormatParser,
        ThreadFormatParser,
        ProcessFormatParser,
        ThreadNameParser,
        ProcessNameParser,
        NameFormatParser,
        ModuleParser,
        FilenameParser,
        PathnameParser,
        MessageFormatParser,
    ]

    def __init__(self, filename, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
                 log_date_format='%Y-%m-%d %H:%M:%S', telnet_password=None):
        if not filename:
            raise ScrapycwLoggerParserException(RESPONSE_CODE.LOG_PARSER_FILENAME_IS_NONE, "日志解析没有日志文件路径")
        self.filename = filename
        self.log_format = format
        self.log_date_format = log_date_format
        self.telnet_password = telnet_password
        self.log_size = self.get_file_size()
        self.content = self.read_log_file()

    def get_file_size(self):
        # 文件是否存在
        if not os.path.exists(self.filename):
            raise ScrapycwLoggerParserException(
                RESPONSE_CODE.LOG_PARSER_LOG_NOT_FIND, "日志文件不存在")
        # 文件是否超过最大解析大小
        return os.path.getsize(self.filename)

    def read_log_file(self):
        if self.log_size > HANDLE_LOG_MAXIMUM_SIZE:
            max_size = self.get_file_size_pretty(HANDLE_LOG_MAXIMUM_SIZE)
            current_size = self.get_file_size_pretty(self.log_size)
            raise ScrapycwLoggerParserException(
                RESPONSE_CODE.LOG_PARSER_LOG_SIZE_MAXIMUM, "当前设置最大可解析日志大小为{}，当前日志大小为: {}, 可以修改 HANDLE_LOG_MAXIMUM_SIZE 修改可解析日志大小".format(max_size, current_size))
        # 获取所有日志内容 TODO 是否会存在内存不够用的问题？如果是，则需要逐行处理
        with open(self.filename) as f:
            return f.read()

    def get_file_size_pretty(self, size, flag=0):
        flags = ["B", "KB", "MB", "GB", "TB"]
        if size // 1024 == 0:
            return str(size % 1024) + flags[flag]
        return self.get_file_size_pretty(size // 1024, flag + 1)

    def parse(self):
        # TODO 需要解决问题：当前message如果有换行则必须放在最后一个位置！鉴于Scrapy原始日志中会有换行，因为message必须放在最后一个位置，并且不能再后面加空格
        logger_pattern = re.escape(self.log_format)
        positions = {}
        for handler_class in self.handler_classes:
            handler = handler_class(date_format=self.log_date_format)
            logger_pattern = logger_pattern.replace(
                re.escape(handler.format), "({})".format(handler.pattern), -1)
            indexs = [m.start() for m in re.finditer(
                re.escape(handler.format), self.log_format)]
            for index in indexs:
                positions[index] = handler.name
        names = [name for _, name in sorted(positions.items())]

        lines = self.content.split("\n")
        results = []
        index = 0
        for line in lines:
            index += 1
            values = re.findall(logger_pattern, line)
            # 如果当前行不符合格式，则没有值
            values = values[0] if len(values) == 1 else tuple()
            # 如果只有一个属性，那么解析结果可能不是tuple
            values = values if isinstance(values, tuple) else (values,)

            if len(values) == 0 and len(results) == 0:
                continue
            elif len(values) == len(names):
                result = {}
                for i in range(len(names)):
                    name = names[i]
                    value = values[i]
                    result[name] = value
                results.append(result)
                result["origin"] = line
                result['index'] = index
            elif line != "" and len(results) != 0:
                results[-1][MessageFormatParser.name] += "\n" + line
                results[-1]["origin"] += line
                results[-1]['index'] = index
        return results


class ScrapyLoggerParser(LoggerParser):

    password_pattern = r"Telnet Password: (\w*)$"
    extension_pattern = r"Enabled extensions:(.*)$"
    downloader_middleware_pattern = r"Enabled downloader middlewares:(.*)$"
    spider_middleware_pattern = r"Enabled spider middlewares:(.*)$"
    pipeline_pattern = r"Enabled item pipelines:(.*)$"
    crawl_stats_pattern = r"Crawled (\d*) pages \(at (\d*) pages/min\), scraped (\d*) items \(at (\d*) items/min\)"
    close_pattern = r"Closing spider \((\w*)\)"
    stats_pattern = r"Dumping Scrapy stats:(.*)$"
    telnet_host_pattern = r"Telnet console listening on (.*):\w*$"
    telnet_port_pattern = r"Telnet console listening on .*:(\w*)$"

    level_nos = {
        '10': "DEBUG",
        '20': "INFO",
        '30': "WARNING",
        '40': "ERROR",
        '50': "CRITICAL",
    }

    def execute(self):
        results = super().parse()
        if len(results) == 0:
            return None

        # 按照日志的password将日志分隔
        log_list = []
        for result in results:
            message = result.get("message", "")
            password_match = re.search(self.password_pattern, message)
            if password_match:
                log_list.append([])

            if len(log_list) > 0:
                logs = log_list[-1]
            else:
                continue
            logs.append(result)
        # 如果没有password则将所有的都进行解析
        if len(log_list) == 0:
            log_list.append(results)

        results = []
        for logs in log_list:
            result = self._parse_logs(logs)
            if self.telnet_password and self.telnet_password == result['telnet_password']:
                return result
            else:
                results.append(result)
        return None if self.telnet_password else results

    def _parse_logs(self, logs):
        start_line = logs[0]
        end_line = logs[-1]
        # 开始时间
        start_time = self.get_time(start_line)
        # 结束时间
        last_time = self.get_time(end_line)
        # 持续时长
        if end_line.get("relativeCreated", None):
            relative_created = float(end_line.get(
                "relativeCreated", None)) / 1000
            continuous_time = datetime.datetime.fromtimestamp(
                relative_created) - datetime.datetime.fromtimestamp(0)
        elif last_time and start_time:
            continuous_time = last_time - start_time
        else:
            continuous_time = None

        """
        # 密码
        # password = self.search_log_message(self.password_pattern, logs)
        # extensions
        # extensions = self.search_log_message(self.extension_pattern, logs, parse_json=True)
        # downloader middleware
        # downloader_middlewares = self.search_log_message(self.downloader_middleware_pattern, logs, parse_json=True)
        # spider middleware
        # spider_middlewares = self.search_log_message(self.spider_middleware_pattern, logs, parse_json=True)
        # pipelines
        # pipelines = self.search_log_message(self.pipeline_pattern, logs, parse_json=True)
        # close reason
        # close_reason = self.search_log_message(self.close_pattern, logs)
        """
        # pylint: disable=unbalanced-tuple-unpacking
        password, telnet_host, telnet_port, extensions, downloader_middlewares, spider_middlewares, pipelines, close_reason, stats = self.search_log_message(logs, (
            self.password_pattern,
            self.telnet_host_pattern,
            self.telnet_port_pattern,
            self.extension_pattern,
            self.downloader_middleware_pattern,
            self.spider_middleware_pattern,
            self.pipeline_pattern,
            self.close_pattern,
            self.stats_pattern,
        ))

        levels = {}
        crawl_stats = []
        for log in logs:
            if log.get("levelname"):
                level = log.get("levelname")
            elif log.get("levelno"):
                level = self.level_nos.get(log.get("levelno"))
            else:
                level = None

            number = levels.get(level, 0)
            levels[level] = number + 1

            match = re.search(self.crawl_stats_pattern, log.get("message", ""))
            if match:
                crawl_stat = {
                    "time": self.get_time(log),
                    "page_count": int(match.group(1)),
                    "page": int(match.group(2)),
                    "item_count": int(match.group(3)),
                    "item": int(match.group(4)),
                }
                crawl_stats.append(crawl_stat)
        
        if stats:
            page_count = stats.get("response_received_count", 0)
            item_count = stats.get("item_scraped_count", 0)
        else:
            page_count = crawl_stats[-1]['page_count'] if len(crawl_stats) > 0 else None
            item_count = crawl_stats[-1]['item_count'] if len(crawl_stats) > 0 else None
    
        return {
            "start_time": start_time,
            "last_time": last_time,
            "end_time": last_time if close_reason else None,
            "continuous_time": continuous_time,
            "telnet_password": password,
            "telnet_host": telnet_host,
            "telnet_port": telnet_port,
            "extensions": extensions,
            "pages": page_count,
            "items": item_count,
            "downloader_middlewares": downloader_middlewares,
            "spider_middlewares": spider_middlewares,
            "pipelines": pipelines,
            "levels": levels,
            # "level_logs": level_logs,
            "crawl_stats": crawl_stats,
            "close_reason": close_reason,
            "spider_stats": stats,
            "is_close": close_reason is not None
        }
        # print()
        # print("=====================================")
        # print("创建时间: \t\t{}".format(start_time))
        # print("截止时间: \t\t{}".format(end_time))
        # print("持续时长: \t\t{}".format(continuous_time))
        # print("telnet密码: \t\t{}".format(password))
        # print("telnet host: \t{}".format(telnet_host))
        # print("telnet port: \t{}".format(telnet_port))
        # print("extensions: \t{}".format(extensions))
        # print("下载中间件: \t\t{}".format(downloader_middlewares))
        # print("爬虫中间件: \t\t{}".format(spider_middlewares))
        # print("pipelines: \t\t{}".format(pipelines))
        # print("levels: \t\t{}".format(levels))
        # print("CRITICAL log: \t{}".format(level_logs.get("CRITICAL")))
        # print("crawl stats: \t{}".format(crawl_stats))
        # print("关闭原因: \t\t{}".format(close_reason))
        # print("关闭stats: \t\t{}".format(stats))

    def search_log_message(self, logs, patterns):
        if isinstance(patterns, str):
            patterns = (patterns, )

        _patterns = {}
        results = []
        index = 0
        for pattern in patterns:
            _patterns[index] = pattern
            results.append(None)
            index += 1

        for log_obj in logs:
            message = log_obj.get("message", "")
            for index, pattern in _patterns.copy().items():
                match = re.search(pattern, message, re.M | re.S)
                if match:
                    result = match.group(1).replace("\r", "").replace("\n", "")
                    try:
                        results[index] = eval(result)
                    except Exception:
                        results[index] = result
                    _patterns.pop(index)
        return results

    def change_level_no_to_name(self):
        pass

    def get_time(self, line):
        if not line:
            return None
        elif line.get("asctime", None):
            return datetime.datetime.strptime(line.get("asctime"), self.log_date_format)
        elif line.get("created", None):
            return datetime.datetime.fromtimestamp(float(line.get("created")))
        else:
            return None


if __name__ == "__main__":
    # 测试代码1
    filename = "/Users/mac/Git/spider/logs/scrapy_app_spider.spiders.google_publisher_spider_2020_2_7.log"

    parser = ScrapyLoggerParser(filename=filename)
    for content in parser.parse():
        print(content)
    print(parser.execute())

    # 开发 TODO 需要解决问题：当前message如果有换行则必须放在最后一个位置！鉴于Scrapy原始日志中会有换行，因为message必须放在最后一个位置，并且不能再后面加空格
    # filename = "/Users/mac/Git/spider/logs/test.log"
    # format = '%(name)s -  %(levelno)s - %(created)f - %(name)s - %(funcName)s -"%(process)d"- "%(thread)d"- %(message)s'
    #
    # date_format = '%Y-%m-%d %H:%M:%S'
    # logging.basicConfig(filename=filename, filemode="w", level=logging.INFO, format=format, datefmt=date_format)
    # logger = logging.getLogger("hello")
    # logger.error("完成")
    # time.sleep(1)
    # logger.info("完成x\nxxxx\ns")
    # time.sleep(2)
    #
    # logger.info("完成")
    # parser = ScrapyLoggerParser(filename=filename, format=format, log_date_format=date_format)
    # for content in parser.parse():
    #     print(content)
    # parser.execute()
