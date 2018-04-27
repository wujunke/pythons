#coding=utf-8
import json

import pymysql
import requests
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
        if investor is None:
            msg.append('未找到匹配投资人')
        if trader is None:
            msg.append('未找到匹配交易师')
        if proj is None:
            msg.append('未找到匹配项目')
        if createuser is None:
            createuser = 8
        if investor and trader and proj:
            try:
                dic = {
                    'timelinedata':{
                        'investor': investor,
                        'trader': trader,
                        'proj': proj,
                        'isClose': False if row['IsClose'] else False,
                        'closeDate': str(row['CloseDate']) if row['CloseDate'] else None,
                        'contractedServiceTime': str(row['ContractedServiceTime']) if row[
                            'ContractedServiceTime'] else None,
                        'turnoverTime': str(row['TurnoverTime']) if row['TurnoverTime'] else None,
                        'createdtime': str(row['CreationTime']) if row['CreationTime'] else None,
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


class DataManager():
    def __init__(self):
        self.allMySqlUser = self.getAllMySqlUser()
        self.allUser = self.getAllUser()

        self.allProj = self.getAllProject()
        self.allMySqlProj = self.getAllMySqlProject()

    #     self.allIndustry = self.getAllIndustry()
    #     self.allMySqlIndustry = self.getAllMySqplIndustry()
    #     self.allCountry = self.getAllCountry()
    #     self.allMySqlCountry = self.getAllMySqplCountry()
    #     self.allTag = self.getAllTag()
    #     self.allMySqlTag = self.getAllMySqplTag()
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


                # def getAllCountry(self):
    #     conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    #     # SELECT 短链接查询操作（一次查询将所有数据取出）
    #     sql = "SELECT * FROM InvestargetDb_v2.dbo.Country WHERE IsDeleted = 0"
    #     conn.execute_query(sql)
    #     res = []
    #     for area in conn:
    #         res.append(area)
    #     conn.close()
    #     return res
    # def getAllMySqplCountry(self):
    #     res = requests.get(baseurl + 'source/country')
    #     return json.loads(res.content).get('result',None)
    #
    #
    # def getAllIndustry(self):
    #     conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    #     # SELECT 短链接查询操作（一次查询将所有数据取出）
    #     sql = "SELECT * FROM InvestargetDb_v2.dbo.Industry WHERE IsDeleted = 0"
    #     conn.execute_query(sql)
    #     res = []
    #     for area in conn:
    #         res.append(area)
    #     conn.close()
    #     return res
    # def getAllMySqplIndustry(self):
    #     res = requests.get(baseurl + 'source/industry')
    #     return json.loads(res.content).get('result',None)
    #
    #
    # def getNewCountryId(self,sqlserverid):
    #     if sqlserverid:
    #         mysqlid = None
    #         realname = None
    #         for area in self.allCountry:
    #             if area['Id'] == sqlserverid:
    #                 realname = area['CountryC']
    #         if realname is not None:
    #             for one in self.allMySqlCountry:
    #                 if one['countryC'] == realname:
    #                     mysqlid = one['id']
    #         if mysqlid is not None:
    #             return mysqlid
    #         else:
    #             return None
    #     else:
    #         return None
    # def getNewIndustryId(self, sqlserverid):
    #     if sqlserverid:
    #         mysqlid = None
    #         realname = None
    #         for area in self.allIndustry:
    #             if area['Id'] == sqlserverid:
    #                 realname = area['IndustryC']
    #         if realname is not None:
    #             for one in self.allMySqlIndustry:
    #                 if one['industryC'] == realname:
    #                     mysqlid = one['id']
    #         if mysqlid is not None:
    #             return mysqlid
    #         else:
    #             return None
    #     else:
    #         return None
    #
    # def getAllTag(self):
    #     conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    #     # SELECT 短链接查询操作（一次查询将所有数据取出）
    #     sql = "SELECT * FROM InvestargetDb_v2.dbo.Tag WHERE IsDeleted = 0"
    #     conn.execute_query(sql)
    #     res = []
    #     for area in conn:
    #         res.append(area)
    #     conn.close()
    #     return res
    # def getAllMySqplTag(self):
    #     res = requests.get(baseurl + 'source/tag',headers={'source': '1',})
    #     return json.loads(res.content).get('result',None)
    #
    # def getNewTagId(self,sqlserverid):
    #     if sqlserverid:
    #         mysqlid = None
    #         realname = None
    #         for area in self.allTag:
    #             if area['Id'] == sqlserverid:
    #                 realname = area['TagNameC']
    #         if realname is not None:
    #             for one in self.allMySqlTag:
    #                 if one['nameC'] == realname:
    #                     mysqlid = one['id']
    #         if mysqlid is not None:
    #             return mysqlid
    #         else:
    #             return None
    #     else:
    #         return None
    #
    # def getProjTags(self,projSqlServerId):
    #     conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    #     # SELECT 短链接查询操作（一次查询将所有数据取出）
    #     sql = "SELECT TagId FROM InvestargetDb_v2.dbo.Project_Tag WHERE IsDeleted = 0 AND ProjectId = %s"%projSqlServerId
    #     conn.execute_query(sql)
    #     res = []
    #     for area in conn:
    #         newId = self.getNewTagId(area['TagId'])
    #         if newId:
    #             res.append(newId)
    #     conn.close()
    #     return res
    #
    # def getProjIndustries(self,projSqlServerId):
    #     conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    #     # SELECT 短链接查询操作（一次查询将所有数据取出）
    #     sql = "SELECT * FROM InvestargetDb_v2.dbo.Project_Industry WHERE IsDeleted = 0 AND ProjectId = %s"%projSqlServerId
    #     conn.execute_query(sql)
    #     res = []
    #     for area in conn:
    #         newId = self.getNewIndustryId(area['IndustryId'])
    #         if newId:
    #             indus = {'industry':newId,'key':area['Key'],'bucket':area['Bucket'],
    #                      'createdtime': str(area['CreationTime'])
    #                      }
    #             res.append(indus)
    #     conn.close()
    #     return res
    #
    # def getProjTransactionTypes(self,projSqlServerId):
    #     conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    #     # SELECT 短链接查询操作（一次查询将所有数据取出）
    #     sql = "SELECT TypeId FROM InvestargetDb_v2.dbo.Project_TransactionType WHERE IsDeleted = 0 AND ProjectId = %s" % projSqlServerId
    #     conn.execute_query(sql)
    #     res = []
    #     for area in conn:
    #         res.append(area['TypeId'])
    #     conn.close()
    #     return res
    # def getProjAttachments(self,projSqlServerId):
    #     conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    #     # SELECT 短链接查询操作（一次查询将所有数据取出）
    #     sql = "SELECT * FROM InvestargetDb_v2.dbo.ProjectAttachment WHERE IsDeleted = 0 AND ProjectId = %s" % projSqlServerId
    #     conn.execute_query(sql)
    #     res = []
    #     for area in conn:
    #         attachment = {'createuser': self.getNewUserId(area['CreatorUserId']), 'key': area['Key'], 'bucket': area['Bucket'], 'filename': area['FileName'], 'filetype': area['FileType'],
    #                       'createdtime': str(area['CreationTime'])
    #                       }
    #         res.append(attachment)
    #     conn.close()
    #     return res
    # def getProjFinances(self,projSqlServerId):
    #     conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    #     # SELECT 短链接查询操作（一次查询将所有数据取出）
    #     sql = "SELECT * FROM InvestargetDb_v2.dbo.ProjectFinance WHERE IsDeleted = 0 AND ProjectId = %s" % projSqlServerId
    #     conn.execute_query(sql)
    #     res = []
    #     for area in conn:
    #         finance = {'createuser': self.getNewUserId(area['CreatorUserId']), 'revenue': area['Revenue'],
    #                       'netIncome': area['NetIncome'], 'revenue_USD': area['Revenue_USD'], 'netIncome_USD': area['NetIncome_USD'],
    #                    'EBITDA': area['EBITDA'], 'grossProfit': area['GrossProfit'], 'totalAsset': area['TotalAsset'],
    #                    'stockholdersEquity': area['Shareholdersequity'], 'operationalCashFlow': area['OperationalCashFlow'], 'grossMerchandiseValue': area['GrossMerchandiseValue'],'fYear':area['FYear'],
    #
    #                       'createdtime': str(area['CreationTime'])
    #                    }
    #         res.append(finance)
    #     conn.close()
    #     return res


if __name__=="__main__":
    main()



# createtime = statudata.pop('createdtime').encode('utf-8')[0:19]
                        # if createtime not in ['None',None,u'None','none']:
                            # statudata['createdtime'] = datetime.datetime.strptime(createtime, "%Y-%m-%d %H:%M:%S")