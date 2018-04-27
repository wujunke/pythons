#coding=utf-8
import json
import random


import datetime
import requests
import time
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import xlrd




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



#记录名称id对对应关系
def saveInfo(itjuzi_id, itjuzi_name, haituo_id):
    if haituo_id:
        f = open('name_id_comparetable', 'a')
        content = {
            'itjuzi_id': itjuzi_id,
            'itjuzi_name':itjuzi_name,
            'haituo_id':int(haituo_id),
        }
        f.writelines(json.dumps(content))
        f.writelines('\n')
        f.close()





token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'

# 插入数据地址
base_url = 'https://api.investarget.com/'

def getHaituoidWithItjuziName(itjuzi_name):
    res_id = None
    headers = {
        'token': token,
        'source': '1',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    if itjuzi_name:
        response = requests.get(base_url + 'org/?orgfullname=%s' % itjuzi_name,
                               headers=headers).content
        response = json.loads(response)
        if response['code'] != 1000:
            print '未找到对应id--%s' % itjuzi_name + str(response)
        else:
            res_id = response['result'][0]['id']
    else:
        print '机构名为空--%s' % itjuzi_name
    return res_id


tables = excel_table_byindex('/Users/investarget/Desktop/IT桔子机构对照表1501-3100.xlsx')
for row in tables:
    itjuzi_name = row['itjuzi_name']
    itjuzi_id = row['itjuzi_id']
    if row['haituo_id']:
        haituo_id = row['haituo_id']
    else:
        #没有id，从库里搜索（按全称搜索）
        haituo_id = getHaituoidWithItjuziName(itjuzi_name)
    saveInfo(itjuzi_id, itjuzi_name, haituo_id)