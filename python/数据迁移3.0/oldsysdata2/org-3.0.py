#coding=utf-8
import json

import datetime
import pymysql
import requests


class DataManager():
    def __init__(self):
        self.allMySqlOrg = self.getAllMySqlOrg()
        self.allMySqlOrgTransactionPhase = self.getAllOrgTransactionPhase()

        self.allOrg = self.getAllOrg()

    def getAllMySqlOrg(self):
        res = []
        connection = pymysql.connect(host='192.168.1.251',
                                     user='root',
                                     password='investarget@2017',
                                     db='investarget',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT  *  FROM investarget.org  WHERE is_deleted = 0  and datasource_id = 1 AND stockcode is NOT NULL  "
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getAllOrgTransactionPhase(self):
        res = []
        connection = pymysql.connect(host='192.168.1.251',
                                     user='root',
                                     password='investarget@2017',
                                     db='investarget',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM investarget.org_TransactionPhase  WHERE is_deleted = 0 "
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getOrgTransactions(self,orgId):
        orgtransactionphase = []
        if orgId:
            for transa in self.allMySqlOrgTransactionPhase:
                if transa['org_id'] == orgId:
                    orgtransactionphase.append(transa['transactionPhase_id'])
        return orgtransactionphase

    def getAllOrg(self):
        res = []
        connection = pymysql.connect(host='39.107.14.53',
                                     user='root',
                                     password='Investarget@2017',
                                     db='investarget',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT  *  FROM investarget.org  WHERE is_deleted = 0  and datasource_id = 1 AND  stockcode is NULL"
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getNewOrgId(self, orgname):
        if orgname:
            for dic in self.allOrg:
                if dic['orgnameC'] == orgname:
                    return dic['id']
            return None
        else:
            return None


#海拓token
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
#车创token
token2 = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecg'
baseurl = 'http://192.168.1.201:8000/'
headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }

times = 0
datamanager = DataManager()

for dic in datamanager.allMySqlOrg:
    oldid = dic.pop('id')
    for key,value in dic.items():
        if isinstance(value,datetime.datetime):
            if value:
                dic[key] = str(value)
    dic.pop('createuser_id')
    dic.pop('lastmodifyuser_id')
    dic.pop('deleteduser_id')
    dic.pop('auditUser_id')
    dic['currency'] = dic['currency_id']
    dic['orgattribute'] = dic['orgattribute_id']
    dic['orgtype'] = dic['orgtype_id']
    dic['industry'] = dic['industry_id']
    dic['orgstatus'] = dic['orgstatus_id']

    dic['orgtransactionphase'] = datamanager.getOrgTransactions(oldid)
    neworgid = datamanager.getNewOrgId(dic['orgnameC'])
    if neworgid:
        response = requests.put(baseurl + 'org/%s/'%neworgid, data=json.dumps(dic), headers=headers).content
        response = json.loads(response)
        if response['code'] != 1000:
            print '新增失败' + str(response)
            print dic['orgnameC']
            print str(times)
            times+=1
        else:
            f = open('org3.0update-old_new_id', 'a')
            f.writelines(json.dumps({'old': oldid, 'new': response['result']['id']}))
            f.writelines('\n')
            f.close()
    else:
        print '没有找到'
        print dic['orgnameC']