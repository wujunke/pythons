#coding=utf-8
import _mssql
import json
import requests

import pymysql.cursors

token = 'd150b8c90ad3855e77cc807999a6ed0a4d78b58074476225'

baseurl = 'http://192.168.1.201:8000/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }


class DataManager():
    def __init__(self):
        # self.allMySqlUser = self.getAllMySqlUser()
        #
        # self.allUser = self.getAllUser()
        self.aaa = ''

    def getProjTags(self,projSqlServerId):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT TagId FROM InvestargetDb_v2.dbo.Project_Tag WHERE IsDeleted = 0 AND ProjectId = %s"%projSqlServerId
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res
    def getProjIndustries(self,projSqlServerId):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.Project_Industry WHERE IsDeleted = 0 AND ProjectId = %s"%projSqlServerId
        conn.execute_query(sql)
        res = []
        for area in conn:
            newId = self.getNewIndustryId(area['IndustryId'])
            if newId:
                indus = {'industry':newId,'key':area['Key'],'bucket':area['Bucket']}
                res.append(indus)
        conn.close()
        return res



    def getAllUser(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT UserName,Id FROM InvestargetDb_v2.dbo.\"User\" WHERE IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getAllMySqlUser(self):
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
                sql = "SELECT * FROM user WHERE is_deleted = 0"
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    # def getNewUserId(self, sqlserverid):
    #     if sqlserverid:
    #         mysqlid = None
    #         realname = None
    #         for area in self.allUser:
    #             if area['Id'] == sqlserverid:
    #                 realname = area['UserName']
    #         if realname is not None:
    #             for one in self.allMySqlUser:
    #                 if one['usercode'] == realname:
    #                     mysqlid = one['id']
    #         if mysqlid is not None:
    #             return mysqlid
    #         else:
    #             return None
    #     else:
    #         return None

a = DataManager()
res = a.getProjIndustries(62)
print res
# print len(a.allMySqlUser)