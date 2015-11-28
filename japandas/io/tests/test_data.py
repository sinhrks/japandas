#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os

import pandas as pd
import pandas.compat as compat
import pandas.util.testing as tm
from pandas.tests.test_graphics import TestPlotBase, _check_plot_works

import japandas as jpd


class TestDataReader(TestPlotBase):

    def test_to_yahoojp(self):
        idx = pd.DatetimeIndex(['2014-10-01', '2014-10-02', '2014-10-03'], name='日付')
        columns = jpd.io.data._ohlc_columns_jp
        expected = pd.DataFrame({'始値': [6450, 6370, 6231],
                                 '高値': [6559, 6423, 6309],
                                 '安値': [6435, 6256, 6217],
                                 '終値': [6500, 6275, 6290],
                                 '出来高': [14482100, 15240200, 10280100],
                                 '調整後終値*': [6500, 6275, 6290]},
                                index=idx, columns=columns)

        df = jpd.DataReader(7203, 'yahoojp', start='2014-10-01', end='2014-10-05')
        tm.assert_frame_equal(df, expected)
        _check_plot_works(df.plot, kind='ohlc')

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
        columns = jpd.io.data._ohlc_columns_en
        expected = pd.DataFrame({'Open': [6450, 6370, 6231],
                                 'High': [6559, 6423, 6309],
                                 'Low': [6435, 6256, 6217],
                                 'Close': [6500, 6275, 6290],
                                 'Volume': [14482100, 15240200, 10280100],
                                 'Adj Close': [6500, 6275, 6290]},
                                index=idx, columns=columns)

        df = jpd.DataReader(7203, 'yahoojp', start='2014-10-01', end='2014-10-05', en=True)
        tm.assert_frame_equal(df, expected)
        _check_plot_works(df.plot, kind='ohlc')

    def test_data_estat_error(self):
        with tm.assertRaises(ValueError):
            # no app ID
            jpd.DataReader('00200521', 'estat', appid=None)

        ESTAT_KEY = os.environ['ESTAT']

        with tm.assertRaises(ValueError):
            # blank list
            jpd.DataReader([], 'estat', appid=ESTAT_KEY)

        with tm.assertRaises(ValueError):
            # invalid type
            jpd.DataReader(1, 'estat', appid=ESTAT_KEY)

    def test_data_estat_list(self):

        ESTAT_KEY = os.environ['ESTAT']
        df = jpd.DataReader('00200521', 'estat', appid=ESTAT_KEY)

        exp_columns = pd.Index([u'統計表ID', u'政府統計名',
                                u'作成機関名', u'提供統計名及び提供分類名',
                                u'統計表題名及び表番号', u'提供周期', u'調査年月',
                                u'公開日', u'小地域属性フラグ', u'統計大分野名',
                                u'統計小分野名', u'総件数', u'最終更新日'],)
        self.assert_index_equal(df.columns, exp_columns)

    def test_data_estat_data(self):

        ESTAT_KEY = os.environ['ESTAT']
        df = jpd.DataReader('0000030001', 'estat', appid=ESTAT_KEY)

        exp = pd.DataFrame({u'value': [117060396, 89187409, 27872987, 5575989, 1523907],
                            u'全国都道府県030001': [u'全国', u'全国市部', u'全国郡部', u'北海道', u'青森県'],
                            u'全域・集中の別030002': [u'全域'] * 5,
                            u'年齢５歳階級Ａ030002': [u'総数'] * 5,
                            u'男女Ａ030001': [u'男女総数'] * 5},
                           index=pd.Index([u'1980年'] * 5, name=u'時間軸(年次)'))
        self.assert_frame_equal(df.head(), exp)

        df = jpd.DataReader(['0000030001', '0000030002'], 'estat', appid=ESTAT_KEY)
        self.assertIsInstance(df, pd.DataFrame)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
