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

token = '5c929f67ac273d8d432ae8be3cf68adcc39d7282d6b48554'
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
    except Exception,e:
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

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file,colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
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








def addOrg(row):
    try:
        emaillist = row['companyEmail'].split(';')
        if len(emaillist) > 0:
            email = emaillist[0]
            if len(email) > 5:
                email = email[0:-1] if email[-1] == '.' else email
            else:
                email = None
        else:
            email = None
        dic = {
            'datasource': 1,
            'orgtype': 12,
            'orgstatus': 2,
            # 'transactionAmountF': row['TransactionAmountF'],
            # 'transactionAmountT': row['TransactionAmountT'],
            # 'typicalCase': None,
            # 'transactionAmountF_USD': row['TransactionAmountF_USD'],
            # 'transactionAmountT_USD': row['TransactionAmountT_USD'],
            # 'partnerOrInvestmentCommiterMember': row['PartnerOrInvestmentCommitteeMember'],
            'mobile': row['mobile'],
            'companyEmail': email,
            'industry': datamanager.getNewIndustryId(row['industry'],row['Pindustry']),
            'marketvalue': int(row['marketvalue']) if row['marketvalue'] else None,
            'address': row['officeaddress'],
            'webSite': row['webSite'],
            'IPOdate': row['launchdate'],
            'orgattribute': datamanager.getNewAttributeId(row['orgattribute']),
            'businessscope': row['businessscope'],
            'mainproductname': row['mainproductname'],
            'mainproducttype': row['mainproducttype'],
            'totalemployees': int(row['totalemployees']) if row['totalemployees'] else None,
            'stockcode': row['stockcode'],
            'stockshortname': row['stockshortname'],
            'orgnameC': row['orgnameC'],
            'orgnameE': row['orgnameE'],
            'description': row['description'],

        }
        response = requests.post(baseurl + 'org/', data=json.dumps(dic), headers=headers).content
        response = json.loads(response)
        if response['code'] != 1000:
            print '新增失败' + str(response)
            print dic['orgnameC']
            return None
        else:
            return response['result']['id']
    except Exception as err:
        print '新增shibai'
        print  err
        return None


def updateOrg(row,orgid):
    emaillist = row['companyEmail'].split(';')
    if len(emaillist) > 0:
        email = emaillist[0]
        if len(email) > 5:
            email = email[0:-1] if email[-1] == '.' else email
        else:
            email = None
    else:
        email = None
    try:
        if orgid:
            dic = {
                # 'orgstatus': 2,
                # 'mobile': row['mobile'],
                # 'companyEmail': email,
                'industry': datamanager.getNewIndustryId(row['industry'],row['Pindustry']),
                # 'marketvalue': int(row['marketvalue']) if row['marketvalue'] else None,
                # 'address': row['officeaddress'],
                # 'webSite': row['webSite'],
                # 'IPOdate': row['launchdate'],
                # 'orgattribute': datamanager.getNewAttributeId(row['orgattribute']),
                # 'businessscope': row['businessscope'],
                # 'mainproductname': row['mainproductname'],
                # 'mainproducttype': row['mainproducttype'],
                # 'totalemployees': int(row['totalemployees']) if row['totalemployees'] else None,
                # 'stockcode': row['stockcode'],
                # 'stockshortname': row['stockshortname'],
                # 'orgnameC': row['orgnameC'],
                # 'orgnameE': row['orgnameE'],
                # 'description': row['description'],
            }
            response = requests.put(baseurl + 'org/%s/' % orgid, data=json.dumps(dic), headers=headers).content
            response = json.loads(response)
            if response['code'] != 1000:
                print '修改失败' + str(response)
                print dic['orgnameC']
        else:
            print '未找到匹配org' + '***' + str(row['orgnameC'])
    except Exception:
        print '修改shibai' + str(row['orgnameC'])
        print traceback.format_exc()
        pass



def addUnreachUser(row,orgid):
    try:
        if orgid:
            if row['master1'] == row['master2'] and row['master2'] not in [None,'',u'']:
                diclist = [{
                    'name': row['master1'],
                    'title': 14,
                    'org': orgid,
                }]
            elif row['master1'] in [None,'',u''] and row['master2'] not in [None,'',u'']:
                diclist = [{
                    'name': row['master2'],
                    'title': 44,
                    'org': orgid,
                }]
            elif row['master1'] not in [None,'',u''] and row['master2'] in [None,'',u'']:
                diclist = [{
                    'name': row['master1'],
                    'title': 14,
                    'org': orgid,
                }]
            elif row['master1'] in [None,'',u''] and row['master2'] in [None,'',u'']:
                diclist = []
            else:
                diclist = [{
                    'name': row['master1'],
                    'title': 14,
                    'org': orgid,
                }, {
                    'name': row['master2'],
                    'title': 44,
                    'org': orgid,
                }]

            for dic in diclist:
                response = requests.post(baseurl + 'user/unuser/', data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] != 1000:
                    print '新增unreachuser失败' + str(response)
                    print dic['name'] +row['orgnameC']
        else:
            print '未找到匹配org' + '***' + str(row['orgnameC'])
    except Exception:
        print '新增usershibai' + str(row['orgnameC'])
        print traceback.format_exc()
        pass


class DataManager():
    def __init__(self):
        self.allOrg = self.getAllOrg()


        self.allMySqlIndustry = self.getAllMySqlIndustry()
        self.allMySqlAttribute = self.getAllMySqlOrgAttribute()





    def getAllOrg(self):
        tables = excel_table_byindex('/Users/investarget/Desktop/20170907.xlsx')
        return tables

    def getAllMySqlOrg(self,orgname):
        res = []
        connection = pymysql.connect(host='192.168.1.251',
                                     user='root',
                                     password='investarget@2017',
                                     db='investarget',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM org WHERE is_deleted = 0 AND datasource_id = 1 AND orgnameC LIKE '%s%%'" % orgname
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getAllMySqlOrgAttribute(self):
        res = requests.get(baseurl + 'source/orgAttribute')
        return json.loads(res.content).get('result', None)

    def getAllMySqlIndustry(self):
        res = requests.get(baseurl + 'source/industry')
        return json.loads(res.content).get('result',None)


    def getNewIndustryId(self, industryname, Pindustryname):
        if industryname:
            mysqlid = None
            for one in self.allMySqlIndustry:
                if one['industryC'] == industryname:
                    if one['Pindustry']['industryC'] == Pindustryname:
                        mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None

    def getNewAttributeId(self,attributename):
        if attributename:
            mysqlid = None
            for one in self.allMySqlAttribute:
                if one['attributeC'] == attributename:
                    mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None


   # tables = excel_table_byname('/Users/investarget/Desktop/2017.xlsx')
   # for row in tables:
   #     print row

datamanager = DataManager()
def main():
    times = 0
    for row in datamanager.allOrg:
        times = times + 1
        print times
        orgname = row['orgnameC']
        if orgname != '' :

            row['launchdate'] = None
            if 'Bffmw' in row['stockshortname']:
                print orgname + row['stockshortname']
            else:
                orglist = datamanager.getAllMySqlOrg(orgname)
                if len(orglist) > 0:
                    updateOrg(row, orglist[0]['id'])
                    # addUnreachUser(row, orglist[0]['id'])
                else:
                    orgid = addOrg(row)
                    if orgid:
                        addUnreachUser(row, orgid)

#获取行业id时 需要serializers 加  depth=1


if __name__=="__main__":
    main()


