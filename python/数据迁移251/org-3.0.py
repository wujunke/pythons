#coding=utf8
import json

import datetime
import pymysql
import requests


class DataManager():
    def __init__(self):
        self.allMySqlOrg = self.getAllMySqlOrg()
        self.allMySqlOrgTransactionPhase = self.getAllOrgTransactionPhase()


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
                sql = "SELECT  *  FROM investarget.org  WHERE is_deleted = 0  and datasource_id = 2"
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
                sql = "SELECT * FROM investarget.org_TransactionPhase  WHERE is_deleted = 0"
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
#海拓token
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
#车创token
token2 = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecg'
baseurl = 'http://39.107.14.53:8080/'
headers = {
        'token':token2,
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
    dic[u'orgtransactionphase'] = datamanager.getOrgTransactions(oldid)

    response = requests.post(baseurl + 'org/', data=json.dumps(dic), headers=headers).content
    response = json.loads(response)
    if response['code'] != 1000:
        print '新增失败' + str(response)
        print dic['orgnameC']
        print str(times)
        times+=1
    else:
        f = open('org3.0-old_new_id', 'a')
        f.writelines(json.dumps({'old': oldid, 'new': response['result']['id']}))
        f.writelines('\n')
        f.close()