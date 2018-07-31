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

base_url = 'http://192.168.1.201:8000/'
# base_url = 'http://192.168.1.251:8080/'
# base_url = 'https://api.investarget.com/'
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



def createOrg(orgname, currency=None, fundSize=None):
    data = {
        'orgfullname': orgname,
        'orgnameC': orgname,
        'orgnameE': orgname,
        'orgtype': 1, #基金类型
        'issub': True,
        'currency': currency,
        'fundSize': fundSize,
    }
    url = base_url + 'org/'
    res = requests.post(url , headers=headers, data=json.dumps(data)).content
    res = json.loads(res)
    if res['code'] == 1000:
        print orgname, '已新增--%s' % res['result']['id']
    else:
        print orgname, res['errormsg']


def searchOrgfullnameOrg(orgname, issub):
    org_id = None
    url = base_url + 'org/?orgfullname=%s&issub=%s' % (orgname.replace(' ', '%20') , issub)
    res = requests.get(url, headers=headers).content
    res = json.loads(res)
    if res['code'] == 1000:
        if res['result']['count'] == 1:
            org_id = res['result']['data'][0]['id']
    return org_id

def searchOrgnameOrg(orgname, issub):
    org_id = None
    url = base_url + 'org/?search=%s&issub=%s' % (orgname.replace(' ', '%20') , issub)
    res = requests.get(url, headers=headers).content
    res = json.loads(res)
    if res['code'] == 1000:
        if res['result']['count'] == 1:
            org_id = res['result']['data'][0]['id']
        elif res['result']['count'] > 1:
            org_id = res['result']['data'][0]['id']
    return org_id


def insertManageFund(data, row):
    url = base_url + 'org/managefund/'
    res = requests.post(url, json.dumps(data), headers=headers).content
    res = json.loads(res)
    if res['code'] == 1000:
        pass
    else:
        print res['errormsg']
        saveFailData(row)

def saveFailData(row):
    f = open('新增失败', 'a')
    f.writelines(json.dumps(row))
    f.writelines('\n')
    f.close()


def saveUnsearchData(row):
    f = open('未匹配', 'a')
    f.writelines(json.dumps(row))
    f.writelines('\n')
    f.close()


def main():
    tables = excel_table_byindex('/Users/investarget/pythons/python/数据迁移3.0/NewData/基金募资情况2.xlsx')
    for row in tables:
        fundname = row[u'基金名称']
        orgname = row[u'管理机构']
        fundsizestr = row[u'募集金额(万元)']
        if u' ' in fundname:
            fund_id = searchOrgfullnameOrg(fundname, True)
            # if fund_id:
            #     pass
            # else:
            #     if row[u'币种'] == u'人民币元':
            #         currency = 1
            #     elif row[u'币种'] == u'美元':
            #         currency = 2
            #     elif row[u'币种'] == u'日元':
            #         currency = 6
            #     elif row[u'币种'] == u'欧元':
            #         currency = 3
            #     else:
            #         currency = 1
            #     if fundsizestr == u'--':
            #         fundsize = None
            #     else:
            #         fundsize = int(float(fundsizestr) * 10000)
            #     createOrg(fundname, currency, fundsize)



            org_id = searchOrgfullnameOrg(orgname, False)
            if orgname == u'DCM资本':
                org_id = 489
            elif orgname == u'德意志银行(中国)':
                org_id = 24081
            elif orgname == u'崇德投资':
                org_id = 724

            if not org_id:
                org_id = searchOrgnameOrg(orgname, False)
            if fund_id and org_id:
                # if row[u'币种'] == u'人民币元':
                #     currency = 1
                # elif row[u'币种'] == u'美元':
                #     currency = 2
                # elif row[u'币种'] == u'日元':
                #     currency = 6
                # elif row[u'币种'] == u'欧元':
                #     currency = 3
                # else:
                #     currency = 1
                if fundsizestr == u'--':
                    fundsize = None
                else:
                    fundsize = int(float(fundsizestr) * 10000)
                type = row[u'基金类型']
                if type == u'--':
                    type = None
                fundsource = row[u'资本类型']
                if fundsource == u'--':
                    fundsource = None
                import datetime
                raisedate = row[u'募集时间']
                if raisedate == u'--':
                    raisedate = None
                elif len(raisedate) == 4:
                    raisedate = raisedate + u'-01-01'
                elif len(raisedate) == 7:
                    raisedate = raisedate + u'-01'
                if raisedate:
                    raisedate = raisedate + 'T00:00:00'

                data = {
                    'org': org_id,
                    'fund': fund_id,
                    'type': type,
                    'fundsource': fundsource,
                    'fundraisedate': raisedate,
                    'fundsize': fundsize,
                }
                row['org_id'] = org_id
                row['fund_id'] = fund_id
                insertManageFund(data, row)
            else:
                row['org_id'] = org_id
                row['fund_id'] = fund_id
                saveUnsearchData(row)






if __name__=="__main__":
    main()