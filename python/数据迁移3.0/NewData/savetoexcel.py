#coding=utf-8
import json

import sys
import xlwt
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


rowlist = []
with open('未匹配') as f:
    for line in f:
        rowlist.append(json.loads(line))


def saveToFile(res):
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(u'管理机构')


    hang = 0
    for row in res:
        lie = 0

        ws.write(hang, lie + 0, str(row[u'募集时间']))
        ws.write(hang, lie + 1, str(row[u'基金名称']))
        ws.write(hang, lie + 2, str(row[u'基金类型']))
        ws.write(hang, lie + 3, str(row[u'管理机构']))
        ws.write(hang, lie + 4, str(row[u'资本类型']))
        ws.write(hang, lie + 5, str(row[u'募集金额(万元)']))
        ws.write(hang, lie + 6, str(row[u'币种']))
        ws.write(hang, lie + 7, str(row[u'当前状态']))

        hang = hang + 1
    wb.save('未找到.xls')


saveToFile(rowlist)