# coding=utf-8

from datetime import datetime, timedelta
import time
import calendar
from relativedelta import relativedelta
from functools import total_ordering
from timeparser import timeparse

__all__ = ['Blackhole', 'ben']


@total_ordering
class Blackhole(object):
    """核心对象,增强版本的datetime.datetime对象
    """
    mock_offset = {}
    _units = ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']

    def __init__(self, year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, dt=None):
        if dt:
            self._dt = dt
        else:
            self._dt = datetime(year, month, day, hour, minute, second, microsecond)

    @classmethod
    def mock(cls, **kwargs):
        """
        获取一个假的当前时间
        """
        cls.mock_offset = kwargs

    @classmethod
    def unmock(cls):
        cls.mock_offset = {}

    @classmethod
    def now(cls):
        dt = datetime.now()
        return cls(dt=dt).shift(**cls.mock_offset)

    @classmethod
    def fromtimestamp(cls, timestamp):
        timestamp = float(timestamp)
        dt = datetime.fromtimestamp(timestamp)
        return cls(dt=dt)

    def raw(self):
        """
        返回datetime对象
        :return:
        """
        return self._dt

    def clone(self):
        """
        生成一个新的对象
        :return:
        """
        return self.__class__(dt=self._dt)

    def replace(self, **kwargs):
        self._dt = self._dt.replace(**kwargs)

    def shift(self, **kwargs):
        """
        返回一个修改后对象
        :param kwargs:
        :return:
        """
        for unit, value in kwargs.items():
            unit = unit.rstrip('s')
            value = getattr(self, unit) + value
            setattr(self, unit, value)
        return self

    def shifted(self, **kwargs):
        """
        返回一个新的修改后对象
        :param kwargs:
        :return:
        """
        return self.clone().shift(**kwargs)

    def floor(self, unit):
        if unit not in self._units:
            raise AttributeError()
        units = self._units[:self._units.index(unit) + 1]
        values = [getattr(self, u) for u in units]
        return self.__class__(*values)

    def ceil(self, unit):
        if unit not in self._units:
            raise AttributeError()
        return self.floor(unit).shifted(**{unit: 1, 'microsecond': -1})

    # Access
    @property
    def date(self):
        return self._dt.date()

    @date.setter
    def date(self, value):
        self._dt = datetime.combine(value, self._dt.time())

    @property
    def time(self):
        return self._dt.time()

    @time.setter
    def time(self, value):
        self._dt = datetime.combine(self._dt.date(), value)

    @property
    def tuple(self):
        return self._dt.timetuple()

    @tuple.setter
    def tuple(self, value):
        self._dt = self._dt.fromtimestamp(int(time.mktime(value)))

    @property
    def year(self):
        return self._dt.year

    @year.setter
    def year(self, value):
        self._dt = self._dt.replace(year=value)

    @property
    def month(self):
        return self._dt.month

    @month.setter
    def month(self, value):
        self._dt += relativedelta(months=value - self._dt.month)

    @property
    def week(self):
        delta = self._dt - datetime(self._dt.year, 1, 1)
        return delta.days / 7

    @month.setter
    def week(self, value):
        week = self._get_week()
        self._dt += timedelta(weeks=value - week)

    @property
    def day(self):
        return self._dt.day

    @day.setter
    def day(self, value):
        self._dt += timedelta(days=value - self._dt.day)

    @property
    def hour(self):
        return self._dt.hour

    @hour.setter
    def hour(self, value):
        self._dt += timedelta(hours=value - self._dt.hour)

    @property
    def minute(self):
        return self._dt.minute

    @minute.setter
    def minute(self, value):
        self._dt += timedelta(minutes=value - self._dt.minute)

    @property
    def second(self):
        return self._dt.second

    @second.setter
    def second(self, value):
        self._dt += timedelta(seconds=value - self._dt.second)

    @property
    def microsecond(self):
        return self._dt.microsecond

    @microsecond.setter
    def microsecond(self, value):
        self._dt += timedelta(microseconds=value - self._dt.microsecond)

    @property
    def weekday(self):
        return self._dt.weekday()

    @property
    def isoweekday(self):
        return self._dt.isoweekday()

    def today(self):
        return self

    def tomorrow(self):
        return self.shifted(days=1)

    def yesterday(self):
        return self.shifted(days=-1)

    # pred method
    def is_today(self):
        """
        判断对象的时间是不是今天
        :return:
        """
        return self._dt.date() == datetime.today().date()

    def is_past_date(self):
        """
        判断对象的时间是不是过去的时间
        :return:
        """
        return self._dt.date() < datetime.today().date()

    def is_future_date(self):
        """
        判断对象的时间是不是未来的时间
        :return:
        """
        return self._dt.date() > datetime.today().date()

    @property
    def timestamp(self):
        """

        :return:
        """
        # return int(time.mktime(self._dt.timetuple()))+self.microsecond/1000000.0
        return int(time.mktime(self._dt.timetuple()))

    @property
    def days_in_month(self):
        """
        查询本月有多少天
        :return:
        """
        return calendar.monthrange(self.year, self.month)[1]

    @property
    def sqldate(self):
        """
        返回时间的年月日,格式: '2016-08-29'
        :return:
        """
        return self._dt.strftime("%Y-%m-%d")

    @property
    def sqltime(self):
        """
        返回时间的时分秒,格式: '23:26:25'
        :return:
        """
        return self._dt.strftime("%H:%M:%S")

    @property
    def sql(self):
        """
        返回sql格式的年月日时分秒,格式: '2016-08-29 23:26:25'
        :return:
        """
        return '{0} {1}'.format(self.sqldate, self.sqltime)

    def strftime(self, fmt):
        """
        调用datetime对象的strftime对象,返回自定义格式的时间输出
        :param fmt: "%Y-%m-%d %H:%M:%S"  # 该格式,仅参考使用
        :return:
        """
        return self._dt.strftime(fmt)

    @classmethod
    def strptime(cls, timestr, fmt):
        """
        调用datetime的strptime方法,将字符串按照对应的时间格式转化为datetime对象,最后返回自己的blackhole类
        :param timestr: 字符串
        :param fmt: 时间格式
        :return:
        """
        dt = datetime.strptime(timestr, fmt)
        return cls(dt=dt)

    def __add__(self, other):
        if isinstance(other, (timedelta, relativedelta)):
            return self.__class__(dt=self._dt + other)
        raise NotImplementedError()

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self.__class__(dt=self._dt - other)
        elif isinstance(other, datetime):
            return self._dt - other
        elif isinstance(other, Blackhole):
            return self._dt - other._dt
        raise NotImplementedError()

    # comparisons
    def __eq__(self, other):
        if not isinstance(other, (Blackhole, datetime)):
            return False
        if isinstance(other, datetime):
            other = ben(other)
        return self._dt == other._dt

    def __lt__(self, other):
        if not isinstance(other, (Blackhole, datetime)):
            return False
        if isinstance(other, datetime):
            other = ben(other)
        return self._dt < other._dt

    # representation
    def __repr__(self):
        return '<{0} object ({1})>'.format(self.__class__.__name__, self._dt)

    def __str__(self):
        return self.__repr__()


def ben(*args, **kwargs):
    """
    This is a constructors to get Blackhole object.
    Which is very convenient to do conversion
    Usage:
        > ben()
        > ben(timestamp)
        > ben(timestr)
        > ben(datetime)
        > ben(Blackhole)
        > ben('2016-01-01', '%Y-%m-%d')
        > ben(year=2016, month=1, day=1, hour=20)
    """
    if kwargs:
        return Blackhole(*args, **kwargs)

    arg_count = len(args)

    if arg_count == 0:
        return Blackhole.now()
    elif arg_count == 1:
        arg = args[0]

        if isinstance(arg, Blackhole):
            return arg.clone()
        elif isinstance(arg, datetime):
            return Blackhole(dt=arg)
        elif isinstance(arg, (int, float)):
            return Blackhole.fromtimestamp(arg)
        else:
            return Blackhole(dt=timeparse(arg))
    elif arg_count == 2:
        date_str, fmt = args
        return Blackhole.strptime(date_str, fmt)
