#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import time

import pandas as pd
from japandas.io.estat import EStatReader

from pandas_datareader import data
from pandas_datareader.yahoo.daily import YahooDailyReader


_ohlc_columns_jp = ['始値', '高値', '安値', '終値', '出来高', '調整後終値*']
_ohlc_columns_en = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']


_SLEEP_TIME = 0.5


class YahooJPReader(YahooDailyReader):

    def __init__(self, en=False, **kwargs):
        super(YahooJPReader, self).__init__(**kwargs)
        self.en = en

    @property
    def url(self):
        return 'http://info.finance.yahoo.co.jp/history/'

    def _get_params(self, symbol):
        params = {
            'code': symbol,
            'sm': self.start.month,
            'sd': self.start.day,
            'sy': self.start.year,
            'em': self.end.month,
            'ed': self.end.day,
            'ey': self.end.year,
            'tm': self.interval,
            'p': 1
        }
        return params

    def read(self):
        # Use _DailyBaseReader's definition
        df = self._read_one_data(self.url, params=self._get_params(self.symbols))
        return df

    def _read_one_data(self, url, params):
        base = (url + '?code={code}.T&sy={sy}&sm={sm}&sd={sd}&'
                'ey={ey}&em={em}&ed={ed}&tm={tm}&p={p}')
        results = []
        while True:
            url = base.format(**params)
            tables = pd.read_html(url, header=0)
            if len(tables) < 2 or len(tables[1]) == 0:
                break
            results.append(tables[1])
            params['p'] = params['p'] + 1
            time.sleep(_SLEEP_TIME)
        result = pd.concat(results, ignore_index=True)

        if self.en:
            result.columns = ['Date'] + _ohlc_columns_en
            dtkey = 'Date'
        else:
            dtkey = '日付'

        if self.interval == 'm':
            result[dtkey] = pd.to_datetime(result[dtkey], format='%Y年%m月')
        else:
            result[dtkey] = pd.to_datetime(result[dtkey], format='%Y年%m月%d日')
        result = result.set_index(dtkey)
        result = result.sort_index()
        return result


def DataReader(symbols, data_source=None, start=None, end=None, appid=None, **kwargs):
    if data_source == 'yahoojp':
        return YahooJPReader(symbols=symbols, start=start,
                             end=end, **kwargs).read()
    elif data_source == 'estat':
        return EStatReader(symbols=symbols, appid=appid, **kwargs).read()
    else:
        return data.DataReader(name=symbols, data_source=data_source,
                               start=start, end=end, **kwargs)


DataReader.__doc__ = data.DataReader.__doc__


if __name__ == '__main__':
    toyota_tse = DataReader(7203, 'yahoojp', start='2014-10-01')
    print(toyota_tse.head())
