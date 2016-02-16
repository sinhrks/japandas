#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import numpy as np
import pandas as pd
import pandas.compat as compat
import pandas.core.common as com


_formats = ['%Y年', '%Y年%m月%d日', '%Y年%m月',
            '%Y年%m月%d日%H時%M分', '%Y年%m月%d日%H時%M分%S秒',

            '%y年', '%y年%m月%d日', '%y年%m月',
            '%y年%m月%d日%H時%M分', '%y年%m月%d日%H時%M分%S秒',

            '%m月%d日', '%m月%d日%H時%M分', '%m月%d日%H時%M分%S秒']


def to_datetime(arg, box=True, format=None, **kwargs):

    try:
        result = pd.to_datetime(arg, box=box, format=format, **kwargs)

        if format is not None:
            # if format is specified, return pd.to_datetime as it is
            return result

        if result is None:
            return result
        elif isinstance(result, (pd.Timestamp, pd.DatetimeIndex)):
            return result
    except ValueError:
        # as of pandas 0.17, to_datetime raises when parsing fails
        result = arg

    def _convert_listlike(arg, box):
        for format in _formats:
            try:
                return pd.to_datetime(arg, box=box, format=format, **kwargs)
            except ValueError:
                pass
        return arg

    if isinstance(result, compat.string_types):
        arg = np.array([arg], dtype='O')
        result = _convert_listlike(arg, box)
        return result[0]

    if isinstance(result, pd.Series):
        values = _convert_listlike(arg.values, False)
        return pd.Series(values, index=arg.index, name=arg.name)
    elif com.is_list_like(result):
        return _convert_listlike(result, box)
    return result


def date_range(start=None, end=None, **kwargs):
    start = to_datetime(start)
    end = to_datetime(end)
    return pd.date_range(start=start, end=end, **kwargs)


def period_range(start=None, end=None, **kwargs):
    start = to_datetime(start)
    end = to_datetime(end)
    return pd.period_range(start=start, end=end, **kwargs)


to_datetime.__doc__ = pd.to_datetime.__doc__
date_range.__doc__ = pd.date_range.__doc__
period_range.__doc__ = pd.period_range.__doc__


"""
try:
    import pandas.tseries.timedeltas as timedeltas
    abbrevs = [('d' ,'days|d|day|日'),
               ('h' ,'hours|h|hour|時間'),
               ('m' ,'minutes|min|minute|m|分'),
               ('s' ,'seconds|sec|second|s|秒'),
               ('ms','milliseconds|milli|millis|millisecond|ms'),
               ('us','microseconds|micro|micros|microsecond|us'),
               ('ns','nanoseconds|nano|nanos|nanosecond|ns')]
    timedeltas.abbrevs = abbrevs
except Exception:
    pass
"""
