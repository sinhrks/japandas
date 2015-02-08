#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import pandas as pd
import pandas.compat as compat
import pandas.util.testing as tm

import japandas as jpd


class TestDataReader(tm.TestCase):

    def test_to_yahoojp(self):
        idx = pd.DatetimeIndex(['2014-10-01', '2014-10-02', '2014-10-03'], name='日付')
        columns = ['始値', '高値', '安値', '終値', '出来高', '調整後終値*']
        expected = pd.DataFrame({'始値': [6450, 6370, 6231],
                                 '高値': [6559, 6423, 6309],
                                 '安値': [6435, 6256, 6217],
                                 '終値': [6500, 6275, 6290],
                                 '出来高': [14482100, 15240200, 10280100],
                                 '調整後終値*': [6500, 6275, 6290]},
                                index=idx, columns=columns)

        df = jpd.DataReader(7203, 'yahoojp', start='2014-10-01', end='2014-10-05')
        tm.assert_frame_equal(df, expected)

        df = jpd.DataReader(7203, 'yahoojp', start='2014-10-01',
                            end='2014-10-05', interval='d')
        tm.assert_frame_equal(df, expected)

        df = jpd.DataReader(7203, 'yahoojp', start='2014-10-01',
                            end='2014-10-05', interval='v')
        tm.assert_frame_equal(df, expected)

        idx = pd.DatetimeIndex(['2014-10-06', '2014-10-14'], name='日付')
        expected = pd.DataFrame({'始値': [6370, 6050],
                                 '高値': [6455, 6069],
                                 '安値': [6145, 5710],
                                 '終値': [6220, 5731],
                                 '出来高': [51266400, 50540700],
                                 '調整後終値*': [6220, 5731]},
                                index=idx, columns=columns)

        df = jpd.DataReader(7203, 'yahoojp', start='2014-10-01',
                            end='2014-10-15', interval='w')
        tm.assert_frame_equal(df, expected)

        idx = pd.DatetimeIndex(['2014-10-01', '2014-11-01', '2014-12-01'], name='日付')
        expected = pd.DataFrame({'始値': [6450, 6830, 7360],
                                 '高値': [6559, 7314, 7873],
                                 '安値': [5710, 6696, 7107],
                                 '終値': [6498, 7314, 7558],
                                 '出来高': [233353400, 232048700, 244583800],
                                 '調整後終値*': [6498, 7314, 7558]},
                                index=idx, columns=columns)

        df = jpd.DataReader(7203, 'yahoojp', start='2014-10-01',
                            end='2014-12-31', interval='m')
        tm.assert_frame_equal(df, expected)

    def test_data_yahoojp_en(self):
        idx = pd.DatetimeIndex(['2014-10-01', '2014-10-02', '2014-10-03'], name='Date')
        columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
        expected = pd.DataFrame({'始値': [6450, 6370, 6231],
                                 '高値': [6559, 6423, 6309],
                                 '安値': [6435, 6256, 6217],
                                 '終値': [6500, 6275, 6290],
                                 '出来高': [14482100, 15240200, 10280100],
                                 '調整後終値*': [6500, 6275, 6290]},
                                index=idx, columns=columns)

        df = jpd.DataReader(7203, 'yahoojp', start='2014-10-01', end='2014-10-05', en=True)
        tm.assert_frame_equal(df, expected)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
