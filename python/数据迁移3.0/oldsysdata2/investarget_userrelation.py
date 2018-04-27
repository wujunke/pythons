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
    addUserRelation()



def addUserRelation():
    times = 0
    # conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    datamanager = DataManager()
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    # sql = "SELECT InvestargetDb_v2.dbo.UserCommonTransaction.* FROM InvestargetDb_v2.dbo.\"User\" INNER JOIN InvestargetDb_v2.dbo.UserCommonTransaction ON InvestargetDb_v2.dbo.UserCommonTransaction.UserId = InvestargetDb_v2.dbo.\"User\".Id WHERE \"User\".IsDeleted = 0 AND  UserCommonTransaction.IsStrong = 1 AND UserCommonTransaction.IsDeleted = 0"
    # # sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND id = 1155"
    # conn.execute_query(sql)

    for row in datamanager.allStrongUserRelation:
        times = times + 1
        try:
            print row['Id']
            userid = datamanager.getNewUserId(row['UserId'])
            traderId = datamanager.getNewUserId(row['TransactionId'])
            createuser = datamanager.getNewUserId(row['CreatorUserId'])
            if userid and traderId:
                dic = {
                    'investoruser' : userid,
                    'traderuser': traderId,
                    'relationtype':True,
                    'createuser': createuser if createuser else 1,
                    'createdtime':str(row['CreationTime']),
                }
                response = requests.post(baseurl + 'user/relationship/', data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] != 1000:
                    print '新增失败' + str(response)
                    print str(row['Id'])+ '*****' + str(times)
            else:
                print '未找到匹配user'  +  '***' + str(row['Id'])
                print 'investor        ' + '       trader'
                print userid
                print traderId
        except Exception:
            print 'shibai'  + str(row['Id'])
            print traceback.format_exc()
            pass
    # conn.close()




class DataManager():
    def __init__(self):
        self.allMySqlUser = self.getAllMySqlUser()

        self.allUser = self.getAllUser()
        self.allCommonUserRelations = self.getAllCommonUserRelations()
        self.allStrongUserRelation = self.getAllStrongUserRelations()

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


    def getAllCommonUserRelations(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.UserCommonTransaction WHERE UserCommonTransaction.IsDeleted = 0 AND UserCommonTransaction.IsStrong = 0 AND UserCommonTransaction.IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getAllStrongUserRelations(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.UserCommonTransaction WHERE UserCommonTransaction.IsDeleted = 0 AND UserCommonTransaction.IsStrong = 1 AND UserCommonTransaction.IsDeleted = 0 "
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    # def getUserRelations(self, userId):
    #     relations = []
    #     if userId:
    #         for transa in self.allUserRelations:
    #             InvestorId = transa['UserId']
    #             transaId = transa['TransactionId']
    #             if InvestorId == userId:
    #                 newid = self.getNewUserId(transaId)
    #                 if newid:
    #                     relations.append(newid)
    #     return relations

if __name__=="__main__":
    main()




# createtime = data.pop('createdtime').encode('utf-8')[0:18]
# print createtime
# data['createdtime'] = datetime.datetime.strptime(createtime, "%Y-%m-%d %H:%M:%S")