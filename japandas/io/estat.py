#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import requests
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd


def get_estat_list(code, appid, **kwargs):
    url = 'http://api.e-stat.go.jp/rest/2.0/app/getStatsList'
    params = {'appId': appid, 'lang': 'J', 'statsCode': code}
    params.update(kwargs)
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)

    values = []
    for table in root.findall('.//TABLE_INF'):
        row = {'id': table.get('id')}
        for elem in table.iter():
            if elem.tag in ('UPDATED_DATE', 'OPEN_DATE'):
                val = pd.to_datetime(elem.text)
            elif elem.tag == 'SURVEY_DATE':
                # Almost impossible to parse SURVEY_DATE as Timestamp...
                val = elem.text
            elif elem.tag == 'OVERALL_TOTAL_NUMVER':
                val = pd.to_numeric(elem.text)
            else:
                val = elem.text
            row[elem.tag] = val
        values.append(row)

    df = pd.DataFrame(values)
    return df


def get_estat(code, appid, **kwargs):
    url = 'http://api.e-stat.go.jp/rest/2.0/app/getStatsData'
    params = {'appId': appid, 'lang': 'J', 'statsDataId': code}
    params.update(kwargs)

    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)

    # retrieve class
    class_names = {}   # mapping from class id to name
    class_codes = {}   # mapping from class id to codes
    for c in root.findall('.//CLASS_OBJ'):
        class_id = c.attrib['id']
        class_names[class_id] = c.attrib['name']

        mapper = {}
        for code in c.findall('CLASS'):
            mapper[code.attrib['code']] = code.attrib['name']
        class_codes[class_id] = mapper

    # retrieve values
    values = []
    for value in root.findall('.//VALUE'):
        row = {}
        for cat in class_codes:
            name = class_names[cat]
            code = value.attrib[cat]
            row[name] = class_codes[cat][code]

        row['value'] = value.text
        values.append(row)

    df = pd.DataFrame(values)
    df.loc[:, 'value'] = pd.to_numeric(df['value'], errors='ignore')

    if 'time' in class_names:
        df = df.set_index(class_names['time'])
    return df