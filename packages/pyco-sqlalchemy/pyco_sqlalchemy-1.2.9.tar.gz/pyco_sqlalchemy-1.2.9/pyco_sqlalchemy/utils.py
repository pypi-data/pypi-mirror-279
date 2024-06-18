"""
require:
    python-dateutil>=2.8.0
"""
import json
import uuid
import time
from pprint import pformat
from datetime import datetime, timedelta, timezone
# from dateutil.parser import parse as parse_datestr

TZ_UTC = timezone.utc
TZ_LOCAL = timezone(timedelta(seconds=-time.timezone))

K_ParseStr2Int_base_map = {
    "default": 10,
    "0o": 8,
    "0O": 8,
    "0b": 2,
    "0B": 2,
    "0x": 16,
    "0X": 16,
    "0+": 36,  ##; 36进制自定义的前缀:[0-10]+[a/A-z/Z] 不区分大小写
    "0#": 62,  ##; 62进制自定义的前缀:[0-10]+[az]+[AZ] 区分大小写
    "0|": 36,  ##; 36进制自定义的前缀:[0-10]+[a/A-z/Z] 不区分大小写
    "0&": 62,  ##; 62进制自定义的前缀:[0-10]+[az]+[AZ] 区分大小写
}


def parse_int(value, default_value=0):
    if isinstance(value, int):
        return value
    elif isinstance(value, float):
        return int(value)
    elif value is True:
        return 1
    elif value is False:
        return 0
    elif value:
        if isinstance(value, str):
            p = value[:2]
            base = K_ParseStr2Int_base_map.get(p, 10)
            v = int(value, base)
            return v
        else:
            v = int(value)
            return v
    else:
        return default_value


def now(tz=None):
    # 使用datetime.now, 使得到的日期, 不管时间区是多少, 时间戳都是一致的.
    # 返回等同于: datetime.utcnow().replace(tz_info=TZ_UTC)
    # eg: now(TZ_UTC).timestamp() == now(TZ_LOCAL).timestamp())
    if not tz:
        tz = TZ_LOCAL
    return datetime.now(tz=tz)


def parse_date(val, nullable=True, tz=TZ_LOCAL, fmt="%Y%m%d %H:%M:%S", **parse_kws):
    v = None
    if isinstance(val, datetime):
        v = val.timestamp()
    elif isinstance(val, str):
        v = datetime.strptime(val, fmt).timestamp()
    elif isinstance(val, (int, float)):
        v = val

    if v:
        return datetime.fromtimestamp(v, tz=tz)
    elif nullable:
        return None
    raise ValueError(f"Unknown DateValue{val}")


class BaseJSONEncoder(json.JSONEncoder):
    @classmethod
    def stringify(cls, obj, strict=False):
        if isinstance(obj, datetime):
            # default use TZ-LOCAL, eg: "2021-03-22 20:32:02.271068+08:00"
            return str(obj.astimezone())
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif hasattr(obj, 'to_json') and callable(obj.to_json):
            return obj.to_json()
        elif hasattr(obj, 'to_dict') and callable(obj.to_dict):
            return obj.to_dict()
        elif hasattr(obj, 'json'):
            if callable(obj.json):
                return obj.json()
            else:
                return obj.json

        text = pformat(obj, indent=2)
        msg = f"{type(obj)}::{text}"
        if not strict:
            return msg
        else:
            raise TypeError(f"BaseJSONEncoder: Object is not serializable. \n{msg}")

    def default(self, obj):
        return self.stringify(obj, strict=True)


###
# json_dumps 可能会抛出 TypeError
json_dumps = lambda obj: json.dumps(obj, indent=2, cls=BaseJSONEncoder)
# json_stringify 总能返回字符串结果, 不会抛出 TypeError
json_stringify = lambda obj: json.dumps(obj, indent=2, default=BaseJSONEncoder.stringify)
