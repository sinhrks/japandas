#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import datetime
import os

import pandas.compat as compat
import pandas.tseries.holiday as holiday


current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, 'data', 'holidays.pkl')
tse_data_path = os.path.join(current_dir, 'data', 'tseholidays.pkl')


def _read_rules(path):
    if os.path.exists(path):
        with open(path, mode='rb') as f:
            rules = compat.cPickle.load(f)
    elif __name__ != '__main__':
        raise ImportError("Unable to load '{0}'".format(path))
    else:
        rules = None
    return rules


rules = _read_rules(data_path)
tse_rules = _read_rules(tse_data_path)


class JapaneseHolidayCalendar(holiday.AbstractHolidayCalendar):
    rules = rules


class TSEHolidayCalendar(holiday.AbstractHolidayCalendar):
    rules = tse_rules


# register to pandas factory
holiday.register(JapaneseHolidayCalendar)
holiday.register(TSEHolidayCalendar)


if __name__ == '__main__':

    # https://github.com/k1LoW/holiday_jp
    import yaml

    def to_pickle(dates, path):
        rules = []
        keys = sorted(compat.iterkeys(dates))
        for key in keys:
            value = dates[key]
            dt = value['date']
            h = holiday.Holiday(value['name'], dt.year, month=dt.month, day=dt.day)
            rules.append(h)
        print(len(rules))
        with open(path, mode='w') as w:
            compat.cPickle.dump(rules, w)
            print('pickled {0} data'.format(len(dates)))

    with open(os.path.join('data', 'holidays.yml'), mode='r') as f:
        data = yaml.load(f)
    # JapaneseHolidayCalendar
    to_pickle(data, data_path)

    tse_data = data.copy()
    for y in range(1970, 2031):
        for m, d in [(1, 1), (1, 2), (1, 3), (12, 31)]:
            dt = datetime.date(y, m, d)
            if dt not in tse_data:
                tse_data[dt] = {'name': '年末年始休業日', 'date': dt}

    # TSEHolidayCalendar
    to_pickle(tse_data, tse_data_path)
