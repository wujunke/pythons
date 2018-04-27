#coding=utf-8
import json
import requests
from pypinyin import slug as hanzizhuanpinpin
import _mssql


baseurl = 'http://192.168.1.201:8000/'
#海拓token
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
    times = 0
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016',)
    datamanager = DataManager()
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT * FROM InvestargetDb_v2.dbo.\"User\" WHERE IsDeleted = 0"

    conn.execute_query(sql)
    for row in conn:
        times = times + 1

        if row['UserType'] in [0,4]:
            print row['Id']
            print 'type == ' + str(row['UserType'])
        else:
            try:
                group = 4
                status = row['AuditStatus']
                if status == 2:
                    if row['UserType'] == 1:
                        group = 1
                    if row['UserType'] == 2:
                        group = 1
                    if row['UserType'] == 3:
                        group = 2
                else:
                    if row['UserType'] == 1:
                        group = 4
                    if row['UserType'] == 2:
                        group = 4
                    if row['UserType'] == 3:
                        group = 5
                dic = {
                    'usernameC':row['Name'],
                    'usernameE':row['Name_en'],
                    'usercode':row['UserName'],
                    'photoBucket':'image',
                    'photoKey': row['PhotoKey'] if row['PhotoKey'] not in [None,'',u''] else None,
                    'cardBucket': 'image',
                    'cardKey': row['CardKey'],
                    'wechat': row['WeChat'],
                    'country': datamanager.getNewCountryId(row['CountryId']),
                    'department': row['DepartMent'],
                    'orgarea': datamanager.getNewOrgAreaId(row['OrgAreaId']),
                    'userstatus': row['AuditStatus'] if row['AuditStatus'] != 0 else 1,
                    'org': datamanager.getNewOrgId(row['OrganizationId']),
                    'mobileAreaCode': row['MobileAreaCode'],
                    'mobile': row['Mobile'],
                    'description': row['Company'] if row['Company'] else 'description',
                    'email': row['EmailAddress'],
                    'title': row['TitleId'],
                    'gender': row['Gender'],
                    'registersource': 5,
                    'groups': [group],
                    'datasource': 1,
                }
                response = requests.post(baseurl + 'user/' , data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] not in [1000,2004]:
                    print '新增失败' + str(response)
                    print dic['usernameC']
                    print row['Id']
            except Exception as err:
                print 'shibai'
                print  err
                print row['Id']
    print times
    conn.close()


class DataManager():
    def __init__(self):
        self.allArea = self.getAllOrgArea()
        self.allMySqlArea = self.getAllMySqlArea()
        self.allOrgType = self.getAllOrgType()
        self.allMySqlOrgType = self.getAllMySqplType()
        self.allIndustry = self.getAllIndustry()
        self.allMySqlIndustry = self.getAllMySqplIndustry()
        self.allCountry = self.getAllCountry()
        self.allMySqlCountry = self.getAllMySqplCountry()

        self.allOrg = self.getAllOrg()
        self.allMySqlOrg = self.getAllMySqlOrg()

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
        res = requests.get(baseurl + 'source/orgarea',headers={'source':'1',})
        return json.loads(res.content).get('result',None)

    def getAllOrg(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res
    def getAllMySqlOrg(self):
        res = requests.get(baseurl + 'org/?page_size=100000',headers={'source':'1',})
        result = json.loads(res.content).get('result',{})
        return result.get('data',None)

    def getAllOrgType(self):
        res = {'1':'基金',
               '2': '律所',
               '3': '投行',
               '4': '会计师事务所',
               '5': '咨询',
               '6': '证券',
               '7': '银行',
               '8': '信托',
               '9': '租赁',
               '10': '保险',
               '11': '期货',
               '12': '上市公司',
               '13': '新三板上市公司',
               '14': '非上市公司',
               '15': '政府引导性基金',
               '16': '金融机构直投基金',
               '17': '上市公司产业基金',
               '18': '其它',
               '19': '个人',
               }
        return res
    def getAllMySqplType(self):
        res = requests.get(baseurl + 'source/orgtype')
        return json.loads(res.content).get('result',None)
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

if __name__=="__main__":
    main()
