#coding=utf-8
import json

import datetime
import pymysql
import requests
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
    addtimeline()


def addtimeline():
    times = 0
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016',)
    datamanager = DataManager()
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT InvestargetDb_v2.dbo.ProjectTimeLine.*,InvestargetDb_v2.dbo.ProjectTimeLine_TransactionStatus.TransactionStatusId,InvestargetDb_v2.dbo.ProjectTimeLine_TransactionStatus.InDate,InvestargetDb_v2.dbo.ProjectTimeLine_TransactionStatus.AlertCycle FROM InvestargetDb_v2.dbo.ProjectTimeLine INNER JOIN InvestargetDb_v2.dbo.ProjectTimeLine_TransactionStatus ON ProjectTimeLine_TransactionStatus.TimeLineId = ProjectTimeLine.Id WHERE ProjectTimeLine.IsDeleted=0 AND ProjectTimeLine_TransactionStatus.IsDeleted=0 AND ProjectTimeLine_TransactionStatus.IsActive = 1"
    conn.execute_query(sql)
    for row in conn:
        times = times + 1
        investor =  datamanager.getNewUserId(row['InvestorId'])
        trader = datamanager.getNewUserId(row['TransactionId'])
        proj = datamanager.getNewProjectId(row['ProjectId'])
        createuser = datamanager.getNewUserId(row['CreatorUserId'])
        msg = []
        now = str(datetime.datetime.now())
        if investor is None:
            msg.append('未找到匹配投资人')
        if trader is None:
            msg.append('未找到匹配交易师')
        if proj is None:
            msg.append('未找到匹配项目')
        if createuser is None:
            createuser = 1
        if investor and trader and proj:
            try:
                dic = {
                    'timelinedata':{
                        'investor': investor,
                        'trader': trader,
                        'proj': proj,
                        'isClose': row['IsClose'] if row['IsClose'] else False,
                        'closeDate': str(row['CloseDate']) if row['CloseDate'] else None,
                        'contractedServiceTime': str(row['ContractedServiceTime']) if row[
                            'ContractedServiceTime'] else None,
                        'turnoverTime': str(row['TurnoverTime']) if row['TurnoverTime'] else None,
                        'createdtime': str(row['CreationTime']) if row['CreationTime'] else now,
                        'createuser': createuser,
                    },

                    'statusdata':{
                        'transationStatus':row['TransactionStatusId'],
                        'inDate':str(row['InDate']) if row['InDate'] else None,
                        'alertCycle':row['AlertCycle'],
                        'isActive':True,
                    },

                    }
                response = requests.post(baseurl + 'timeline/' , data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] not in [1000]:
                    print '新增失败' + str(response)
                    print row['Id']
                else:
                    f = open('timeline-old_new_id', 'a')
                    f.writelines(json.dumps({'old':row['Id'] ,'new':response['result']['id']}))
                    f.writelines('\n')
                    f.close()

            except Exception as err:
                print 'shibai'
                print  err
                print row['Id']
        else:
            print row['Id']
            print msg[0]
    print times
    conn.close()




def updatetimeline():
    times = 0
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016',)
    datamanager = DataManager()
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT InvestargetDb_v2.dbo.ProjectTimeLine.*,InvestargetDb_v2.dbo.ProjectTimeLine_TransactionStatus.TransactionStatusId,InvestargetDb_v2.dbo.ProjectTimeLine_TransactionStatus.InDate,InvestargetDb_v2.dbo.ProjectTimeLine_TransactionStatus.AlertCycle FROM InvestargetDb_v2.dbo.ProjectTimeLine INNER JOIN InvestargetDb_v2.dbo.ProjectTimeLine_TransactionStatus ON ProjectTimeLine_TransactionStatus.TimeLineId = ProjectTimeLine.Id WHERE ProjectTimeLine.IsDeleted=0 AND ProjectTimeLine_TransactionStatus.IsDeleted=0 AND ProjectTimeLine_TransactionStatus.IsActive = 1 AND ProjectTimeLine.Id > 279"
    conn.execute_query(sql)
    for row in conn:
        times = times + 1
        newtimelineid =  datamanager.getNewTimelineId(row['Id'])
        if newtimelineid:
            try:
                dic = {
                    'timelinedata':{
                        # 'investor': investor,
                        # 'trader': trader,
                        # 'proj': proj,
                        'isClose': row['IsClose'] if row['IsClose'] else False,
                        'closeDate': str(row['CloseDate']) if row['CloseDate'] else None,
                        # 'contractedServiceTime': str(row['ContractedServiceTime']) if row[
                        #     'ContractedServiceTime'] else None,
                        # 'turnoverTime': str(row['TurnoverTime']) if row['TurnoverTime'] else None,
                        # 'createdtime': str(row['CreationTime']) if row['CreationTime'] else now,
                        # 'createuser': createuser,
                    },

                    # 'statusdata':{
                    #     'transationStatus':row['TransactionStatusId'],
                    #     'inDate':str(row['InDate']) if row['InDate'] else None,
                    #     'alertCycle':row['AlertCycle'],
                    #     'isActive':True,
                    # },

                    }
                response = requests.put(baseurl + 'timeline/%s/?lang=cn'%newtimelineid , data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] not in [1000]:
                    print '新增失败' + str(response)
                    print row['Id']
                else:
                    f = open('timelineupdate-old_new_id', 'a')
                    f.writelines(json.dumps({'old':row['Id'] ,'new':response['result']['id']}))
                    f.writelines('\n')
                    f.close()

            except Exception as err:
                print 'shibai'
                print  err
                print row['Id']
        else:
            print row['Id']
    print times
    conn.close()





class DataManager():
    def __init__(self):
        self.allMySqlUser = self.getAllMySqlUser()
        self.allMySqlProj = self.getAllMySqlProject()
        # self.allMySqlTimeline = self.getAllMySqlTimeline()

    def getAllMySqlUser(self):
        res = []
        file = open('user-old_new_id')
        for line in file:
            if len(line) > 10:
                res.append(json.loads(line.replace('\n', '')))
        return res

    def getNewUserId(self,oldid):
        if oldid:
            for dic in self.allMySqlUser:
                if dic['old'] == oldid:
                    return dic['new']
            return None
        else:
            return None

    def getAllMySqlProject(self):
        res = []
        file = open('proj-old_new_id')
        for line in file:
            if len(line) > 10:
                res.append(json.loads(line.replace('\n', '')))
        return res

    def getNewProjectId(self,oldid):
        if oldid:
            for dic in self.allMySqlProj:
                if dic['old'] == oldid:
                    return dic['new']
            return None
        else:
            return None


    # def getAllMySqlTimeline(self):
    #     res = []
    #     file = open('timeline-old_new_id')
    #     for line in file:
    #         if len(line) > 10:
    #             res.append(json.loads(line.replace('\n', '')))
    #     return res
    #
    # def getNewTimelineId(self,oldid):
    #     if oldid:
    #         for dic in self.allMySqlTimeline:
    #             if dic['old'] == oldid:
    #                 return dic['new']
    #         return None
    #     else:
    #         return None



if __name__=="__main__":
    main()



# createtime = statudata.pop('createdtime').encode('utf-8')[0:19]
                        # if createtime not in ['None',None,u'None','none']:
                            # statudata['createdtime'] = datetime.datetime.strptime(createtime, "%Y-%m-%d %H:%M:%S")