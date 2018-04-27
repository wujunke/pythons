#coding=utf-8
import json
import traceback

import pymysql
import requests
import time
from pypinyin import slug as hanzizhuanpinpin
import _mssql

token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'

# baseurl = 'http://39.107.14.53:8080/'
baseurl = 'http://192.168.1.201:8000/'

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
    sql = "SELECT InvestargetDb_v2.dbo.UserRemarks.* FROM InvestargetDb_v2.dbo.\"User\" INNER JOIN InvestargetDb_v2.dbo.UserRemarks ON InvestargetDb_v2.dbo.UserRemarks.UserId = InvestargetDb_v2.dbo.\"User\".Id WHERE \"User\".IsDeleted = 0 AND UserRemarks.IsDeleted = 0 AND UserRemarks.Id >= 2210"
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
                    'lastmodifytime':str(row['LastModificationTime']) if row['LastModificationTime'] else None,
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
    sql = "SELECT UserId FROM InvestargetDb_v2.dbo.\"User\" INNER JOIN InvestargetDb_v2.dbo.User_Tags ON InvestargetDb_v2.dbo.User_Tags.UserId = InvestargetDb_v2.dbo.\"User\".Id WHERE \"User\".IsDeleted = 0 AND \"User\".Id >= 2172983 AND User_Tags.IsDeleted= 0 GROUP BY User_Tags.UserId HAVING count(User_Tags.UserId) > 0"
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
        self.allUser = self.getAllUser()
        self.allTag = self.getAllTag()
        self.allMySqlTag = self.getAllMySqplTag()
        self.allUserTag = self.getAllUserTags()

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