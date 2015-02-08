#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os
import pandas.compat as compat
import pandas.tseries.holiday as holiday
import pandas.util.testing as tm


current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, 'data', 'holidays.pkl')

if os.path.exists(data_path):
    f = open(data_path, mode='rb')
    rules = compat.cPickle.load(f)

elif __name__ != '__main__':
    raise ImportError("Unable to load 'holidays.pkl'")


class JapaneseHolidayCalendar(holiday.AbstractHolidayCalendar):
        rules = rules


if __name__ == '__main__':

    # https://github.com/k1LoW/holiday_jp

    import collections
    import yaml

    f = open(os.path.join('data', 'holidays.yml'), mode='r')
    data = yaml.load(f)
    f.close()
    keys = sorted(compat.iterkeys(data))

    rules = []

    for key in keys:
        value = data[key]

        dt = value['date']
        h = holiday.Holiday(value['name_en'], dt.year, month=dt.month, day=dt.day)
        rules.append(h)

    w = open(data_path, mode='w')
    compat.cPickle.dump(rules, w)
    w.close()
