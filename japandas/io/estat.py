#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import requests
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd


# http://www.e-stat.go.jp/api/e-stat-manual/

METADATA_MAPPER = {
    # 'TABLE_INF': u'統計表ID',
    'STAT_NAME': u'政府統計名',
    'GOV_ORG': u'作成機関名',
    'STATISTICS_NAME': u'提供統計名及び提供分類名',
    'TITLE': u'統計表題名及び表番号',
    'CYCLE': u'提供周期',
    'SURVEY_DATE': u'調査年月',
    'OPEN_DATE': u'公開日',
    'SMALL_AREA': u'小地域属性フラグ',
    'MAIN_CATEGORY': u'統計大分野名',
    'SUB_CATEGORY': u'統計小分野名',
    'OVERALL_TOTAL_NUMBER': u'総件数',
    'UPDATED_DATE': u'最終更新日',
    'id': u'統計表ID'
}


def get_estat_list(code, appid, **kwargs):
    url = 'http://api.e-stat.go.jp/rest/2.0/app/getStatsList'
    params = {'appId': appid, 'lang': 'J', 'statsCode': code}
    params.update(kwargs)
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)

    values = []
    for table in root.findall('.//TABLE_INF'):
        columns = [u'統計表ID']
        row = {u'統計表ID': table.get('id')}
        for elem in table.iter():
            if elem.tag == 'TABLE_INF':
                continue

            if elem.tag in ('UPDATED_DATE', 'OPEN_DATE'):
                val = pd.to_datetime(elem.text)
            elif elem.tag == 'SURVEY_DATE':
                # Almost impossible to parse SURVEY_DATE as Timestamp...
                val = elem.text
            elif elem.tag == 'OVERALL_TOTAL_NUMVER':
                val = pd.to_numeric(elem.text)
            else:
                val = elem.text
            label = METADATA_MAPPER.get(elem.tag, elem.tag)
            columns.append(label)
            row[label] = val
        values.append(row)

    df = pd.DataFrame(values, columns=columns)
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