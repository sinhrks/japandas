#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import numpy as np
import pandas as pd

from japandas.compat import PANDAS_0190, PANDAS_0180


if PANDAS_0190:
    from pandas.tests.plotting.common import TestPlotBase, _check_plot_works
else:
    from pandas.tests.test_graphics import TestPlotBase, _check_plot_works


class TestTools(TestPlotBase):

    def test_to_ohlc(self):
        n = 50
        idx = pd.date_range(start='2014-10-01 09:00', freq='H', periods=n)
        s = pd.Series(np.random.randn(n), index=idx)
        _check_plot_works(s.plot, kind='ohlc')
        _check_plot_works(s.plot, kind='ohlc', x_compat=True)

        if PANDAS_0180:
            ohlc = s.resample('B').ohlc()
        else:
            ohlc = s.resample('B', how='ohlc')
        _check_plot_works(ohlc.plot, kind='ohlc')
        _check_plot_works(ohlc.plot, kind='ohlc', x_compat=True)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
