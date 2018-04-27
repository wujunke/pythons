#coding=utf-8
import json

import pymysql
import requests
import _mssql

token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'

baseurl = 'http://192.168.1.201:8000/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }


def main():
    addPublicDataroom()



def addPublicDataroom():
    times = 0
    datamanager = DataManager()
    for row in datamanager.allDataroom:
        times = times + 1
        proj = datamanager.getNewProjectId(row['ProjectId'])
        createuser = datamanager.getNewUserId(row['CreatorUserId'])
        type = 0
        dic = {}
        if row['IsPublic']:
            type = 1  #public
            dic = {
                'type':type,
                'proj':proj,
                'createuser': createuser if createuser else 8,
                'createdtime':str(row['CreationTime']),
            }
        # else:
        #     if row['UserType'] == 1:
        #         type = 3  #investor
        #         investor = datamanager.getNewUserId(row['InvestorId'])
        #         traderid = datamanager.getTraderId(row['InvestorId'],row['ProjectId'])
        #         dic = {
        #             'type': type,
        #             'proj': proj,
        #             'investor':investor,
        #             'trader':traderid,
        #             'createuser': createuser if createuser else 8,
        #             'createdtime': str(row['CreationTime']),
        #         }
        #     elif row['UserType'] == 2 :
        #         type = 2   #supportor
        #         dic = {
        #             'type': type,
        #             'proj': proj,
        #             'createuser': createuser if createuser else 8,
        #             'createdtime': str(row['CreationTime']),
        #         }
        #     elif row['UserType'] == 3 :
        #         pass  #交易师的不管
        #     else:
        #         pass #error
        if type in (1,2,3):
            try:
                response = requests.post(baseurl + 'dataroom/add/', data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] not in [1000]:
                    print '新增失败' + str(response)
                    print row['Id']
                else:
                    f = open('dataroom-old_new_id', 'a')
                    f.writelines(json.dumps({'old': row['Id'], 'new': response['result']['id'],'UserType':row['UserType'],'isPublic':row['IsPublic']}))
                    f.writelines('\n')
                    f.close()

            except Exception as err:
                print 'shibai'
                print  err
                print row['Id']
        else:
            pass
    print times

class DataManager():
    def __init__(self):
        self.allMySqlUser = self.getAllMySqlUser()
        self.allUser = self.getAllUser()

        self.allProj = self.getAllProject()
        self.allMySqlProj = self.getAllMySqlProject()

        self.allDataroom = self.getAllDataroom()
        self.allSupportDataroom = self.getAllSupportDataroom()
        self.allInvestorDataroom = self.getAllInvestorDataroom()
        self.allTraderDataroom = self.getAllTraderDataroom()


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



    def getAllDataroom(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.ProjectDataRoom WHERE IsDeleted = 0 AND IsPublic = 1"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getAllInvestorDataroom(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.ProjectDataRoom WHERE IsDeleted = 0 AND IsPublic = 0 AND UserType = 1"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getAllSupportDataroom(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.ProjectDataRoom WHERE IsDeleted = 0 AND IsPublic = 0 AND UserType = 2"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getAllTraderDataroom(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.ProjectDataRoom WHERE IsDeleted = 0 AND IsPublic = 0 AND UserType = 3"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getTraderId(self,investorId,projId):
        for area in self.allTraderDataroom:
            if area['InvestorId'] == investorId and area['ProjectId'] == projId:
                res = area['UserId']
                res = self.getNewUserId(res)
                return res


if __name__=="__main__":
    main()



# createtime = statudata.pop('createdtime').encode('utf-8')[0:19]
                        # if createtime not in ['None',None,u'None','none']:
                            # statudata['createdtime'] = datetime.datetime.strptime(createtime, "%Y-%m-%d %H:%M:%S")