#coding=utf-8
import json
import traceback

import pymysql
import requests
import time
from pypinyin import slug as hanzizhuanpinpin
import _mssql

token = '57c5c6a2033f69d80eaaa536eb4275acb7b535d925178e38'

baseurl = 'http://192.168.1.201:8000/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }

def main():
    addProjFavorite()



def addProjFavorite():
    times = 0

    datamanager = DataManager()

    for row in datamanager.allProjFavorite:
        times = times + 1
        try:
            print row['Id']
            userid = datamanager.getNewUserId(row['UserId'])
            proj = datamanager.getNewProjectId(row['ProjectId'])
            traderId = datamanager.getNewUserId(row['TransactionId'])
            createuser = datamanager.getNewUserId(row['CreatorUserId'])
            if userid and proj:
                if row['ftype'] in [3,5]:
                    if traderId:
                        pass
                    else:
                        print 'trader 未找到'
                        continue
                dic = {
                    'user' : userid,
                    'trader': traderId,
                    'favoritetype':row['ftype'],
                    'projs':[proj],
                    'createuser': createuser if createuser else 8,
                    'createdtime':str(row['CreationTime']),
                }
                response = requests.post(baseurl + 'proj/favorite/', data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] != 1000:
                    print '新增失败' + str(response)
                    print str(row['Id'])+ '*****' + str(times)
            else:
                print '未找到匹配user'  +  '***' + str(row['Id'])
                print 'investor        ' + '       trader'
                print userid
                print proj
        except Exception:
            print 'shibai'  + str(row['Id'])
            print traceback.format_exc()
            pass





class DataManager():
    def __init__(self):
        self.allMySqlUser = self.getAllMySqlUser()

        self.allUser = self.getAllUser()
        self.allProj = self.getAllProject()
        self.allMySqlProj = self.getAllMySqlProject()

        self.allProjFavorite = self.getAllProjFavorite()
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

    def getNewUserId(self, sqlserverid):
        if sqlserverid:
            mysqlid = None
            realname = None
            for area in self.allUser:
                if area['Id'] == sqlserverid:
                    realname = area['UserName']
            if realname is not None:
                for one in self.allMySqlUser:
                    if one['usercode'] == realname:
                        mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None


    def getAllProjFavorite(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT InvestargetDb_v2.dbo.Project_Favorite.* FROM InvestargetDb_v2.dbo.Project_Favorite INNER JOIN InvestargetDb_v2.dbo.Project ON InvestargetDb_v2.dbo.Project.Id = InvestargetDb_v2.dbo.Project_Favorite.ProjectId INNER JOIN InvestargetDb_v2.dbo.\"User\" ON InvestargetDb_v2.dbo.\"User\".Id = InvestargetDb_v2.dbo.Project_Favorite.TransactionId or InvestargetDb_v2.dbo.\"User\".Id = InvestargetDb_v2.dbo.Project_Favorite.UserId WHERE Project_Favorite.IsDeleted = 0 AND Project.IsDeleted = 0 AND \"User\".IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getAllProject(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT Code,Id FROM InvestargetDb_v2.dbo.Project WHERE IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getAllMySqlProject(self):
        res = []
        connection = pymysql.connect(host='192.168.1.251',
                                     user='root',
                                     password='investarget@2017',
                                     db='investarget',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT id,code FROM project WHERE is_deleted = 0"
                cursor.execute(sql)
                result = cursor.fetchall()
                for area in result:
                    res.append(area)
        finally:
            connection.close()
        return res

    def getNewProjectId(self, sqlserverid):
        if sqlserverid:
            mysqlid = None
            realname = None
            for area in self.allProj:
                if area['Id'] == sqlserverid:
                    realname = area['Code']
            if realname is not None:
                for one in self.allMySqlProj:
                    if one['code'] == realname:
                        mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None


if __name__=="__main__":
    main()




# createtime = data.pop('createdtime').encode('utf-8')[0:18]
# print createtime
# data['createdtime'] = datetime.datetime.strptime(createtime, "%Y-%m-%d %H:%M:%S")