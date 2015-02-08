#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import datetime

import pandas as pd
import pandas.compat as compat
import pandas.util.testing as tm

import japandas as jpd


class TestCalendar(tm.TestCase):

    def setUp(self):
        self.expected = [datetime.datetime(2014, 1, 1, 0, 0),
                         datetime.datetime(2014, 1, 13, 0, 0),
                         datetime.datetime(2014, 2, 11, 0, 0),
                         datetime.datetime(2014, 3, 21, 0, 0),
                         datetime.datetime(2014, 4, 29, 0, 0),
                         datetime.datetime(2014, 5, 3, 0, 0),
                         datetime.datetime(2014, 5, 4, 0, 0),
                         datetime.datetime(2014, 5, 5, 0, 0),
                         datetime.datetime(2014, 5, 6, 0, 0),
                         datetime.datetime(2014, 7, 21, 0, 0),
                         datetime.datetime(2014, 9, 15, 0, 0),
                         datetime.datetime(2014, 9, 23, 0, 0),
                         datetime.datetime(2014, 10, 13, 0, 0),
                         datetime.datetime(2014, 11, 3, 0, 0),
                         datetime.datetime(2014, 11, 23, 0, 0),
                         datetime.datetime(2014, 11, 24, 0, 0),
                         datetime.datetime(2014, 12, 23, 0, 0)]

        self.start_date = datetime.datetime(2014, 1, 1)
        self.end_date = datetime.datetime(2014, 12, 31)

    def test_calendar(self):

        calendar = jpd.JapaneseHolidayCalendar()
        holidays_0 = calendar.holidays(self.start_date,
                                       self.end_date)

        holidays_1 = calendar.holidays(
                        self.start_date.strftime('%Y-%m-%d'),
                        self.end_date.strftime('%Y-%m-%d'))
        holidays_2 = calendar.holidays(
                        pd.Timestamp(self.start_date),
                        pd.Timestamp(self.end_date))

        self.assertEqual(holidays_0.to_pydatetime().tolist(), self.expected)
        self.assertEqual(holidays_1.to_pydatetime().tolist(), self.expected)
        self.assertEqual(holidays_2.to_pydatetime().tolist(), self.expected)

    def test_cday(self):
        calendar = jpd.JapaneseHolidayCalendar()
        cday = pd.offsets.CDay(calendar=calendar)

        dt = datetime.datetime(2014, 1, 12)
        tm.assert_equal(dt - cday, datetime.datetime(2014, 1, 10))
        tm.assert_equal(dt + cday, datetime.datetime(2014, 1, 14))

        dt = datetime.datetime(2014, 1, 10)
        tm.assert_equal(dt - cday, datetime.datetime(2014, 1, 9))
        tm.assert_equal(dt + cday, datetime.datetime(2014, 1, 14))

        dt = datetime.datetime(2014, 4, 28)
        tm.assert_equal(dt - cday, datetime.datetime(2014, 4, 25))
        tm.assert_equal(dt + cday, datetime.datetime(2014, 4, 30))

        dt = datetime.datetime(2014, 5, 3)
        tm.assert_equal(dt - cday, datetime.datetime(2014, 5, 2))
        tm.assert_equal(dt + cday, datetime.datetime(2014, 5, 7))

        dt = datetime.datetime(2014, 5, 6)
        cday = pd.offsets.CDay(calendar=calendar)
        tm.assert_equal(dt - cday, datetime.datetime(2014, 5, 2))
        tm.assert_equal(dt + cday, datetime.datetime(2014, 5, 7))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
