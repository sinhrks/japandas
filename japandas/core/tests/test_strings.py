#!/usr/bin/env python
# coding: utf-8

# do not import unicode_literals here to test ASCII in Python 2.7

import pandas as pd
import pandas.util.testing as tm


class TestStrings(tm.TestCase):

    def setUp(self):
        self.zhiragana_s = pd.Series([u'ぁあぃいぅうぇえぉお',
                                      u'かがきぎくぐけげこご',
                                      u'さざしじすずせぜそぞ',
                                      u'ただちぢっつづてでとど',
                                      u'なにぬねの',
                                      u'はばぱひびぴふぶぷへべぺほぼぽ',
                                      u'まみむめもゃやゅゆょよ',
                                      u'らりるれろわをんゎゐゑゕゖゔ'])

        self.zkatakana_s = pd.Series([u'ァアィイゥウェエォオ',
                                      u'カガキギクグケゲコゴ',
                                      u'サザシジスズセゼソゾ',
                                      u'タダチヂッツヅテデトド',
                                      u'ナニヌネノ',
                                      u'ハバパヒビピフブプヘベペホボポ',
                                      u'マミムメモャヤュユョヨ',
                                      u'ラリルレロワヲンヮヰヱヵヶヴ',
                                      u'ー・「」。、'])

        self.hkatakana_s = pd.Series([u'ｧｱｨｲｩｳｪｴｫｵ',
                                      u'ｶｶﾞｷｷﾞｸｸﾞｹｹﾞｺｺﾞ',
                                      u'ｻｻﾞｼｼﾞｽｽﾞｾｾﾞｿｿﾞ',
                                      u'ﾀﾀﾞﾁﾁﾞｯﾂﾂﾞﾃﾃﾞﾄﾄﾞ',
                                      u'ﾅﾆﾇﾈﾉ',
                                      u'ﾊﾊﾞﾊﾟﾋﾋﾞﾋﾟﾌﾌﾞﾌﾟﾍﾍﾞﾍﾟﾎﾎﾞﾎﾟ',
                                      u'ﾏﾐﾑﾒﾓｬﾔｭﾕｮﾖ',
                                      u'ﾗﾘﾙﾚﾛﾜｦﾝヮヰヱヵヶｳﾞ',
                                      u'ｰ･｢｣｡､'])

        self.zalpha_s = pd.Series([u'ＡＢＣＤＥＦＧＨ',
                                   u'ＩＪＫＬＭＮＯＰ',
                                   u'ＱＲＳＴＵＶＷＸＹＺ',
                                   u'ａｂｃｄｅｆｇｈ',
                                   u'ｉｊｋｌｍｎｏｐ',
                                   u'ｑｒｓｔｕｖｗｘｙｚ'])
        self.halpha_s = pd.Series(['ABCDEFGH',
                                   'IJKLMNOP',
                                   'QRSTUVWXYZ',
                                   'abcdefgh',
                                   'ijklmnop',
                                   'qrstuvwxyz'])

        self.zdigit_s = pd.Series([u'０１２３４', u'５６７８９'])
        self.hdigit_s = pd.Series(['01234', '56789'])

        self.zsymbol_s = pd.Series([u'！＂＃＄％＆',
                                    u'＇（）＊＋，',
                                    u'－．／：；＜',
                                    u'＝＞？＠［＼',
                                    u'］＾＿｀～｛',
                                    u'｜｝　'])
        self.hsymbol_s = pd.Series([u'!"#$%&',
                                    u"'()*+,",
                                    u'-./:;<',
                                    u'=>?@[\\',
                                    u']^_`~{',
                                    u'|} '])

    def test_mapper(self):
        import japandas.core.strings as s
        tm.assert_equal(len(s._KANA_MAPPER), len(s._HKANA))
        tm.assert_equal(len(s._ALPHA_MAPPER), len(s._ZALPHA))
        tm.assert_equal(len(s._DIGIT_MAPPER), len(s._ZDIGIT))
        tm.assert_equal(len(s._SYMBOL_MAPPER), len(s._ZSYMBOL))

        tm.assert_equal(len(s._reverse_dict(s._KANA_MAPPER)), len(s._HKANA))
        tm.assert_equal(len(s._reverse_dict(s._ALPHA_MAPPER)), len(s._ZALPHA))
        tm.assert_equal(len(s._reverse_dict(s._DIGIT_MAPPER)), len(s._ZDIGIT))
        tm.assert_equal(len(s._Z2H_SYMBOL), len(s._H2Z_SYMBOL))

        tm.assert_equal(len(s._Z2H_KANA), len(s._H2Z_KANA))
        tm.assert_equal(len(s._Z2H_ALPHA), len(s._H2Z_ALPHA))
        tm.assert_equal(len(s._Z2H_DIGIT), len(s._H2Z_DIGIT))
        tm.assert_equal(len(s._reverse_dict(s._SYMBOL_MAPPER)), len(s._ZSYMBOL))

    def test_z2h(self):
        s = pd.Series([u'ａａａ', 'bbb', u'アアア', u'１', u'＊'])
        result = s.str.z2h()
        expected = pd.Series(['aaa', 'bbb', u'ｱｱｱ', '1', '*'])
        tm.assert_series_equal(result, expected)

        # full-width kana to half-width kana
        result = self.zkatakana_s.str.z2h(kana=True, alpha=False, digit=False, symbol=False)
        tm.assert_series_equal(result, self.hkatakana_s)
        result = self.zkatakana_s.str.z2h(kana=False, alpha=True, digit=False, symbol=False)
        tm.assert_series_equal(result, self.zkatakana_s)
        result = self.zkatakana_s.str.z2h(kana=False, alpha=False, digit=True, symbol=False)
        tm.assert_series_equal(result, self.zkatakana_s)
        result = self.zkatakana_s.str.z2h(kana=False, alpha=False, digit=False, symbol=True)
        tm.assert_series_equal(result, self.zkatakana_s)

        # full-width kana to half-width alpha
        result = self.zalpha_s.str.z2h(kana=True, alpha=False, digit=False, symbol=False)
        tm.assert_series_equal(result, self.zalpha_s)
        result = self.zalpha_s.str.z2h(kana=False, alpha=True, digit=False, symbol=False)
        tm.assert_series_equal(result, self.halpha_s)
        result = self.zalpha_s.str.z2h(kana=False, alpha=False, digit=True, symbol=False)
        tm.assert_series_equal(result, self.zalpha_s)
        result = self.zalpha_s.str.z2h(kana=False, alpha=False, digit=False, symbol=True)
        tm.assert_series_equal(result, self.zalpha_s)

        # full-width kana to half-width digit
        result = self.zdigit_s.str.z2h(kana=True, alpha=False, digit=False, symbol=False)
        tm.assert_series_equal(result, self.zdigit_s)
        result = self.zdigit_s.str.z2h(kana=False, alpha=True, digit=False, symbol=False)
        tm.assert_series_equal(result, self.zdigit_s)
        result = self.zdigit_s.str.z2h(kana=False, alpha=False, digit=True, symbol=False)
        tm.assert_series_equal(result, self.hdigit_s)
        result = self.zdigit_s.str.z2h(kana=False, alpha=False, digit=False, symbol=True)
        tm.assert_series_equal(result, self.zdigit_s)

        # full-width kana to half-width symbol
        result = self.zsymbol_s.str.z2h(kana=True, alpha=False, digit=False, symbol=False)
        tm.assert_series_equal(result, self.zsymbol_s)
        result = self.zsymbol_s.str.z2h(kana=False, alpha=True, digit=False, symbol=False)
        tm.assert_series_equal(result, self.zsymbol_s)
        result = self.zsymbol_s.str.z2h(kana=False, alpha=False, digit=True, symbol=False)
        tm.assert_series_equal(result, self.zsymbol_s)
        result = self.zsymbol_s.str.z2h(kana=False, alpha=False, digit=False, symbol=True)
        tm.assert_series_equal(result, self.hsymbol_s)

        # half-width to half-width
        result = self.hkatakana_s.str.z2h()
        tm.assert_series_equal(result, self.hkatakana_s)
        result = self.halpha_s.str.z2h()
        tm.assert_series_equal(result, self.halpha_s)
        result = self.hdigit_s.str.z2h()
        tm.assert_series_equal(result, self.hdigit_s)
        result = self.hsymbol_s.str.z2h()
        tm.assert_series_equal(result, self.hsymbol_s)

    def test_h2z(self):
        s = pd.Series(['aaa', 'bbb', u'ｱｱｱ', u'１', '*'])
        result = s.str.h2z()
        expected = pd.Series([u'ａａａ', u'ｂｂｂ', u'アアア', u'１', u'＊'])
        tm.assert_series_equal(result, expected)

        # half-width kana to full-width kana
        result = self.hkatakana_s.str.h2z(kana=True, alpha=False, digit=False, symbol=False)
        tm.assert_series_equal(result, self.zkatakana_s)
        result = self.hkatakana_s.str.h2z(kana=False, alpha=True, digit=False, symbol=False)
        tm.assert_series_equal(result, self.hkatakana_s)
        result = self.hkatakana_s.str.h2z(kana=False, alpha=False, digit=True, symbol=False)
        tm.assert_series_equal(result, self.hkatakana_s)
        result = self.hkatakana_s.str.h2z(kana=False, alpha=False, digit=False, symbol=True)
        tm.assert_series_equal(result, self.hkatakana_s)

        # half-width kana to full-width alpha
        result = self.halpha_s.str.h2z(kana=True, alpha=False, digit=False, symbol=False)
        tm.assert_series_equal(result, self.halpha_s)
        result = self.halpha_s.str.h2z(kana=False, alpha=True, digit=False, symbol=False)
        tm.assert_series_equal(result, self.zalpha_s)
        result = self.halpha_s.str.h2z(kana=False, alpha=False, digit=True, symbol=False)
        tm.assert_series_equal(result, self.halpha_s)
        result = self.halpha_s.str.h2z(kana=False, alpha=False, digit=False, symbol=True)
        tm.assert_series_equal(result, self.halpha_s)

        # half-width kana to full-width digit
        result = self.hdigit_s.str.h2z(kana=True, alpha=False, digit=False, symbol=False)
        tm.assert_series_equal(result, self.hdigit_s)
        result = self.hdigit_s.str.h2z(kana=False, alpha=True, digit=False, symbol=False)
        tm.assert_series_equal(result, self.hdigit_s)
        result = self.hdigit_s.str.h2z(kana=False, alpha=False, digit=True, symbol=False)
        tm.assert_series_equal(result, self.zdigit_s)
        result = self.hdigit_s.str.h2z(kana=False, alpha=False, digit=False, symbol=True)
        tm.assert_series_equal(result, self.hdigit_s)

        # half-width kana to full-width symbol
        result = self.hsymbol_s.str.h2z(kana=True, alpha=False, digit=False, symbol=False)
        tm.assert_series_equal(result, self.hsymbol_s)
        result = self.hsymbol_s.str.h2z(kana=False, alpha=True, digit=False, symbol=False)
        tm.assert_series_equal(result, self.hsymbol_s)
        result = self.hsymbol_s.str.h2z(kana=False, alpha=False, digit=True, symbol=False)
        tm.assert_series_equal(result, self.hsymbol_s)
        result = self.hsymbol_s.str.h2z(kana=False, alpha=False, digit=False, symbol=True)
        tm.assert_series_equal(result, self.zsymbol_s)

        # full-width to full-width
        result = self.zkatakana_s.str.h2z()
        tm.assert_series_equal(result, self.zkatakana_s)
        result = self.zalpha_s.str.h2z()
        tm.assert_series_equal(result, self.zalpha_s)
        result = self.zdigit_s.str.h2z()
        tm.assert_series_equal(result, self.zdigit_s)
        result = self.zkatakana_s.str.h2z()
        tm.assert_series_equal(result, self.zkatakana_s)

    def test_z2h_obj(self):
        s = pd.Series(['aaa', None, u'アアア', u'あああ', u'１', 3])
        result = s.str.z2h()
        expected = pd.Series(['aaa', None, u'ｱｱｱ', u'あああ', '1', None])
        tm.assert_series_equal(result, expected)

        empty_str = pd.Series(dtype=str)
        tm.assert_series_equal(empty_str.str.h2z(), empty_str)

    def test_h2z_obj(self):
        s = pd.Series(['aaa', None, u'ｱｱｱ', u'あああ', u'１', 3])
        result = s.str.h2z()
        expected = pd.Series([u'ａａａ', None, u'アアア', u'あああ', u'１', None])
        tm.assert_series_equal(result, expected)

        empty_str = pd.Series(dtype=str)
        tm.assert_series_equal(empty_str.str.h2z(), empty_str)

    def test_normalize(self):
        s = pd.Series([u'ａａａ', 'bbb', u'ｱｱｱ', u'１', u'＊'])
        result = s.str.normalize('NFKC')
        expected = pd.Series(['aaa', 'bbb', u'アアア', '1', '*'])
        tm.assert_series_equal(result, expected)

        s = pd.Series([u'ａａａ', None, 'bbb', u'ｱｱｱ', u'１', 5, u'＊'])
        result = s.str.normalize('NFKC')
        expected = pd.Series(['aaa', None, 'bbb', u'アアア', '1', None, '*'])
        tm.assert_series_equal(result, expected)

        empty_str = pd.Series(dtype=str)
        tm.assert_series_equal(empty_str.str.normalize('NFKC'), empty_str)

    def test_normalize_format(self):
        import unicodedata
        values = [u'ｱｲｳｴｵ', u'ｶｷｸｹｺ', u'ｶﾞｷﾞｸﾞｹﾞｺﾞ', u'ＡＢＣＤＥ']
        for format in ['NFD', 'NFC', 'NFKD', 'NFKC']:
            result = pd.Series(values).str.normalize(format).tolist()
            expected = [unicodedata.normalize(format, v) for v in values]
            tm.assert_equal(result, expected)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
