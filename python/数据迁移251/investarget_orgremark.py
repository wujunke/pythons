#coding=utf-8
import json
import traceback

import pymysql
import requests
from pypinyin import slug as hanzizhuanpinpin
import _mssql

token = '57b514db76baafb64198a7753c18b88e6999c49d4bb20982'

baseurl = 'http://192.168.1.201:8000/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }

def main():
    addOrgRemark()



def addOrgRemark():
    times = 0
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    datamanager = DataManager()
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT InvestargetDb_v2.dbo.OrgRemarks.* FROM InvestargetDb_v2.dbo.OrgRemarks WHERE IsDeleted = 0"
    # sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND id = 1155"
    conn.execute_query(sql)

    for row in conn:
        times = times + 1
        try:
            # orgid = datamanager.getNewOrgId(row['OrgId'])
            userid = datamanager.getNewUserId(row['CreatorUserId'])
            # if orgid:
            #     dic = {
            #         'org' : orgid,
            #         'createuser': 8,
            #         'remark': row['Remark'],
            #         # 'createdtime':row['CreationTime'],
            #         # 'lastmodifytime':row['LastModificationTime'],
            #         # 'lastmodifyuser':row['LastModifierUserId'],
            #     }
            #     response = requests.post(baseurl + 'org/remark/', data=json.dumps(dic), headers=headers).content
            #     response = json.loads(response)
            #     if response['code'] != 1000:
            #         print '新增失败' + str(response)
            #         print str(row['Id'])+ '*****' + str(times)
            # else:
            #     print '未找到匹配org'  +  '***' + str(row['Id'])
        except Exception:
            print 'shibai'  + str(row['Id'])
            print traceback.format_exc()
            pass
    conn.close()


class DataManager():
    def __init__(self):
        self.allMySqlUser = self.getAllMySqlUser()
        self.allOrg = self.getAllOrg()
        self.allMySqlOrg = self.getAllMySqlOrg()

        self.allUser = self.getAllUser()


    def getAllMySqlOrg(self):
        res = requests.get(baseurl + 'org/?page_size=100000', headers={'source': '1', })
        result = json.loads(res.content).get('result', {})
        return result.get('data', None)
    def getAllOrg(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT Name,Id FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getNewOrgId(self, sqlserverid):
        if sqlserverid:
            mysqlid = None
            realname = None
            for area in self.allOrg:
                if area['Id'] == sqlserverid:
                    realname = area['Name']
            if realname is not None:
                for one in self.allMySqlOrg:
                    if one['orgnameC'] == realname:
                        mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None

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

if __name__=="__main__":
    main()
