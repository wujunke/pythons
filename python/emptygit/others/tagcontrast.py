#coding=utf-8
import json

import requests
import  xlrd


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



tables = excel_table_byindex('/Users/investarget/Desktop/tagcontrast.xlsx')

userslist = []
for row in tables:
    tagid = row.pop('tagid')
    for key, value in row.items():
        if value == 1.0:
            print key, int(tagid)
            data = {
                'tag': tagid,
                'cat_name': key,
            }
            res = requests.post('http://192.168.1.201:8000/source/tagcontrast', data=json.dumps(data), headers={'Content-Type': 'application/json',}).content
            res = json.loads(res)
            if res['code'] != 1000:
                print res['errormsg']