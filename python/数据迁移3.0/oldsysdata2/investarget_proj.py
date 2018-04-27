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
    sql = "SELECT InvestargetDb_v2.dbo.Project.* , InvestargetDb_v2.dbo.ProjectFormat.* FROM InvestargetDb_v2.dbo.Project INNER JOIN InvestargetDb_v2.dbo.ProjectFormat ON InvestargetDb_v2.dbo.Project.ProjectFormatId = InvestargetDb_v2.dbo.ProjectFormat.Id WHERE InvestargetDb_v2.dbo.Project.IsDeleted =0 and Project.Code = 'P201701100106'"
    conn.execute_query(sql)
    for row in conn:
        times = times + 1
        supportuserid =  datamanager.getNewUserId(row['UserId'])
        if supportuserid is None:
            supportuserid = 8
        try:
            attachments = datamanager.getProjAttachments(row['Id'])
            linkkey = None
            if row['IsMarketPlace']:
                if len(attachments) == 1:
                    linkkey = attachments[0]['key']
            dic = {
                    'projtitleC':row['TitleC'] if row['TitleC'] else '暂无',
                    'projtitleE':row['TitleE']if row['TitleE'] else 'nothing',
                    'projstatus':row['StatusId'] if row['StatusId'] else 1,
                    'c_descriptionC':row['C_DescriptionC']if row['C_DescriptionC'] else '暂无',
                    'c_descriptionE': row['C_DescriptionE']if row['C_DescriptionE'] else 'nothing',
                    'p_introducteC': row['B_introducteC']if row['B_introducteC'] else '暂无',
                    'p_introducteE': row['B_introducteE']if row['B_introducteE'] else 'nothing',
                    'isoverseasproject': True,
                    'ismarketplace':row['IsMarketPlace']if row['IsMarketPlace'] else False,
                    'supportUser': supportuserid,
                    'isHidden': row['Ishidden']if row['Ishidden'] else False,
                    'financeAmount': row['FinancedAmount']if row['FinancedAmount'] else 0,
                    'financeAmount_USD': row['FinancedAmount_USD']if row['FinancedAmount_USD'] else 0,
                    'companyValuation': row['CompanyValuation']if row['CompanyValuation'] else 0,
                    'companyValuation_USD': row['CompanyValuation_USD']if row['CompanyValuation_USD'] else 0,
                    'companyYear': row['CompanyYear']if row['CompanyYear'] else 0,
                    'financeIsPublic': row['FinanceIsPublic'] if row['FinanceIsPublic'] else True,
                    'code': row['Code'],
                    'currency': row['currencyId']if row['currencyId'] else 1,
                    'contactPerson': row['contactPerson']if row['contactPerson'] else '暂无',
                    'phoneNumber': row['PhoneNumber']if row['PhoneNumber'] else '暂无',
                    'email': row['eMail'],
                    'country':datamanager.getNewCountryId(row['CountryId']),
                    'targetMarketC': row['TargetMarketC']if row['TargetMarketC'] else '暂无',
                    'targetMarketE': row['TargetMarketE']if row['TargetMarketE'] else 'nothing',
                    'character': row['CharacterId'],
                    'productTechnologyC': row['ProductTechnologyC']if row['ProductTechnologyC'] else '暂无',
                    'productTechnologyE': row['ProductTechnologyE']if row['ProductTechnologyE'] else 'nothing',
                    'businessModelC': row['BusinessModelC']if row['BusinessModelC'] else '暂无',
                    'businessModelE': row['BusinessModelE']if row['BusinessModelE'] else 'nothing',
                    'brandChannelC': row['BrandSalesChannelC']if row['BrandSalesChannelC'] else '暂无',
                    'brandChannelE': row['BrandSalesChannelE']if row['BrandSalesChannelE'] else 'nothing',
                    'managementTeamC': row['ManagementC']if row['ManagementC'] else '暂无',
                    'managementTeamE': row['ManagementE']if row['ManagementE'] else 'nothing',
                    'BusinesspartnersC': row['PartnersC']if row['PartnersC'] else '暂无',
                    'BusinesspartnersE': row['PartnersE']if row['PartnersE'] else 'nothing',
                    'useOfProceedC': row['UseofProceedC']if row['UseofProceedC'] else '暂无',
                    'useOfProceedE': row['UseofProceedE']if row['UseofProceedE'] else 'nothing',
                    'financingHistoryC': row['FinancingRecordC']if row['FinancingRecordC'] else '暂无',
                    'financingHistoryE': row['FinancingRecordE']if row['FinancingRecordE'] else 'nothing',
                    'operationalDataC': row['OperatingFiguresC']if row['OperatingFiguresC'] else '暂无',
                    'operationalDataE': row['OperatingFiguresE']if row['OperatingFiguresE'] else 'nothing',
                    'publishDate': str(row['PublishedDate']),
                    'isSendEmail': row['IsSendEmail']if row['IsSendEmail'] else False,
                    'createdtime': str(row['CreationTime']),
                    'createuser':datamanager.getNewUserId(row['CreatorUserId']),
                    'datasource': 1,
                    'linkpdfkey':linkkey,
                    'industries':datamanager.getProjIndustries(row['Id']),
                    'tags':datamanager.getProjTags(row['Id']),
                    'transactionType':datamanager.getProjTransactionTypes(row['Id']),
                    'projAttachment': None if row['IsMarketPlace'] else attachments,
                    'finance':datamanager.getProjFinances(row['Id']),
                }
            response = requests.post(baseurl + 'proj/' , data=json.dumps(dic), headers=headers).content
            response = json.loads(response)
            if response['code'] not in [1000,2004]:
                print '新增失败' + str(response)
                print row['Id']
        except Exception as err:
            print 'shibai'
            print  err
            print row['Id']
    print times
    conn.close()


class DataManager():
    def __init__(self):
        self.allMySqlUser = self.getAllMySqlUser()
        self.allUser = self.getAllUser()
        self.allIndustry = self.getAllIndustry()
        self.allMySqlIndustry = self.getAllMySqplIndustry()
        self.allCountry = self.getAllCountry()
        self.allMySqlCountry = self.getAllMySqplCountry()
        self.allTag = self.getAllTag()
        self.allMySqlTag = self.getAllMySqplTag()
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

    def getAllCountry(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.Country WHERE IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res
    def getAllMySqplCountry(self):
        res = requests.get(baseurl + 'source/country')
        return json.loads(res.content).get('result',None)


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


    def getNewCountryId(self,sqlserverid):
        if sqlserverid:
            mysqlid = None
            realname = None
            for area in self.allCountry:
                if area['Id'] == sqlserverid:
                    realname = area['CountryC']
            if realname is not None:
                for one in self.allMySqlCountry:
                    if one['countryC'] == realname:
                        mysqlid = one['id']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
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

    def getProjTags(self,projSqlServerId):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT TagId FROM InvestargetDb_v2.dbo.Project_Tag WHERE IsDeleted = 0 AND ProjectId = %s"%projSqlServerId
        conn.execute_query(sql)
        res = []
        for area in conn:
            newId = self.getNewTagId(area['TagId'])
            if newId:
                res.append(newId)
        conn.close()
        return res

    def getProjIndustries(self,projSqlServerId):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.Project_Industry WHERE IsDeleted = 0 AND ProjectId = %s"%projSqlServerId
        conn.execute_query(sql)
        res = []
        for area in conn:
            newId = self.getNewIndustryId(area['IndustryId'])
            if newId:
                indus = {'industry':newId,'key':area['Key'],'bucket':area['Bucket'],
                         'createdtime': str(area['CreationTime'])
                         }
                res.append(indus)
        conn.close()
        return res

    def getProjTransactionTypes(self,projSqlServerId):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT TypeId FROM InvestargetDb_v2.dbo.Project_TransactionType WHERE IsDeleted = 0 AND ProjectId = %s" % projSqlServerId
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area['TypeId'])
        conn.close()
        return res
    def getProjAttachments(self,projSqlServerId):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.ProjectAttachment WHERE IsDeleted = 0 AND ProjectId = %s" % projSqlServerId
        conn.execute_query(sql)
        res = []
        for area in conn:
            attachment = {'createuser': self.getNewUserId(area['CreatorUserId']), 'key': area['Key'], 'bucket': area['Bucket'], 'filename': area['FileName'], 'filetype': area['FileType'],
                          'createdtime': str(area['CreationTime'])
                          }
            res.append(attachment)
        conn.close()
        return res
    def getProjFinances(self,projSqlServerId):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.ProjectFinance WHERE IsDeleted = 0 AND ProjectId = %s" % projSqlServerId
        conn.execute_query(sql)
        res = []
        for area in conn:
            finance = {'createuser': self.getNewUserId(area['CreatorUserId']), 'revenue': area['Revenue'],
                          'netIncome': area['NetIncome'], 'revenue_USD': area['Revenue_USD'], 'netIncome_USD': area['NetIncome_USD'],
                       'EBITDA': area['EBITDA'], 'grossProfit': area['GrossProfit'], 'totalAsset': area['TotalAsset'],
                       'stockholdersEquity': area['Shareholdersequity'], 'operationalCashFlow': area['OperationalCashFlow'], 'grossMerchandiseValue': area['GrossMerchandiseValue'],'fYear':area['FYear'],

                          'createdtime': str(area['CreationTime'])
                       }
            res.append(finance)
        conn.close()
        return res


if __name__=="__main__":
    main()
