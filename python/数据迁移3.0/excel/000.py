# -*- coding: utf-8 -*-
import traceback
import  xdrlib ,sys

import time

import xlwt
from pypinyin import slug as hanzizhuanpinpin
import requests
import xlrd
import json

reload(sys)
sys.setdefaultencoding('utf-8')


token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
baseurl = 'http://192.168.1.201:8000/'
# token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
# baseurl = 'https://api.investarget.com/'

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
def excel_table_byindex(file,colnameindex=0, by_index=0):
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


userdict = {

}
familar = {
    '1': '加过微信',
    '2': '了解投资偏好',
    '3': '跟进过我们的项目',
    '4': '见过面',
    '5': '好友',
    '99': '未接触'
}

tables = excel_table_byindex(u'/Users/investarget/pythons/python/数据迁移3.0/excel/exceldata/000.xlsx')
tables2 = excel_table_byindex(u'/Users/investarget/pythons/python/数据迁移3.0/excel/exceldata/001.xlsx')
for row in tables:
    if userdict.get(str(row['id'])) is None:
        userdict[str(row['id'])] = row
    else:
        userdict[str(row['id'])][u'tag'] = userdict[str(row['id'])][u'tag'] + u',' + row[u'tag']

for row in tables2:
    if userdict.get(str(row['id'])) is None:
        userdict[str(row['id'])] = row



def saveToFile(res):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('user')
    hang = 0
    ws.write(hang, 0, '名称')
    ws.write(hang, 1, '手机')
    ws.write(hang, 2, '机构')
    ws.write(hang, 3, '标签')
    ws.write(hang, 4, '熟悉度')
    ws.write(hang, 5, '熟悉度等级')
    hang = hang + 1
    for row in res.values():
        ws.write(hang, 0, str(row[u'name']))
        ws.write(hang, 1, str(int(row[u'mobile'])))
        ws.write(hang, 2, str(row[u'org']))
        ws.write(hang, 3, str(row[u'tag']))
        ws.write(hang, 4, str(int(row[u'familar_id'])))
        ws.write(hang, 5, familar[str(int(row[u'familar_id']))])

        hang = hang + 1


    wb.save('user000.xls')






saveToFile(userdict)