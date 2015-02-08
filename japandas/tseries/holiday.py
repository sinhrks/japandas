#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import pandas.compat as compat
import pandas.tseries.holiday as holiday

holiday.Holiday

if __name__ == '__main__':

    # https://github.com/k1LoW/holiday_jp

    import os
    import yaml

    f = open(os.path.join('data', 'holidays.yml'))
    data = yaml.load(f)
    for k, v in compat.iteritems(data):
        dt = v['date']
        h = holiday.Holiday(v['name_en'], dt.year, month=dt.month, day=dt.day)
        print(h)
