#coding=utf-8
import json
import random

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
    colnames = table.row_values(colnameindex)
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                 if isinstance(colnames[i], float):
                     colnames[i] = str(int(colnames[i]))
                 app[colnames[i]] = row[i]
             list.append(app)
    return list



import csv


def saveorgfund(data):
    with open('org.txt', 'a') as f:
        f.write(json.dumps(data))
        f.write('\n')


orglist = []
f1 = open('/Users/investarget/pythons/python/emptygit/addInvestEvent/name_id_comparetable', 'r')
lines = f1.readlines()
for l in lines:
    dic = json.loads(l)
    orglist.append(dic)
f1.close()


# f1 = open('org.txt', 'r')
# lines = f1.readlines()
# for l in lines:
#     orglist.append(int(l.replace('\n', '')))
# f1.close()

def getOrgId(org_name):
    if u'（领投）' in org_name:
        org_name = org_name.replace(u'（领投）', u'')
    if u'（财务顾问）' in org_name:
        org_name = org_name.replace(u'（财务顾问）', u'')
    for org in orglist:
        if org['itjuzi_name'] == org_name:
            return org['haituo_id']
    return None

def getFundMand(haituoId):
    url = 'https://api.investarget.com/org/managefund/?org=%s' % haituoId
    res = requests.get(url, headers={
        'Content-Type': 'application/json',
        'token': 'a7305831f4903690feb349c16ab37f9b4962197305ba32c7'}).content
    res = json.loads(res)
    if res['code'] == 1000:
        if res['result']['count'] > 0:
            return 1
    return 0


def savetocsvfile(data):
    with open("test7-44.csv","a") as csvfile:
        writer = csv.writer(csvfile)
        tagstr = bin(int(data['tag']))
        tagstr = tagstr[2:]
        taglist = [(int(i) * 5) for i in ('0' * (42 - len(tagstr)) + tagstr)]

        writer.writerow([
            int(data['com_id']),
            data['com_name'],
            (int(data['invse_round_id']) + 1) / 18.0,
            int(data['tag']),
            data['com_full_name'],
            int(data['top']),
            data['investor'],
            (int(data['invse_detail_money']) / int(data['invse_total_money'])) if int(data['invse_total_money']) != 0 else 0.0,
            # int(data['invse_total_money']),
            int(data['patent']),
            int(data['org_id']),
            int(data['fund'])
        ] + taglist)


tables = excel_table_byindex('test7.xlsx')




ln = 0
for row in tables:
    ln += 1
    if ln > 0:
        investorg_name = row['investor']
        haituoid = getOrgId(investorg_name)
        if haituoid:
            fund = getFundMand(haituoid)
            row['fund'] = fund
            row['org_id'] = haituoid
            pass
        else:
            # print row['investor']
            row['fund'] = 0
            row['org_id'] = 0
        savetocsvfile(row)
        # if int(row['org_id']) in orglist:
        #     row['fund'] = 1
        # else:
        #     row['fund'] = 0
        # savetocsvfile(row)
        print ln
