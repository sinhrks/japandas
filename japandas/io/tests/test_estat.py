#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import os

import numpy as np
import pandas as pd
import pandas.util.testing as tm
import japandas as jpd


class TestEstat(tm.TestCase):

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

        exp_columns = pd.Index(['統計表ID', '政府統計名',
                                '作成機関名', '提供統計名及び提供分類名',
                                '統計表題名及び表番号', '提供周期', '調査年月',
                                '公開日', '小地域属性フラグ', '統計大分野名',
                                '統計小分野名', '総件数', '最終更新日'],)
        self.assert_index_equal(df.columns, exp_columns)

        target = df.head(n=3)
        df = jpd.DataReader(target, 'estat', appid=ESTAT_KEY)
        self.assertIsInstance(df, pd.DataFrame)

        df = jpd.DataReader('00200523', 'estat', appid=ESTAT_KEY)
        self.assert_index_equal(df.columns, exp_columns)

    def test_data_estat_list_all(self):
        # 以下 すべての提供データをテスト
        # http://www.e-stat.go.jp/api/api-data/

        targets = ['00200521', '00200522', '00200523', '00200524', '00200531',
                   '00200532', '00200533', '00200541', '00200543', '00200544',
                   '00200545', '00200551', '00200552', '00200553', '00200561',
                   '00200563', '00200564', '00200565', '00200566', '00200571',
                   '00200572', '00200573',    # '00200511', '00200502', (no data found)
                   '00250011']
        for target in targets:
            self._assert_target(target)

    def test_data_estat_list_all2(self):
        # Travis CI でのタイムアウトを防ぐため分割
        targets = ['00350600', '00350620', '00351000', '00400001', '00400002',
                   '00400003', '00400004', '00400202', '00450011', '00450012',
                   '00450021', '00450022', '00450061', '00450071', '00450091',
                   '00450151', '00500201', '00500209', '00500215', '00500216',
                   '00500217', '00500225', '00550010', '00550020', '00550030',
                   '00550040', '00550100', '00550200', '00550210', '00551020',
                   '00551130', '00600330', '00600470', '00600480']
        for target in targets:
            self._assert_target(target)

    def _assert_target(self, target):
        ESTAT_KEY = os.environ['ESTAT']

        df = jpd.DataReader(target, 'estat', appid=ESTAT_KEY)
        exp_columns = pd.Index(['統計表ID', '政府統計名',
                                '作成機関名', '提供統計名及び提供分類名',
                                '統計表題名及び表番号', '提供周期', '調査年月',
                                '公開日', '小地域属性フラグ', '統計大分野名',
                                '統計小分野名', '総件数', '最終更新日'],)
        self.assert_index_equal(df.columns, exp_columns)

        target = df.head(n=3)
        df = jpd.DataReader(target, 'estat', appid=ESTAT_KEY)
        self.assertIsInstance(df, pd.DataFrame)

    def test_data_estat_data(self):

        ESTAT_KEY = os.environ['ESTAT']
        df = jpd.DataReader('0000030001', 'estat', appid=ESTAT_KEY)

        exp = pd.DataFrame({'value': [117060396, 89187409, 27872987, 5575989, 1523907],
                            '全国都道府県030001': ['全国', '全国市部', '全国郡部', '北海道', '青森県'],
                            '全域・集中の別030002': ['全域'] * 5,
                            '年齢５歳階級Ａ030002': ['総数'] * 5,
                            '男女Ａ030001': ['男女総数'] * 5},
                           index=pd.DatetimeIndex(['1980-01-01'] * 5, name='時間軸(年次)'))
        self.assert_frame_equal(df.head(), exp)

        df = jpd.DataReader(['0000030001', '0000030002'], 'estat', appid=ESTAT_KEY)
        self.assertIsInstance(df, pd.DataFrame)

        df = jpd.DataReader("0002180001", 'estat', appid=ESTAT_KEY)
        exp = pd.DataFrame({'value': [445007, 194243, 199623, 203464, 190711],
                            '全国・都道府県・大都市': ['全国'] * 5,
                            '性別': ['総数'] * 5,
                            '表章項目': ['都道府県（自都市）内移動者数'] * 5},
                           index=pd.DatetimeIndex(['2009-03-01', '2009-02-01', '2009-01-01',
                                                   '2008-12-01', '2008-11-01'], name='時間軸（月次）'))
        self.assert_frame_equal(df.head(), exp)

    def test_data_estat_data_numeric(self):
        ESTAT_KEY = os.environ['ESTAT']
        df = jpd.DataReader('0003109612', 'estat', appid=ESTAT_KEY)
        self.assertEqual(df['value'].dtype, np.float64)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
