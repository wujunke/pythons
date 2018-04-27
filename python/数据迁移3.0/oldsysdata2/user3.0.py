#coding=utf8
import json

import datetime
import pymysql
import requests


class DataManager():
    def __init__(self):

        self.allMySqlOrg = self.getAllMySqlOrg()
        self.allMySqlUserGroups = self.getAllUserGroup()

        self.allMySqlUserTags = self.getAllUserTags()

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
                sql = "SELECT *  FROM user WHERE datasource_id =2"
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getAllMySqlOrg(self):
        res = []
        file = open('org3.0-old_new_id')
        for line in file:
            if len(line) > 10:
                res.append(json.loads(line.replace('\n', '')))
        return res

    def getNewOrgId(self,oldid):
        if oldid:
            for dic in self.allMySqlOrg:
                if dic['old'] == oldid:
                    return dic['new']
            return None
        else:
            return None


    def getAllUserGroup(self):
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
                sql = "SELECT * FROM user_groups"
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getNewUserGroup(self,olduserid):
        if olduserid:
            for dic in self.allMySqlUserGroups:
                if dic['myuser_id'] == olduserid:
                    return [dic['group_id']]
            return None
        else:
            return None

    def getAllUserTags(self):
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
                sql = "SELECT * FROM user_tags"
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getNewUserTags(self, olduserid):
        if oldorgid:
            res = []
            for dic in self.allMySqlUserTags:
                if dic['user_id'] == oldid:
                    res.append(dic['tag_id'])
            if len(res)> 0:
                return res
            else:
                return None
        else:
            return None





#海拓token
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
#车创token
token2 = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecg'
baseurl = 'http://39.107.14.53:8080/'
headers = {
        'token':token2,
        'source':'2',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }

times = 0
datamanager = DataManager()

for dic in datamanager.alluser:
    oldid = dic.pop('id')
    oldorgid = dic.pop('org_id')
    for key,value in dic.items():
        if isinstance(value,datetime.datetime):
            if value:
                dic[key] = str(value)
    dic.pop('createuser_id')
    dic.pop('lastmodifyuser_id')
    dic.pop('deleteduser_id')
    dic['org'] = datamanager.getNewOrgId(oldorgid)
    if datamanager.getNewUserGroup(oldid):
        dic['groups'] = datamanager.getNewUserGroup(oldid)
    dic['tag'] = datamanager.getNewUserTags(oldid)

    response = requests.post(baseurl + 'user/', data=json.dumps(dic), headers=headers).content
    response = json.loads(response)
    if response['code'] not in [1000]:
        print '新增失败' + str(response)
        print dic['usernameC']
        print oldid
    else:
        f = open('user3.0-old_new_id', 'a')
        print oldid
        print response['result']
        f.writelines(json.dumps({'old': oldid, 'new': response['result']['id']}))
        f.writelines('\n')
        f.close()