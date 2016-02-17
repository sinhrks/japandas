#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

from pandas_datareader.base import _BaseReader
from japandas.tseries.tools import to_datetime


# http://www.e-stat.go.jp/api/e-stat-manual/

METADATA_MAPPER = {
    # 'TABLE_INF': '統計表ID',
    'STAT_NAME': '政府統計名',
    'GOV_ORG': '作成機関名',
    'STATISTICS_NAME': '提供統計名及び提供分類名',
    'TITLE': '統計表題名及び表番号',
    'CYCLE': '提供周期',
    'SURVEY_DATE': '調査年月',
    'OPEN_DATE': '公開日',
    'SMALL_AREA': '小地域属性フラグ',
    'MAIN_CATEGORY': '統計大分野名',
    'SUB_CATEGORY': '統計小分野名',
    'OVERALL_TOTAL_NUMBER': '総件数',
    'UPDATED_DATE': '最終更新日',
    'id': '統計表ID'
}


class EStatReader(_BaseReader):

    def __init__(self, symbols=None, appid=None, **kwargs):
        if isinstance(symbols, pd.DataFrame):
            if '統計表ID' in symbols.columns:
                symbols = symbols.loc[:, '統計表ID']
            else:
                raise ValueError('DataFrame 中に "統計表ID" カラムがありません')

        super(EStatReader, self).__init__(symbols=symbols, **kwargs)

        if appid is None:
            raise ValueError('アプリケーションID "appid" を文字列で指定してください')
        self.appid = appid

    @property
    def url(self):
        return 'http://api.e-stat.go.jp/rest/2.0/app/getStatsData'

    @property
    def params(self):
        return {'appId': self.appid, 'lang': 'J'}

    def read(self):
        """ read data """
        if isinstance(self.symbols, pd.compat.string_types):
            if len(self.symbols) == 8:
                return self.get_estat_list()

            params = self.params
            params['statsDataId'] = self.symbols
            return self._read_one_data(self.url, params)

        elif pd.core.common.is_list_like(self.symbols):
            dfs = []
            for symbol in self.symbols:
                params = self.params
                params['statsDataId'] = symbol
                df = self._read_one_data(self.url, params)
                dfs.append(df)

            if len(dfs) == 0:
                raise ValueError('取得するIDがありません')
            elif len(dfs) == 1:
                return dfs[0]
            else:
                return dfs[0].append(dfs[1:])
        else:
            raise ValueError('IDは文字列もしくはそのリストで指定してください')

    def _read_lines(self, out):
        root = ET.fromstring(out.getvalue())
        # retrieve class
        class_names = {}   # mapping from class id to name
        class_codes = {}   # mapping from class id to codes
        for c in root.findall('.//CLASS_OBJ'):
            class_id = c.attrib['id']
            class_names[class_id] = c.attrib['name']

            mapper = {}
            for code in c.findall('CLASS'):
                mapper[code.attrib['code']] = code.attrib['name']
            class_codes[class_id] = mapper

        # retrieve values
        values = []
        for value in root.findall('.//VALUE'):
            row = {}
            for cat in class_codes:
                name = class_names[cat]
                code = value.attrib[cat]
                row[name] = class_codes[cat][code]

            if value.text in ('-', ):
                # avoid to_numeric fails
                row['value'] = np.nan
            else:
                row['value'] = value.text
            values.append(row)

        df = pd.DataFrame(values)
        df.loc[:, 'value'] = pd.to_numeric(df['value'], errors='ignore')

        if 'time' in class_names:
            df = df.set_index(class_names['time'])
            df.index = to_datetime(df.index)
        return df

    def get_estat_list(self):
        url = 'http://api.e-stat.go.jp/rest/2.0/app/getStatsList'
        params = {'appId': self.appid, 'lang': 'J', 'statsCode': self.symbols}

        out = self._read_url_as_StringIO(url, params=params)
        root = ET.fromstring(out.getvalue())

        values = []
        columns = []
        for table in root.findall('.//TABLE_INF'):
            columns = ['統計表ID']
            row = {'統計表ID': table.get('id')}
            for elem in table.iter():
                if elem.tag == 'TABLE_INF':
                    continue

                if elem.tag in ('UPDATED_DATE', 'OPEN_DATE'):
                    val = pd.to_datetime(elem.text)
                elif elem.tag == 'SURVEY_DATE':
                    # Almost impossible to parse SURVEY_DATE as Timestamp...
                    val = elem.text
                elif elem.tag == 'OVERALL_TOTAL_NUMVER':
                    val = pd.to_numeric(elem.text)
                else:
                    val = elem.text
                label = METADATA_MAPPER.get(elem.tag, elem.tag)
                columns.append(label)
                row[label] = val
            values.append(row)

        if len(values) == 0:

            try:
                # if msg can be extracted from XML, raise it
                root = ET.fromstring(out.getvalue())
                msg = root.find('RESULT').find('ERROR_MSG').text
            except Exception:
                # otherwie, raise all XML content
                raise ValueError(out.getvalue())
            raise ValueError(msg.encode('utf-8', 'replace'))

        df = pd.DataFrame(values, columns=columns)
        return df
