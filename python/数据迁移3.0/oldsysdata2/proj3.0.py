#coding=utf8
import json

import datetime
import pymysql
import requests


class DataManager():
    def __init__(self):

        self.allProj = self.getAllProj()

        self.allMySqlProjIndustries = self.getAllProjindustries()

        self.allMySqlProjTags = self.getAllProjTags()

        self.allMySqlProjServices = self.getAllProjServices()

        self.allMySqlProjTransactiontype = self.getAllProjTransactontypes()

        self.allMySqlProjAttachments = self.getAllProjAttachments()

        self.allMySqlProjFinances = self.getAllProjFinances()

    def getAllProj(self):
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
                sql = "SELECT *  FROM project WHERE datasource_id = 2"
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getAllProjTags(self):
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
                sql = "SELECT * FROM project_tags "
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getNewProjTags(self, olduserid):
        if olduserid:
            res = []
            for dic in self.allMySqlProjTags:
                if dic['proj_id'] == olduserid:
                    res.append(dic['tag_id'])
            if len(res)> 0:
                return res
            else:
                return None
        else:
            return None


    def getAllProjindustries(self):
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
                    sql = "SELECT * FROM project_industries"
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    for area in result:
                        res.append(area)
            finally:
                connection.close()
            return res

    def getNewProjIndustries(self, olduserid):
            if olduserid:
                res = []
                for dic in self.allMySqlProjIndustries:
                    if dic['proj_id'] == olduserid:
                        for key, value in dic.items():
                            if isinstance(value, datetime.datetime):
                                if value:
                                    dic[key] = str(value)
                        mindic = dic.copy()
                        mindic.pop('id')
                        mindic['industry'] = mindic['industry_id']
                        mindic.pop('createuser_id')
                        mindic.pop('deleteduser_id')
                        res.append(mindic)
                if len(res) > 0:
                    return res
                else:
                    return None
            else:
                return None

    def getAllProjServices(self):
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
                        sql = "SELECT * FROM project_services "
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        for area in result:
                            res.append(area)
                finally:
                    connection.close()
                return res

    def getNewProjServices(self, olduserid):
                if olduserid:
                    res = []
                    for dic in self.allMySqlProjServices:
                        if dic['proj_id'] == olduserid:
                            res.append(dic['service_id'])
                    if len(res) > 0:
                        return res
                    else:
                        return None
                else:
                    return None

    def getAllProjTransactontypes(self):
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
                            sql = "SELECT * FROM project_TransactionType "
                            cursor.execute(sql)
                            result = cursor.fetchall()
                            for area in result:
                                res.append(area)
                    finally:
                        connection.close()
                    return res

    def getNewProjTransactiontypes(self, olduserid):
                    if olduserid:
                        res = []
                        for dic in self.allMySqlProjTransactiontype:
                            if dic['proj_id'] == olduserid:
                                res.append(dic['transactionType_id'])
                        if len(res) > 0:
                            return res
                        else:
                            return None
                    else:
                        return None

    def getAllProjAttachments(self):
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
                                sql = "SELECT * FROM projectAttachment "
                                cursor.execute(sql)
                                result = cursor.fetchall()
                                for area in result:
                                    res.append(area)
                        finally:
                            connection.close()
                        return res

    def getNewProjAttachments(self, olduserid):
                        if olduserid:
                            res = []
                            for dic in self.allMySqlProjAttachments:
                                if dic['proj_id'] == olduserid:
                                    for key, value in dic.items():
                                        if isinstance(value, datetime.datetime):
                                            if value:
                                                dic[key] = str(value)
                                    mindic = dic.copy()
                                    mindic.pop('proj_id')
                                    mindic.pop('id')
                                    mindic.pop('createuser_id')
                                    mindic.pop('lastmodifyuser_id')
                                    mindic.pop('deleteduser_id')
                                    res.append(mindic)
                            if len(res) > 0:
                                return res
                            else:
                                return None
                        else:
                            return None

    def getAllProjFinances(self):
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
                                    sql = "SELECT * FROM projectFinance "
                                    cursor.execute(sql)
                                    result = cursor.fetchall()
                                    for area in result:
                                        res.append(area)
                            finally:
                                connection.close()
                            return res

    def getNewProjFinances(self, olduserid):
                            if olduserid:
                                res = []
                                for dic in self.allMySqlProjFinances:
                                    if dic['proj_id'] == olduserid:
                                        for key, value in dic.items():
                                            if isinstance(value, datetime.datetime):
                                                if value:
                                                    dic[key] = str(value)
                                        mindic = dic.copy()
                                        mindic.pop('proj_id')
                                        mindic.pop('id')
                                        mindic.pop('createuser_id')
                                        mindic.pop('lastmodifyuser_id')
                                        mindic.pop('deleteduser_id')
                                        res.append(mindic)
                                if len(res) > 0:
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

supportuser = 100007222
for dic in datamanager.allProj:
    oldid = dic.pop('id')

    for key,value in dic.items():
        if isinstance(value,datetime.datetime):
            if value:
                dic[key] = str(value)
    dic.pop('createuser_id')
    dic.pop('lastmodifyuser_id')
    dic.pop('deleteduser_id')
    if datamanager.getNewProjTags(oldid):
        dic['tags'] = datamanager.getNewProjTags(oldid)
    if datamanager.getNewProjIndustries(oldid):
        dic['industries'] = datamanager.getNewProjIndustries(oldid)
    if datamanager.getNewProjTransactiontypes(oldid):
        dic['transactionType'] = datamanager.getNewProjTransactiontypes(oldid)
    if datamanager.getNewProjAttachments(oldid):
        dic['projAttachment'] = datamanager.getNewProjAttachments(oldid)
    if datamanager.getNewProjFinances(oldid):
        dic['finance'] = datamanager.getNewProjFinances(oldid)
    if datamanager.getNewProjServices(oldid):
        dic['service'] = datamanager.getNewProjServices(oldid)
    dic['supportUser'] = supportuser


    response = requests.post(baseurl + 'proj/', data=json.dumps(dic), headers=headers).content
    response = json.loads(response)
    if response['code'] not in [1000]:
        print '新增失败' + str(response)
        print dic['projtitleC']
        print oldid
    else:
        f = open('proj3.0-old_new_id', 'a')
        print oldid
        print response['result']
        f.writelines(json.dumps({'old': oldid, 'new': response['result']['id']}))
        f.writelines('\n')
        f.close()