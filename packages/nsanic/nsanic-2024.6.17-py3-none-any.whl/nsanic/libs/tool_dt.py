import zoneinfo
from datetime import datetime, date, time, timedelta
from typing import Union

from nsanic.libs.consts import G_TIME_ZONE


def cur_dt(tz: str = G_TIME_ZONE):
    """当前日期"""
    return datetime.now(tz=zoneinfo.ZoneInfo(tz))


def cur_time(ms=False, tz: str = G_TIME_ZONE):
    """当前时间戳"""
    t = cur_dt(tz=tz).timestamp()
    return int(t * 1000) if ms else int(t)


def dt_str(dt: Union[datetime, date, int, float, str] = None, fmt='%Y-%m-%d %H:%M:%S', tz: str = G_TIME_ZONE):
    """日期时间字符串格式输出, 不指定时间将输出当前时间"""
    if not dt:
        return cur_dt(tz=tz).strftime(fmt)
    if isinstance(dt, datetime):
        return dt.strftime(fmt)
    elif isinstance(dt, date):
        fmt = (fmt.replace('%H:', '').replace('%H', '').replace('%M:', '').
               replace('%M', '')).replace('%S.', '').replace('%S', '').replace('%f', '')
        return dt.strftime(fmt)
    elif isinstance(dt, (int, float)):
        dt = datetime.fromtimestamp(dt, tz=zoneinfo.ZoneInfo(tz))
        return dt.strftime(fmt)
    elif isinstance(dt, str):
        dt.replace('/', '-').replace('T', ' ')
        if len(dt) > 10:
            return datetime.strptime(dt, '%Y-%m-%d %H:%M:%S').strftime(fmt)
        return datetime.strptime(dt, '%Y-%m-%d').strftime(fmt)


def to_datetime(dt: Union[date, datetime, str, int, float], fmt='%Y-%m-%d %H:%M:%S', tz=G_TIME_ZONE):
    if dt is None:
        return
    if isinstance(dt, str):
        dt = datetime.strptime(dt, fmt)
    if isinstance(dt, datetime):
        return dt
    elif isinstance(dt, date):
        return datetime.combine(dt, time(), tzinfo=zoneinfo.ZoneInfo(tz))
    elif isinstance(dt, (int, float)):
        return datetime.fromtimestamp(dt, tz=zoneinfo.ZoneInfo(tz))
    return


def create_dt(
        year=2023,
        month=1,
        day=1,
        hour=0,
        minute=0,
        second=0,
        misecond=0,
        tz: Union[str, zoneinfo.ZoneInfo] = None):
    if not tz:
        tz = zoneinfo.ZoneInfo(G_TIME_ZONE)
    if isinstance(tz, str):
        tz = zoneinfo.ZoneInfo(tz)
    return datetime(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=misecond, tzinfo=tz)


def get_day_begin(dt: Union[datetime, date] = None, tz: str = G_TIME_ZONE):
    if not dt:
        dt = datetime.now(tz=zoneinfo.ZoneInfo(tz))
    if isinstance(dt, datetime):
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        return int(dt.timestamp())
    return int(datetime.combine(dt, time(), tzinfo=zoneinfo.ZoneInfo(tz)).timestamp())


def get_day_end(dt: Union[datetime, date] = None, tz: str = G_TIME_ZONE):
    if not dt:
        dt = datetime.now(tz=zoneinfo.ZoneInfo(tz))
    if isinstance(dt, date):
        dt = datetime.combine(dt, time(), tzinfo=zoneinfo.ZoneInfo(tz))
    dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    return int(dt.timestamp())


def get_day_interval(dt: Union[datetime, date, int, float] = None, tz: str = G_TIME_ZONE):
    if not dt:
        dt = datetime.now(tz=zoneinfo.ZoneInfo(tz))
    if isinstance(dt, (int, float)):
        dt = datetime.fromtimestamp(dt, tz=zoneinfo.ZoneInfo(tz))
    if isinstance(dt, date):
        dt = datetime.combine(dt, time(), tzinfo=zoneinfo.ZoneInfo(tz))
    s_dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    e_dt = dt.replace(hour=23, minute=59, second=59, microsecond=999999)
    return int(s_dt.timestamp()), int(e_dt.timestamp())


def get_day_hours(dt: Union[datetime, date, int, float] = None, tz: str = G_TIME_ZONE):
    st, et = get_day_interval(dt, tz=tz)
    hour_list = []
    start = st
    for i in range(st, et, 3600):
        end = start + 3600 - 1
        if end >= et:
            end = et
        hour_list.append((start, end))
        start = end + 1
    return hour_list


def date_range(start: Union[datetime, date], end: Union[datetime, date] = None, tz: str = G_TIME_ZONE):
    if not end:
        end = datetime.now(tz=zoneinfo.ZoneInfo(tz)).date()
    if isinstance(start, datetime):
        start = start.date()
    if isinstance(end, datetime):
        end = end.date()
    delta = end - start
    m_date = min(start, end)
    return [m_date + timedelta(days=i) for i in range(abs(delta.days) + 1)]


def get_date_arr(days: int, set_date: Union[datetime, date] = None, tz: str = G_TIME_ZONE):
    if not set_date:
        set_date = datetime.now(tz=zoneinfo.ZoneInfo(tz)).date()
    else:
        if isinstance(set_date, datetime):
            set_date = set_date.date()
    return [(set_date - timedelta(days=days - 1 - i)) for i in range(days)]


def get_day_before(days: int, set_date: Union[datetime, date] = None, tz: str = G_TIME_ZONE):
    if not set_date:
        set_date = datetime.now(tz=zoneinfo.ZoneInfo(tz))
    return set_date - timedelta(days)
