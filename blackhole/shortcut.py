# coding=utf-8

from datetime import datetime
from blackhole import Blackhole, ben

__all__ = ['tslice']


def tslice(unit, start=ben(), end=None, step=1, count=float('inf')):
    """
    tslice(unit, start=None, end=None, step=1, count=None) -> generator of Blackhole object
    unit in ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']
    this is some kind xrange-like
    :param unit:
    :param start:
    :param end:
    :param step:
    :param count:
    :return:
    """
    if unit not in Blackhole._units:
        raise AttributeError()
    if isinstance(start, basestring):
        start = ben(start)
    if isinstance(end, basestring):
        end = ben(end)

    cnt = 0
    if step > 0:
        end = end or ben(datetime.max)
        while start < end and cnt < count:
            yield start
            start = start.shifted(**{unit: step})
            cnt += 1
    elif step < 0:
        end = end or ben(datetime.min)
        while start > end and cnt < count:
            yield start
            start = start.shifted(**{unit: step})
            cnt += 1
