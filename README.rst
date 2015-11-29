japandas
========

.. image:: https://img.shields.io/pypi/v/japandas.svg
    :target: https://pypi.python.org/pypi/japandas/
.. image:: https://readthedocs.org/projects/japandas/badge/?version=latest
    :target: http://japandas.readthedocs.org/en/latest/
    :alt: Latest Docs
.. image:: https://travis-ci.org/sinhrks/japandas.svg?branch=master
    :target: https://travis-ci.org/sinhrks/japandas
.. image:: https://coveralls.io/repos/sinhrks/japandas/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/sinhrks/japandas?branch=master

Overview
~~~~~~~~

pandas Japanese extension.

pandas の日本語拡張。以下の機能を提供する。

- 日本語の日付のパース
- 日本の祝日カレンダーと、それを利用した営業日計算
- 文字列の全角/半角変換
- Yahoo! ファイナンスからの日本の株式情報取得
- e-Stat からのデータの取得
- ローソク足チャート

**補足** このパッケージでは、"日本固有の機能であり本流に実装される可能性が低いもの", もしくは"それらに関係し本流に実装される可能性が低いもの" を実装 / メンテナンスする。


インストール
~~~~~~~~~~

.. code-block:: sh

    pip install japandas

ドキュメント
~~~~~~~~~~

- 開発版: http://japandas.readthedocs.org/en/latest/
- リリース版: http://japandas.readthedocs.org/en/stable/

機能概要
~~~~~~~

日本語の日付のパース
,,,,,,,,,,,,,,,,,

.. code-block:: python

    >>> import japandas as jpd
    >>> jpd.to_datetime('2014年11月30日')
    Timestamp('2014-11-30 00:00:00')

    >>> jpd.to_datetime(['2014年11月30日13時25分', '2014年11月30日14時38分'])
    <class 'pandas.tseries.index.DatetimeIndex'>
    [2014-11-30 13:25:00, 2014-11-30 14:38:00]
    Length: 2, Freq: None, Timezone: None

    >>> jpd.date_range(start=u'2013年12月01日', end=u'2014年12月01日', freq='D')
    <class 'pandas.tseries.index.DatetimeIndex'>
    [2013-12-01, ..., 2014-12-01]
    Length: 366, Freq: D, Timezone: None


日本の祝日カレンダーと、それを利用した営業日計算
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

.. code-block:: python

    >>> import pandas as pd
    >>> import datetime

    >>> calendar = jpd.JapaneseHolidayCalendar()
    >>> cday = pd.offsets.CDay(calendar=calendar)

    >>> datetime.datetime(2014, 4, 28) + cday
    # 4/29は祝日(昭和の日)
    Timestamp('2014-04-30 00:00:00')

    >>> datetime.datetime(2014, 4, 28) - cday
    # 4/26は土曜日, 4/27は日曜日
    Timestamp('2014-04-25 00:00:00')

    >>> datetime.datetime(2014, 5, 3) + cday
    # 5/4は日曜日, 5/5は祝日(こどもの日), 5/6は祝日(みどりの日/振替休日)
    Timestamp('2014-05-07 00:00:00')

    >>> datetime.datetime(2014, 5, 3) - cday
    # 5/3は土曜日
    Timestamp('2014-05-02 00:00:00')

    # 適当なデータを作成
    >>> df = pd.DataFrame(np.random.randn(10, 3),
    ...                   index=jpd.date_range(u'2014年5月1日', u'2014年5月10日', freq='D'))
    >>> df
                       0         1         2
    2014-05-01  0.762453 -1.418762 -0.150073
    2014-05-02  0.966500 -0.473888  0.272871
    2014-05-03  0.473370 -1.282504  0.380449
    2014-05-04  0.215411  0.220587 -1.088699
    2014-05-05  0.286348 -1.069165 -1.471871
    2014-05-06 -0.665438 -0.402046 -1.008051
    2014-05-07  1.173935  2.080087 -2.279285
    2014-05-08 -0.957195  0.746798  0.092214
    2014-05-09 -0.259276 -0.775489  0.572525
    2014-05-10 -0.910188  0.294136  0.020730

    >>> cday = pd.offsets.CDay(calendar=calendar)
    >>> indexer = jpd.date_range(u'2014年5月1日', u'2014年5月10日', freq=cday)

    # カレンダー上 営業日のレコードを抽出
    >>> df.ix[indexer]
                       0         1         2
    2014-05-01  0.762453 -1.418762 -0.150073
    2014-05-02  0.966500 -0.473888  0.272871
    2014-05-07  1.173935  2.080087 -2.279285
    2014-05-08 -0.957195  0.746798  0.092214
    2014-05-09 -0.259276 -0.775489  0.572525


全角/半角変換
,,,,,,,,,,,

.. code-block:: python

   >>> s = pd.Series([u'ｱｲｳｴｵ', u'ABC01', u'DE345'])
   >>> z = s.str.h2z()
   >>> z
   0    アイウエオ
   1    ＡＢＣ０１
   2    ＤＥ３４５
   dtype: object

   >>> z.str.z2h()
   0    ｱｲｳｴｵ
   1    ABC01
   2    DE345
   dtype: object


Yahoo! ファイナンスからの日本の株式情報取得
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,


.. code-block:: python

    >>> df = jpd.DataReader(7203, 'yahoojp', start='2014-10-01', end='2014-10-05')
    >>> df
                  始値    高値    安値    終値       出来高  調整後終値*
    日付
    2014-10-01  6450  6559  6435  6500  14482100    6500
    2014-10-02  6370  6423  6256  6275  15240200    6275
    2014-10-03  6231  6309  6217  6290  10280100    6290

e-Stat からの統計情報取得
,,,,,,,,,,,,,,,,,,,,,,,

.. code-block:: python

    >>> key = "your application id"
    >>> df = jpd.DataReader("0000030001", 'estat', appid=key)
    >>> df.head()
                 value 全国都道府県030001 全域・集中の別030002 年齢５歳階級Ａ030002 男女Ａ030001
    時間軸(年次)
    1980年    117060396           全国            全域            総数      男女総数
    1980年     89187409         全国市部            全域            総数      男女総数
    1980年     27872987         全国郡部            全域            総数      男女総数
    1980年      5575989          北海道            全域            総数      男女総数
    1980年      1523907          青森県            全域            総数      男女総数


ローソク足チャート
,,,,,,,,,,,,,,,,,

.. code-block:: python

    >>> df.plot(kind='ohlc')
    チャート省略


License
~~~~~~~

BSD.

日本の祝日データソースとして以下を利用。

- `komagata/holiday_jp <https://github.com/komagata/holiday_jp>`_

  Copyright (c) 2009 Masaki Komagata. See `LICENSE <https://github.com/komagata/holiday_jp/blob/master/LICENSE>`_ for details.

- `k1LoW/holiday_jp <https://github.com/k1LoW/holiday_jp>`_

  MIT.

