# -*- coding: utf-8 -*-
import traceback
import  xdrlib ,sys

import _mssql

import pymysql
import xlrd
from datetime import datetime
from pypinyin import slug as hanzizhuanpinpin
import requests
from xlrd import xldate_as_tuple
import json

reload(sys)
sys.setdefaultencoding('utf-8')

token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
# baseurl = 'http://39.107.14.53:8080/'
baseurl = 'http://192.168.1.201:8000/'
headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print str(e)
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的索引  ，by_index：表的索引
def excel_table_byindex(file,colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list


def getAllCountry():

    res = json.loads(requests.get(baseurl+'source/orgarea',headers=headers).content)
    re = res.get('result')
    return re

allcountry = getAllCountry()

def getCountryId(countryname):
    reid = None
    for country in allcountry:
        if country.get('nameC') == countryname:
            reid = country.get('id')
    return reid


def main():
    times = 0
    tables = excel_table_byindex('/Users/investarget/Desktop/python/数据迁移3.0/excel/exceldata/Robotics.xlsx')
    for row in tables:
        times = times + 1
        if row['com_name'] in [None,'',u'']:
            print '公司名缺失--%s'%row['name']
            continue
        try:
            mobile = row['usermobile']
            if isinstance(mobile, float):
                mobile = str(int(mobile))
            else:
                mobile = str(mobile)
            dic = {
                'location':getCountryId(str(row['location']).split('-')[0]),
                'com_name': row['com_name'],
                'source': row['source'],
                'username': row['username'],
                'usermobile': mobile,
                'comments': row['comments'],
                'bd_status': str(int(row['bd_status'])),
                'manager':100014845,
            }

            response = requests.post(baseurl+'bd/projbd/',headers=headers,data=json.dumps(dic)).content
            response = json.loads(response)
            if response['code'] != 1000:
                print '新增失败--%s'%row['com_name'] + str(response)
        except Exception:
            print 'shibai--%s'%row['com_name']
            print traceback.format_exc()





   # tables = excel_table_byname('/Users/investarget/Desktop/2017.xlsx')
   # for row in tables:
   #     print row

if __name__=="__main__":
    main()