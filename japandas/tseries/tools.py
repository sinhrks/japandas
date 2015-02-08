#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import re

import numpy as np
import pandas as pd
import pandas.compat as compat
import pandas.core.common as com


_formats = ['%Y年%m月%d日', '%Y年%m月',
            '%Y年%m月%d日%H時%M分', '%Y年%m月%d日%H時%M分%S秒',

            '%y年%m月%d日', '%y年%m月',
            '%y年%m月%d日%H時%M分', '%y年%m月%d日%H時%M分%S秒',

            '%m月%d日', '%m月%d日%H時%M分', '%m月%d日%H時%M分%S秒']


def to_datetime(arg, box=True, format=None, **kwargs):

    result = pd.to_datetime(arg, box=box, format=format, **kwargs)

    if format is not None:
        # if format is specified, return pd.to_datetime as it is
        return result

    if result is None:
        return result
    elif isinstance(result, (pd.Timestamp, pd.DatetimeIndex)):
        return result

    def _convert_listlike(arg, box):
        for format in _formats:
            try:
                return pd.to_datetime(arg, box=box, format=format, **kwargs)
            except ValueError as e:
                pass
        return arg

    if isinstance(result, compat.string_types):
        arg = np.array([arg], dtype='O')
        result = _convert_listlike(arg, box)
        return result[0]

    if isinstance(result, pd.Series):
        values = _convert_listlike(arg.values, False)
        return Series(values, index=arg.index, name=arg.name)
    elif com.is_list_like(result):
        return _convert_listlike(result, box)
    return result


to_datetime.__doc__ = pd.to_datetime.__doc__