# -*- coding: utf-8 -*-
import traceback
import  xdrlib ,sys

import xlwt
from pypinyin import slug as hanzizhuanpinpin
import requests
import xlrd
import json

reload(sys)
sys.setdefaultencoding('utf-8')



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

tables = excel_table_byindex('/Users/investarget/pythons/python/数据迁移3.0/excel/exceldata/税务.xlsx')

wb = xlwt.Workbook(encoding='utf-8')
ws = wb.add_sheet(u'xxx')

hang = 1
for row in tables:

    ws.write(hang, 0, '')
    ws.write(hang, 1, row[u'客户名称'])
    ws.write(hang, 2, '')
    ws.write(hang, 3, row[u'姓名'])
    ws.write(hang, 4, row[u'证件号'])
    ws.write(hang, 5, row[u'缴纳城市'])
    ws.write(hang, 6, row[u'账单月份'])
    ws.write(hang, 7, row[u'费用月份'])
    ws.write(hang, 8, row[u'缴费说明'])
    ws.write(hang, 9, '')

    ws.write(hang, 10, row[u'费用总计'])

    ws.write(hang, 11, row[u'服务费'])

    ws.write(hang, 12, row[u'社保缴费基数'])
    ws.write(hang, 13, row[u'社保公积金个人小计'])
    ws.write(hang, 14, row[u'社保公积金企业小计'])
    ws.write(hang, 15, row[u'社保公积金个人小计'] + row[u'社保公积金企业小计'] + row[u'社保补缴滞纳金'])
    ws.write(hang, 16, row[u'社保补缴滞纳金'])

    ws.write(hang, 17, row[u'公积金个人基数'])
    ws.write(hang, 18, row[u'公积金个人金额'])
    ws.write(hang, 19, row[u'公积金单位金额'])
    ws.write(hang, 20, row[u'公积金个人金额'] + row[u'公积金单位金额'] + row[u'公积金补缴滞纳金'])
    ws.write(hang, 21, row[u'公积金补缴滞纳金'])

    ws.write(hang, 22, '')



    hang = hang + 1
wb.save('xinshuiwu.xls')


