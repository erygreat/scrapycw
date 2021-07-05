import datetime
import json
import time

from scrapycw import settings
from scrapycw.core.scrapycw_object import ScrapycwObject
from scrapy.settings import BaseSettings


class DatetimeJsonEncoder(json.JSONEncoder, ScrapycwObject):
    """
    python对象转换为Json时的时间类型处理器
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            if settings.HANDLE_LOG_USE_TIMEZONE:
                now_timestamp = time.time()
                utc_diff_time = datetime.datetime.fromtimestamp(now_timestamp) - datetime.datetime.utcfromtimestamp(now_timestamp)
                timezone_timestamp = time.mktime(obj.timetuple()) + utc_diff_time.total_seconds()
                timezone_struct_time = time.localtime(timezone_timestamp)
                return time.strftime('%Y-%m-%d %H:%M:%S', timezone_struct_time)
            else:
                return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, datetime.timedelta):
            return obj.__str__()
        return super(DatetimeJsonEncoder, self).default(obj)


class ScrapySettingEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, BaseSettings):
            items = {}
            for key, value in obj.attributes.items():
                items[key] = value.value
            return items
        # if isinstance(obj, datetime.datetime):
        #     return obj.strftime("%Y-%m-%d %H:%M:%S")
        # if isinstance(obj, object):
        #     return dict({'__classname__': type(obj).__name__}, **vars(obj))
        return super(ScrapySettingEncoder, self).default(obj)


if __name__ == "__main__":
    current_time = datetime.datetime.now()
    d = {"current_time": current_time}
    d_str = json.dumps(d, cls=DatetimeJsonEncoder)
    print(d_str)
