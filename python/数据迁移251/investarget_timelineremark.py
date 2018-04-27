#coding=utf-8
import json
import traceback

import datetime
import pymysql
import requests
from pypinyin import slug as hanzizhuanpinpin
import _mssql
#海拓token
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
#车创token
token2 = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecg'

# baseurl = 'http://39.107.14.53:8080/'
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
            now = str(datetime.datetime.now())
            # orgid = datamanager.getNewOrgId(row['OrgId'])
            userid = datamanager.getNewUserId(row['TransactionId'])
            timelineid = datamanager.getNewTimeLineId(row['TimeLineId'])
            if timelineid:
                dic = {
                    'createuser' : userid if userid else 1,
                    'timeline': timelineid,
                    'remark': row['Remark'],
                    'createdtime':str(row['CreationTime']) if row['CreationTime'] else now ,
                    # 'lastmodifytime':str(row['LastModificationTime']) if row['CreationTime'] else None,
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
        self.allTimeline = self.getAllTimeline()
        self.allMySqlUser = self.getAllMySqlUser()

    def getAllMySqlUser(self):
        res = []
        file = open('user-old_new_id')
        for line in file:
            if len(line) > 10:
                res.append(json.loads(line.replace('\n', '')))
        return res

    def getNewUserId(self, oldid):
        if oldid:
            for dic in self.allMySqlUser:
                if dic['old'] == oldid:
                    return dic['new']
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
