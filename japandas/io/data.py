#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

from japandas.io.estat import EStatReader

from pandas_datareader import data


_ohlc_columns_jp = ['始値', '高値', '安値', '終値', '出来高', '調整後終値*']
_ohlc_columns_en = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']


def DataReader(symbols, data_source=None, start=None, end=None, appid=None, **kwargs):
    if data_source == 'yahoojp':
        msg = "YahooJPReaderは削除されました https://www.yahoo-help.jp/app/answers/detail/p/546/a_id/93575"
        raise NotImplementedError(msg)
    elif data_source == 'estat':
        return EStatReader(symbols=symbols, appid=appid, **kwargs).read()
    else:
        return data.DataReader(name=symbols, data_source=data_source,
                               start=start, end=end, **kwargs)


DataReader.__doc__ = data.DataReader.__doc__
