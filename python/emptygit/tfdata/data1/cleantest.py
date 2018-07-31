#coding=utf-8
import json
import re

import requests
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


import csv


def savetocsvfile(data):
    with open("test5.csv","a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            data['com_name'],
            int(data['invse_round_id']),
            int(data['tag']),
            data['com_full_name'],
            int(data['top']),
            data['investor'],
            int(data['invse_detail_money']),
            int(data['invse_total_money']),
            int(data['patent'])
        ])


tables = excel_table_byindex('test3.xlsx')

for row in tables:
    investor = row['investor']
    if investor:
        savetocsvfile(row)



