#coding=utf-8
import json
import traceback

import datetime
import requests
from pypinyin import slug as hanzizhuanpinpin
import _mssql

token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
baseurl = 'http://39.107.14.53:8080/'
headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }


def main():
    addOrg()



def addOrg():
    times = 0
    print times
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    datamanager = DataManager()
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND Name IS NOT NULL"
    # sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND id = 1155"
    conn.execute_query(sql)

    for row in conn:
        times = times + 1
        try:
            dic = {
                'orgnameC': row['Name'],
                'orgnameE': row['NameEn'],
                'description': row['Description'],
                'decisionCycle': row['DecisionCycle'],
                'decisionMakingProcess': row['DecisionMakingProcess'],
                'investoverseasproject': row['OverSeasProject'] if row['OverSeasProject'] else False,
                'currency': row['Currency'] if row['Currency'] else 1,
                'orgcode': row['StockCode'],
                'orgtype': datamanager.getNewTypeId(row['OrgType']),
                'transactionAmountF': row['TransactionAmountF'],
                'transactionAmountT': row['TransactionAmountT'],
                'weChat': row['WeChat'],
                'fundSize': row['FundSize'],
                'address': row['Address'],
                'webSite': row['WebSite'],
                'typicalCase': row['TypicalCase'],
                'transactionAmountF_USD': row['TransactionAmountF_USD'],
                'transactionAmountT_USD': row['TransactionAmountT_USD'],
                'partnerOrInvestmentCommiterMember': row['PartnerOrInvestmentCommitteeMember'],
                'mobile': row['Phone'],
                'companyEmail': row['CompanyEmail'],
                'orgstatus': 2,
                'orgtransactionphase': datamanager.getOrgTransactions(row['Id']),
                'industry': datamanager.getNewIndustryId(row['IndustryId']),
                'datasource': 1,
                'createdtime': str(row['CreationTime']) if row['CreationTime'] else str(datetime.datetime.now()),
                'lastmodifytime':str(row['LastModificationTime']) if row['LastModificationTime'] else str(datetime.datetime.now()),
            }
            response = requests.post(baseurl + 'org/', data=json.dumps(dic), headers=headers).content
            response = json.loads(response)
            if response['code'] != 1000:
                print '新增失败' + str(response)
                print dic['orgnameC']
                print str(times)
            else:
                f = open('org-old_new_id', 'a')
                f.writelines(json.dumps({'old': row['Id'], 'new': response['result']['id']}))
                f.writelines('\n')
                f.close()
        except Exception as err:
            print 'shibai'
            print  err
            pass
    conn.close()


class DataManager():
    def __init__(self):
        self.allArea = self.getAllOrgArea()
        self.allMySqlArea = self.getAllMySqlArea()
        self.allOrgType = self.getAllOrgType()
        self.allMySqlOrgType = self.getAllMySqplType()
        self.allIndustry = self.getAllIndustry()
        self.allMySqlOrg = self.getAllMySqlOrg()
        self.allMySqlIndustry = self.getAllMySqplIndustry()


        self.allOrgTransaction = self.getAllOrgTransaction()

    def getAllOrgArea(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.OrgArea WHERE IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res
    def getAllMySqlArea(self):
        res = requests.get(baseurl + 'source/orgarea')
        return json.loads(res.content).get('result',None)

    def getAllMySqlOrg(self):
        res = requests.get(baseurl + 'org/?page_size=100000', headers={'source': '1', })
        result = json.loads(res.content).get('result', {})
        return result.get('data', None)

    def getAllOrgTransaction(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization_TransactionPhase WHERE IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getOrgTransactions(self,orgId):
        orgtransactionphase = []
        if orgId:
            for transa in self.allOrgTransaction:
                if transa['OrganizationId'] == orgId:
                    orgtransactionphase.append(transa['TransactionPhaseId'])
        return orgtransactionphase

    def getAllOrgType(self):
        res = {'1': u'基金',
               '2': u'律所',
               '3': u'投行',
               '4': u'会计师事务所',
               '5': u'咨询',
               '6': u'证券',
               '7': u'银行',
               '8': u'信托',
               '9': u'租赁',
               '10': u'保险',
               '11': u'期货',
               '12': u'上市公司',
               '13': u'新三板上市公司',
               '14': u'非上市公司',
               '15': u'政府引导性基金',
               '16': u'金融机构直投基金',
               '17': u'上市公司产业基金',
               '18': u'其它',
               '19': u'个人',
               }
        return res
    def getAllMySqplType(self):
        res = requests.get(baseurl + 'source/orgtype')
        return json.loads(res.content).get('result',None)

    def getNewOrgId(self, realname):
        if realname:
            realname = realname.encode('utf-8').replace('\n','').decode('utf-8')
            mysqlid = None
            for one in self.allMySqlOrg:
                if one['orgnameC'] == realname:
                    mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None

    def getAllIndustry(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.Industry WHERE IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res
    def getAllMySqplIndustry(self):
        res = requests.get(baseurl + 'source/industry')
        return json.loads(res.content).get('result',None)

    def getNewOrgAreaId(self,sqlserverid):
        if sqlserverid:
            mysqlid = None
            realname = None
            for area in self.allArea:
                if area['Id'] == sqlserverid:
                    realname = area['AreaName']
            if realname is not None:
                for one in self.allMySqlArea:
                    if one['nameC'] == realname:
                        mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None
    def getNewTypeId(self, sqlserverid):
        if sqlserverid:
            mysqlid = None
            realname = None
            for key,value in self.allOrgType.items():
                if key == sqlserverid:
                    realname = value
            if realname is not None:
                for one in self.allMySqlOrgType:
                    if one['nameC'] == realname:
                        mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return 18
        else:
            return None
    def getNewIndustryId(self, sqlserverid):
        if sqlserverid:
            mysqlid = None
            realname = None
            for area in self.allIndustry:
                if area['Id'] == sqlserverid:
                    realname = area['IndustryC']
            if realname is not None:
                for one in self.allMySqlIndustry:
                    if one['industryC'] == realname:
                        mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None

if __name__=="__main__":
    main()
