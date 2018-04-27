#coding=utf-8
import json
import traceback

import pymysql
import requests
import time
from pypinyin import slug as hanzizhuanpinpin
import _mssql


#海拓token
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
#车创token
token2 = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecg'
baseurl = 'http://39.107.14.53:8080/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }

def main():
    addUserRemark()



def addUserRemark():
    times = 0
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    datamanager = DataManager()
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT InvestargetDb_v2.dbo.UserRemarks.* FROM InvestargetDb_v2.dbo.\"User\" INNER JOIN InvestargetDb_v2.dbo.UserRemarks ON InvestargetDb_v2.dbo.UserRemarks.UserId = InvestargetDb_v2.dbo.\"User\".Id WHERE \"User\".IsDeleted = 0 AND UserRemarks.IsDeleted = 0"
    # sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND id = 1155"
    conn.execute_query(sql)

    for row in conn:
        times = times + 1
        try:
            userid = datamanager.getNewUserId(row['UserId'])
            createuser = datamanager.getNewUserId(row['CreatorUserId'])
            if userid:
                dic = {
                    'user' : userid,
                    'createuser': createuser if createuser else 1,
                    'remark': row['Remark'],
                    'createdtime':str(row['CreationTime']),
                }
                response = requests.post(baseurl + 'user/remark/', data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] != 1000:
                    print '新增失败' + str(response)
                    print str(row['Id'])+ '*****' + str(times)
            else:
                print '未找到匹配user'  +  '***' + str(row['Id'])
        except Exception:
            print 'shibai'  + str(row['Id'])
            print traceback.format_exc()
            pass
    conn.close()


def addUserTag():
    times = 0
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    datamanager = DataManager()
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT UserId FROM InvestargetDb_v2.dbo.\"User\" INNER JOIN InvestargetDb_v2.dbo.User_Tags ON InvestargetDb_v2.dbo.User_Tags.UserId = InvestargetDb_v2.dbo.\"User\".Id WHERE \"User\".IsDeleted = 0 AND User_Tags.IsDeleted= 0 GROUP BY User_Tags.UserId HAVING count(User_Tags.UserId) > 0"
    # sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND id = 1155"
    conn.execute_query(sql)

    for row in conn:
        times = times + 1
        try:
            userid = datamanager.getNewUserId(row['UserId'])
            if userid:
                tags = datamanager.getUserTags(row['UserId'])
                if len(tags) > 0:
                    dic = {
                        'userlist' : [userid],
                        'userdata':{
                            'tags': tags,
                        },
                    }
                    response = requests.put(baseurl + 'user/', data=json.dumps(dic), headers=headers).content
                    response = json.loads(response)
                    if response['code'] != 1000:
                        print '新增失败' + str(response)
                        print str(row['UserId'])+ '*****' + str(times)
                else:
                    print '未找到匹配标签' + '***' + str(row['UserId'])
            else:
                print '未找到匹配user'  +  '***' + str(row['UserId'])
        except Exception:
            print 'shibai'  + str(row['UserId'])
            print traceback.format_exc()
            pass
    conn.close()


class DataManager():
    def __init__(self):
        self.allMySqlUser = self.getAllMySqlUser()

        self.allUser = self.getAllUser()

        self.allTag = self.getAllTag()
        self.allMySqlTag = self.getAllMySqplTag()

        self.allUserTag = self.getAllUserTags()

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
        connection = pymysql.connect(host='39.107.14.53',
                                     user='root',
                                     password='Investarget@2017',
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


    def getAllTag(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.Tag WHERE IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res
    def getAllMySqplTag(self):
        res = requests.get(baseurl + 'source/tag',headers={'source': '1',})
        return json.loads(res.content).get('result',None)

    def getNewTagId(self,sqlserverid):
        if sqlserverid:
            mysqlid = None
            realname = None
            for area in self.allTag:
                if area['Id'] == sqlserverid:
                    realname = area['TagNameC']
            if realname is not None:
                for one in self.allMySqlTag:
                    if one['nameC'] == realname:
                        mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None

    def getAllUserTags(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT InvestargetDb_v2.dbo.User_Tags.* FROM InvestargetDb_v2.dbo.\"User\" INNER JOIN InvestargetDb_v2.dbo.User_Tags ON InvestargetDb_v2.dbo.User_Tags.UserId = InvestargetDb_v2.dbo.\"User\".Id WHERE \"User\".IsDeleted = 0 AND User_Tags.IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getUserTags(self, userId):
        tags = []
        if userId:
            for transa in self.allUserTag:
                oneId = transa['UserId']
                if oneId == userId:
                    newid = self.getNewTagId(transa['TagId'])
                    if newid:
                        tags.append(newid)
        return tags

if __name__=="__main__":
    main()




# createtime = data.pop('createdtime')
# print createtime
# data['createdtime'] = datetime.datetime.strptime(createtime.encode('utf-8')[0:19], "%Y-%m-%d %H:%M:%S")