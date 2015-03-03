
日時処理
========

日本語日付のパース
------------------

``jpd.to_datetime`` で 日本語の日付をパースできます。引数が単一の文字列の場合、結果は ``Timestamp`` に、リストや ``np.array`` の場合は ``DatetimeIndex`` になります。この挙動は ``pd.to_datetime`` と同様です。

.. code-block:: python

    >>> import pandas as pd
    >>> import japandas as jpd

    >>> jpd.to_datetime(u'2014年11月30日')
    Timestamp('2014-11-30 00:00:00')

    >>> jpd.to_datetime([u'2014年11月30日13時25分', u'2014年11月30日14時38分'])
    <class 'pandas.tseries.index.DatetimeIndex'>
    [2014-11-30 13:25:00, 2014-11-30 14:38:00]
    Length: 2, Freq: None, Timezone: None


同様に、``jpd.date_range``, ``jpd.period_range`` でも 日本語の日付をパースすることができます。それ以外の挙動は ``pd.date_range``, ``pd.period_range`` と同様です。

.. code-block:: python

    >>> jpd.date_range(start=u'2013年12月01日', end=u'2014年12月01日', freq='D')
    <class 'pandas.tseries.index.DatetimeIndex'>
    [2013-12-01, ..., 2014-12-01]
    Length: 366, Freq: D, Timezone: None

    >>> jpd.period_range(start=u'2013年12月01日', end=u'2014年12月01日', freq='M')
    <class 'pandas.tseries.period.PeriodIndex'>
    [2013-12, ..., 2014-12]
    Length: 13, Freq: M


日本の祝日カレンダー
--------------------

`japandas` では以下 2 種類のカレンダークラスを定義しています。

- ``japandas.JapaneseHolidayCalendar``: 1970 年から 2030 年までの日本の祝日を定義したカレンダークラスです。
- ``japandas.TSEHolidayCalendar``: 1970 年から 2030 年までの東京証券取引所の休業日 (日本の祝日 + 年末年始 12/31 - 1/3) を定義したカレンダークラスです。

定義された祝日の一覧は、それぞれ ``Calendar.holidays()`` メソッドで確認することができます。

.. code-block:: python

    >>> calendar = jpd.JapaneseHolidayCalendar()
    >>> calendar.holidays()
    <class 'pandas.tseries.index.DatetimeIndex'>
    [1970-01-01, ..., 2030-12-23]
    Length: 969, Freq: None, Timezone: None


このカレンダーと ``pd.offsets.CDay`` クラスを利用すると、カレンダーの定義に従って営業日の計算を行うことができます。

.. code-block:: python

    >>> cday = pd.offsets.CDay(calendar=calendar)

    >>> import datetime
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


また、カレンダーの定義を条件として ``DataFrame`` や ``Series`` からレコードを抽出することができます。以下の例では、それぞれカレンダー上で営業日となっているレコードの抽出 / 休日となっているレコードの抽出を行っています。

**補足** 対象とするデータは ``DatetimeIndex`` を持っている必要があります。

.. code-block:: python

    >>> df = pd.DataFrame(np.random.randn(10, 3),
                          index=jpd.date_range(u'2014年5月1日', u'2014年5月10日', freq='D'))
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

    # カレンダー上 休日のレコードを抽出
    >>> df[~df.index.isin(indexer)]
                       0         1         2
    2014-05-03  0.473370 -1.282504  0.380449
    2014-05-04  0.215411  0.220587 -1.088699
    2014-05-05  0.286348 -1.069165 -1.471871
    2014-05-06 -0.665438 -0.402046 -1.008051
    2014-05-10 -0.910188  0.294136  0.020730
