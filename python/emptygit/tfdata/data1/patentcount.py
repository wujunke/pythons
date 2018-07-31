#coding=utf-8
import json

import requests
#coding=utf-8
import json
import re

import requests
import time
import xlrd
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)





def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print str(e)

def excel_table_byindex(file,colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows
    colnames =  table.row_values(colnameindex)
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list



def savepatentcount(data):
    with open('patent.txt', 'a') as f:
        f.write(json.dumps(data))
        f.write('\n')

def getpatentcount(com_full_name):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'WEE_SID=68miKBgRHJ9kWLlG8Yj3tbsYxzj5GpyWBFPZZjyWtm38vOXHyO6Z!168938531!NONE!1531728893969; IS_LOGIN=true; wee_username=eGlheWFuc3VtbWVyODE%3D; wee_password=WDgxeTAxMjI%3D; JSESSIONID=68miKBgRHJ9kWLlG8Yj3tbsYxzj5GpyWBFPZZjyWtm38vOXHyO6Z!168938531!NONE'
    }
    url = 'http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/executeGeneralSearch0529-executeGeneralSearch.shtml'

    data = {
        'searchCondition.searchExp': '申请（专利权）人=(%s)' % com_full_name,
        'searchCondition.dbId': 'VDB'
    }
    res = requests.post(url, headers=headers, data=data, timeout=30).content
    res = json.loads(res)
    totalCount = res['resultPagination']['totalCount']
    data = {
        com_full_name: totalCount
    }
    savepatentcount(data)
    return totalCount


patentdict = {}
f = open('patent.txt', 'r')
lines = f.readlines()
for l in lines:
    dic = json.loads(l)
    patentdict[dic.items()[0][0]] = dic.items()[0][1]



tables = excel_table_byindex('test5.xlsx')

for row in tables:
    com_full_name = row['com_full_name']
    count = patentdict.get(com_full_name, 'null')
    if count == 'null':
        totalCount = getpatentcount(com_full_name)
        patentdict[com_full_name] = patentdict
