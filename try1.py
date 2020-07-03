# -*- coding: utf-8 -*-
from datetime import datetime
starttime = datetime.now()
import requests, pandas as pd, numpy as np
from bs4 import BeautifulSoup
from pandas import ExcelWriter
pd.options.display.max_rows = 10000
pd.options.display.max_columns = 1000
import warnings; warnings.simplefilter('ignore')


year = '107'
table_num = '165'
alphabets = 'A、 B、 C、 D、 E、 F、 G、 H、 I、 J、 K、 M、 N、 O、 P、 Q、 T、 U、 V、 W、 X、 Z'
alphabets = alphabets.replace(' ','')
alphabets = alphabets.split('、')

result = []
county = ''
town = ''

url = 'https://ws.fia.gov.tw/001/upload/ias/isa107/107_165-A.html'
print(url)
r = requests.get(url, verify=False)

print(r.status_code)
print(r.content)

r.encoding = 'utf-8'
soup = BeautifulSoup(r.text,'html.parser')
tables = soup.findAll("table", attrs={'style':'width: 1190px; border-collapse: collapse; empty-cells: show'})

"""
for alphabet in alphabets:
    url = 'https://ws.fia.gov.tw/001/upload/ias/isa{0}/{0}_{1}-{2}.html'.format(year,table_num,alphabet)
    print(url)
    r = requests.get(url, verify=False)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'html.parser')
    tables = soup.findAll("table", attrs={'style':'width: 1190px; border-collapse: collapse; empty-cells: show'})
    for table in tables:
        data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele]) 
        data = [x for x in data if len(x) > 1]
        for d in data:
            if '縣市別' in d[0]:
                new_county = d[0].replace('縣市別：','').replace(' ','')
                if county != new_county:
                    county = new_county
                    print(county)
            elif len(d) == 10:
                town = d[0]
                if d[1] != '其\u3000他' and d[1] != '合\u3000計' :
                    result.append([county]+d)
                print(town, end=' ')
            elif len(d) == 9 and d[0] != '其\u3000他' and d[0] != '合\u3000計' :
                result.append([county]+[town]+d)

export = pd.DataFrame(result)
export = export.infer_objects()
export.columns = ['county','town','village','unit','income','mean','median','q1','q3','std','cov']
export[['unit','income','mean','median','q1','q3','std','cov']] = export[['unit','income','mean','median','q1','q3','std','cov']].apply(pd.to_numeric)
export['town'] = export['town'].str.replace('　','')
export['segment'] = pd.cut(export['mean'],bins=[-1,500,600,700,900,100000,],right=True,labels=['1','2','3','4','5'])#labels=['1','2','3']
export['ctv'] = export['county'] + export['town'] + export['village']

pd.cut(export['mean'],bins=[-1,500,600,700,900,100000,],right=True,labels=['1','2','3','4','5'])
export.head()

mapping = pd.read_excel('ctv_mapping.xlsx', sheetname='Sheet1')
mapping.head()

df = mapping.merge(export, left_on='ctv_y', right_on='ctv', how='left')
df.head()

df = df.sort_values(by='mean',ascending=False).reset_index(drop=True)
df = df.drop(columns=['ctv_x', 'ctv_y', 'county_y', 'town_y', 'village_y','ctv'])
df.columns = ['county','town','village','unit','income','mean','median','q1','q3','std','cov','segment']
df.head()

writer = ExcelWriter('fia_income_{}.xlsx'.format(year))
df.to_excel(writer,'Sheet1',index=False)
writer.save()

endtime = datetime.now()
print('start time:', starttime)
print('end time:', endtime)
print('running time:', endtime - starttime)
"""