#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import unicodedata

import pandas as pd
import pandas.compat as compat
import pandas.core.common as com

import pandas.core.strings as strings


# requires special handling
_HSOUNDMARK = ['ｶﾞ', 'ｷﾞ', 'ｸﾞ', 'ｹﾞ', 'ｺﾞ',
               'ｻﾞ', 'ｼﾞ', 'ｽﾞ', 'ｾﾞ', 'ｿﾞ',
               'ﾀﾞ', 'ﾁﾞ', 'ﾂﾞ', 'ﾃﾞ', 'ﾄﾞ',
               'ﾊﾞ', 'ﾋﾞ', 'ﾌﾞ', 'ﾍﾞ', 'ﾎﾞ',
               'ﾊﾟ', 'ﾋﾟ', 'ﾌﾟ', 'ﾍﾟ', 'ﾎﾟ', 'ｳﾞ']

_HKANA = 'ｧｱｨｲｩｳｪｴｫｵｶｷｸｹｺｻｼｽｾｿﾀﾁｯﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓｬﾔｭﾕｮﾖﾗﾘﾙﾚﾛﾜｦﾝﾞｰ･｢｣｡､'
_ZALPHA = ('ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'
           'ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ')
_ZSYMBOL = '！＂＃＄％＆＇（）＊＋，－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～　'
_ZDIGIT = '０１２３４５６７８９'

# mapping from full-width to half width
_KANA_MAPPER = {unicodedata.normalize('NFKC', c): c for c in _HKANA}
_ALPHA_MAPPER = {c: unicodedata.normalize('NFKC', c) for c in _ZALPHA}
_DIGIT_MAPPER = {c: unicodedata.normalize('NFKC', c) for c in _ZDIGIT}
_SYMBOL_MAPPER = {c: unicodedata.normalize('NFKC', c) for c in _ZSYMBOL}


def _reverse_dict(dict):
    return {v: k for k, v in compat.iteritems(dict)}

def _ord_dict(dict):
    return {ord(k): v for k, v in compat.iteritems(dict)}


# for unicode.translate
_Z2H_KANA = _ord_dict(_KANA_MAPPER)
_Z2H_ALPHA = _ord_dict(_ALPHA_MAPPER)
_Z2H_DIGIT = _ord_dict(_DIGIT_MAPPER)
_Z2H_SYMBOL = _ord_dict(_SYMBOL_MAPPER)
_H2Z_KANA = _ord_dict(_reverse_dict(_KANA_MAPPER))
_H2Z_ALPHA = _ord_dict(_reverse_dict(_ALPHA_MAPPER))
_H2Z_DIGIT = _ord_dict(_reverse_dict(_DIGIT_MAPPER))
_H2Z_SYMBOL = _ord_dict(_reverse_dict(_SYMBOL_MAPPER))


# for multiple replace
_Z2H_SOUNDMARK = {unicodedata.normalize('NFKC', c): c for c in _HSOUNDMARK}
_H2Z_SOUNDMARK = _reverse_dict(_Z2H_SOUNDMARK)


def _h2z_sm(text):
    return compat.reduce(lambda t, kv: t.replace(*kv),
                         compat.iteritems(_H2Z_SOUNDMARK), text)


def _z2h_sm(text):
    return compat.reduce(lambda t, kv: t.replace(*kv),
                         compat.iteritems(_Z2H_SOUNDMARK), text)


def str_z2h(self, kana=True, alpha=True, digit=True, symbol=True):
    mapper = dict()
    if kana:
        mapper.update(_Z2H_KANA)
    if alpha:
        mapper.update(_Z2H_ALPHA)
    if digit:
        mapper.update(_Z2H_DIGIT)
    if symbol:
        mapper.update(_Z2H_SYMBOL)

    if kana:
        if compat.PY3:
            f = lambda x: _z2h_sm(x).translate(mapper)
        else:
            f = lambda x: _z2h_sm(compat.u_safe(x)).translate(mapper)
    else:
        if compat.PY3:
            f = lambda x: x.translate(mapper)
        else:
            f = lambda x: compat.u_safe(x).translate(mapper)
    return self._wrap_result(strings._na_map(f, self.series))

def str_h2z(self, kana=True, alpha=True, digit=True, symbol=True):
    mapper = dict()
    if kana:
        mapper.update(_H2Z_KANA)
    if alpha:
        mapper.update(_H2Z_ALPHA)
    if digit:
        mapper.update(_H2Z_DIGIT)
    if symbol:
        mapper.update(_H2Z_SYMBOL)

    if kana:
        if compat.PY3:
            f = lambda x: _h2z_sm(x).translate(mapper)
        else:
            f = lambda x: _h2z_sm(compat.u_safe(x)).translate(mapper)
    else:
        if compat.PY3:
            f = lambda x: x.translate(mapper)
        else:
            f = lambda x: compat.u_safe(x).translate(mapper)
    return self._wrap_result(strings._na_map(f, self.series))


def str_normalize(self, form='NFKC'):
    if compat.PY3:
        f = lambda x: unicodedata.normalize(form, x)
    else:
        f = lambda x: unicodedata.normalize(form, compat.u_safe(x))
    return self._wrap_result(strings._na_map(f, self.series))


# do not overwrite existing func
if not hasattr(strings.StringMethods, 'normalize'):
    strings.StringMethods.normalize = str_normalize


if not hasattr(strings.StringMethods, 'z2h'):
    strings.StringMethods.z2h = str_z2h


if not hasattr(strings.StringMethods, 'h2z'):
    strings.StringMethods.h2z = str_h2z
