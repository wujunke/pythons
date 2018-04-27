#coding=utf-8
import json
import traceback

import pymysql
import requests
import time
from pypinyin import slug as hanzizhuanpinpin
import _mssql

baseurl = 'http://39.107.14.53:8080/'
#海拓token
# baseurl = 'http://192.168.1.201:8000/'

token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
#车创token
token2 = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecg'
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

    for row in datamanager.allCommonUserRelations:
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
                    'relationtype':False,
                    'createuser': createuser if createuser else 1,
                    'createdtime':str(row['CreationTime']),
                }  #investor:100005608     trader:100000031
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

        self.allUser = self.getAllUser()
        self.allCommonUserRelations = self.getAllCommonUserRelations()
        self.allStrongUserRelation = self.getAllStrongUserRelations()

    def getAllUser(self):
        res = []
        file = open('user-old_new_id')
        for line in file:
            if len(line) > 10:
                res.append(json.loads(line.replace('\n', '')))
        return res

    def getNewUserId(self, oldid):
        if oldid:
            for dic in self.allUser:
                if dic['old'] == oldid:
                    return dic['new']
            return None
        else:
            return None


    def getAllCommonUserRelations(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.UserCommonTransaction WHERE UserCommonTransaction.IsDeleted = 0 AND UserId >= 2172983"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getAllStrongUserRelations(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.UserCommonTransaction WHERE UserCommonTransaction.IsDeleted = 0 AND UserCommonTransaction.IsStrong = 1 "
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