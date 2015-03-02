
文字列処理
==========

Unicode 正規化
--------------

``Series.str.normalize`` は、標準の ``unicodedata.normalize`` と同じ処理を ``Series`` の値に対して行います。

.. code-block:: python

    >>> import pandas as pd
    >>> import japandas as jpd

    >>> s = pd.Series([u'ｱｲｳｴｵ', u'ｶｷｸｹｺ', u'ｶﾞｷﾞｸﾞｹﾞｺﾞ', u'ＡＢＣＤＥ'])
    >>> s
    0         ｱｲｳｴｵ
    1         ｶｷｸｹｺ
    2    ｶﾞｷﾞｸﾞｹﾞｺﾞ
    3         ＡＢＣＤＥ
    dtype: object

    >>> s.str.normalize()
    0    アイウエオ
    1    カキクケコ
    2    ガギグゲゴ
    3    ABCDE
    dtype: object


引数として、``unicodedata.normalize`` と同じフォーマットを渡すことができます。

- ``NFC``: 正規形 C。
- ``NFKC``: 正規形 KC。デフォルト。
- ``NFD``: 正規形 D。
- ``NFKD``: 正規形 KD。

.. code-block:: python

    >>> s.str.normalize('NFD')
    0         ｱｲｳｴｵ
    1         ｶｷｸｹｺ
    2    ｶﾞｷﾞｸﾞｹﾞｺﾞ
    3         ＡＢＣＤＥ
    dtype: object


全角/半角変換
-------------

.. note:: この機能を利用するためには `mojimoji` のインストールが必要です。

``Series.str.zen_to_han`` で値を 全角文字から半角文字へ変換、 ``Series.str.han_to_zen`` で値を 半角文字から全角文字へ変換できます。利用できるオプションなど、詳細は `mojimoji` のドキュメントを参照してください。

https://github.com/studio-ousia/mojimoji

.. code-block:: python

   >>> s = pd.Series([u'ｱｲｳｴｵ', u'ABC01', u'DE345'])
   >>> z = s.str.han_to_zen()
   >>> z
   0    アイウエオ
   1    ＡＢＣ０１
   2    ＤＥ３４５
   dtype: object

   >>> z.str.zen_to_han()
   0    ｱｲｳｴｵ
   1    ABC01
   2    DE345
   dtype: object

.. deprecated:: ``Series.str.z2h``, ``Series.str.h2z`` は deprecate され、将来のバージョンで削除されます。また、一部記号の扱いが ``mojimoji`` では異なります。
