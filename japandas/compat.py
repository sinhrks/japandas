#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from distutils.version import LooseVersion


PANDAS_VERSION = LooseVersion(pd.__version__)

if PANDAS_VERSION >= LooseVersion('0.19.0'):
    PANDAS_0190 = True
else:
    PANDAS_0190 = False

if PANDAS_VERSION >= LooseVersion('0.18.0'):
    PANDAS_0180 = True
else:
    PANDAS_0180 = False
