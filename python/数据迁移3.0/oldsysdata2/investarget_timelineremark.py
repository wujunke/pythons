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
    addTimelineRemark()



def addTimelineRemark():
    times = 0
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    datamanager = DataManager()
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT InvestargetDb_v2.dbo.TimeLineRemarks.*,InvestargetDb_v2.dbo.ProjectTimeLine.TransactionId FROM InvestargetDb_v2.dbo.TimeLineRemarks INNER JOIN InvestargetDb_v2.dbo.ProjectTimeLine ON TimeLineRemarks.TimeLineId = ProjectTimeLine.Id WHERE TimeLineRemarks.IsDeleted = 0 AND ProjectTimeLine.IsDeleted = 0"
    # sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND id = 1155"
    conn.execute_query(sql)

    for row in conn:
        times = times + 1
        try:
            # orgid = datamanager.getNewOrgId(row['OrgId'])
            userid = datamanager.getNewUserId(row['TransactionId'])
            timelineid = datamanager.getNewTimeLineId(row['TimeLineId'])
            if timelineid:
                dic = {
                    'createuser' : userid,
                    'timeline': timelineid,
                    'remark': row['Remark'],
                    'createdtime':str(row['CreationTime']),
                    'lastmodifytime':str(row['LastModificationTime']),
                    'lastmodifyuser':datamanager.getNewUserId(row['LastModifierUserId']),
                }
                response = requests.post(baseurl + 'timeline/remark/', data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] != 1000:
                    print '新增失败' + str(response)
                    print str(row['Id'])+ '*****' + str(times)
                    print '====='
                else:
                    f = open('timelineremark-old_new_id', 'a')
                    f.writelines(json.dumps({'old': row['Id'], 'new': response['result']['id']}))
                    f.writelines('\n')
                    f.close()
            else:
                print '未找到匹配timeline'  +  '***' + str(row['Id'])
                print timelineid
                print '*****'
        except Exception:
            print '失败'  + str(row['Id'])
            print traceback.format_exc()
            print '-----'
    conn.close()


class DataManager():
    def __init__(self):
        self.allMySqlUser = self.getAllMySqlUser()
        self.allUser = self.getAllUser()
        self.allTimeline = self.getAllTimeline()

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
            if sqlserverid ==  2000045:
                mysqlid = 8
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


    def getAllTimeline(self):
        res = []
        file = open('timeline-old_new_id')
        for line in file:
            if len(line) > 10:
                res.append(json.loads(line.replace('\n','')))
        return res

    def getNewTimeLineId(self,sqlserverid):
        if sqlserverid:
            mysqlid = None
            for area in self.allTimeline:
                if area['old'] == sqlserverid:
                    mysqlid = area['new']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None


if __name__=="__main__":
    main()
