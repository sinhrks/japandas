
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

``Series.str.z2h`` で値を 全角文字から半角文字へ変換、 ``Series.str.h2z`` で値を 半角文字から全角文字へ変換できます。

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

変換の対象とする文字のグループはキーワードオプションで変更できます。それぞれのキーワードについて対象となる文字列は以下の通りです。デフォルトでは全て ``True`` で、全ての文字が変換されます。変換したくないグループがある場合は 対応するキーワードに ``False`` を指定してください。

**補足** ``kana`` には日本語の記号 (句読点) も含まれることに注意してください。

- ``kana``: ``ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノ
  ハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロワヲンヴー・「」。、``
- ``alpha``: ``ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz``
- ``digit``: ``0123456789``
- ``symbol``: ``!"#$%&'()*+,"-./:;<=>?@[\]^_`~{|}``

.. code-block:: python

    >>> s = pd.Series([u'ｱｲｳｴｵ', u'ABC01', u'DE345'])

    # アルファベットは全角にしない
    >>> s.str.h2z(alpha=False)
    0    アイウエオ
    1    ABC０１
    2    DE３４５
    dtype: object

    # カナ、アルファベットは全角にしない
    >>> s.str.h2z(kana=False, alpha=False, digit=True)
    0    ｱｲｳｴｵ
    1    ABC０１
    2    DE３４５
    dtype: object

    # カナ、アルファベット、数値は全角にしない = 記号以外は半角のまま
    >>> s.str.h2z(kana=False, alpha=False, digit=False)
    0    ｱｲｳｴｵ
    1    ABC01
    2    DE345
    dtype: object
