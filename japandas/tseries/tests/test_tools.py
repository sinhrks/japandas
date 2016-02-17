#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import pandas as pd
import pandas.compat as compat
import pandas.util.testing as tm

import japandas as jpd


class TestTools(tm.TestCase):

    def test_to_datetime(self):
        cases = {'2011年10月30日': ('2011-10-30', '%Y-%m-%d'),
                 '2012年12月': ('2012-12', '%Y-%m'),
                 '12月3日': ('12-03', '%m-%d'),
                 '2013年9月4日10時15分': ('2013-09-04 10:15', '%Y-%m-%d %H:%M'),
                 '10月5日13時25分': ('10-05 13:25', '%m-%d %H:%M'),
                 '2014年3月8日20時45分8秒': ('2014-03-08 20:45:08', '%Y-%m-%d %H:%M:%S'),
                 '3月8日20時45分8秒': ('03-08 20:45:08', '%m-%d %H:%M:%S'),
                 '11年10月30日': ('11-10-30', '%y-%m-%d'),
                 '09年12月': ('09-12', '%y-%m'),
                 '13年9月4日10時15分': ('13-09-04 10:15', '%y-%m-%d %H:%M'),
                 '14年3月8日20時45分8秒': ('14-03-08 20:45:08', '%y-%m-%d %H:%M:%S'),
                 '14年': ('2014-01-01', '%Y-%m-%d'),
                 '2014年': ('2014-01-01', '%Y-%m-%d')
                 }

        for k, (s, f) in compat.iteritems(cases):
            result = jpd.to_datetime(k)
            expected = pd.to_datetime(s, format=f)
            tm.assert_equal(result, expected)

            result = jpd.to_datetime([k])
            expected = pd.to_datetime([s], format=f)
            tm.assert_index_equal(result, expected)

            result = jpd.to_datetime([k], box=False)
            expected = pd.to_datetime([s], format=f, box=False)
            tm.assert_numpy_array_equal(result, expected)

    def test_date_range(self):
        result = jpd.date_range(start='2013年11月15日', end='2014年12月18日', freq='D')
        expected = pd.date_range(start='2013-11-15', end='2014-12-18', freq='D')
        tm.assert_index_equal(result, expected)

        result = jpd.date_range(start='2014年1月15日09時25分', end='2014年1月18日10時45分', freq='M')
        expected = pd.date_range(start='2014-01-15 09:25', end='2014-01-18 10:45', freq='M')
        tm.assert_index_equal(result, expected)

    def test_period_range(self):
        result = jpd.period_range(start='2013年11月15日', end='2014年12月18日', freq='D')
        expected = pd.period_range(start='2013-11-15', end='2014-12-18', freq='D')
        tm.assert_index_equal(result, expected)

        result = jpd.period_range(start='2014年1月15日09時25分', end='2014年1月18日10時45分', freq='M')
        expected = pd.period_range(start='2014-01-15 09:25', end='2014-01-18 10:45', freq='M')
        tm.assert_index_equal(result, expected)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
