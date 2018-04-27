#coding=utf8
import json

import datetime
import pymysql
import requests


class DataManager():
    def __init__(self):

        self.allMySqlOrg2 = self.getAllMySqlOrg2()
        self.allMySqlOrg3 = self.getAllMySqlOrg3()
        self.alluser = self.getAllUser()

    def getAllUser(self):
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
                sql = "SELECT *  FROM unreachuser WHERE datasource_id =1 AND id > 15"
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res





    def getAllMySqlOrg2(self):
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
                sql = "SELECT * FROM org"
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getAllMySqlOrg3(self):
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
                sql = "SELECT * FROM org"
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getNewOrgId(self, orgid):
        if orgid:
            orgname = None
            for org2 in self.allMySqlOrg2:
                if int(org2['id']) == int(orgid):
                    orgname = org2['orgnameC']
            if orgname:
                for dic in self.allMySqlOrg3:
                    if dic['orgnameC'] == orgname:
                       return dic['id']
            else:
                return None
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

for dic in datamanager.alluser:
    for key,value in dic.items():
        if isinstance(value,datetime.datetime):
            if value:
                dic[key] = str(value)
    dic['createuser'] = 1
    dic.pop('datasource_id')
    dic['title'] = dic['title_id']
    orgid = datamanager.getNewOrgId(dic['org_id'])
    if orgid:
        dic['org'] = orgid
        response = requests.post(baseurl + 'user/unuser/', data=json.dumps(dic), headers=headers).content
        response = json.loads(response)
        if response['code'] not in [1000]:
            print '新增失败' + str(response)
            print dic['usernameC']
            print (dic['id'])
        else:
            f = open('unuser3.0-old_new_id', 'a')
            print (dic['id'])
            print response['result']
            f.writelines(json.dumps({'old': (dic['id']), 'new': response['result']['id']}))
            f.writelines('\n')
            f.close()