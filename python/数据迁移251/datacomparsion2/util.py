import json

import _mssql
import requests
from config import baseurl, headers



def getOrgId(orgname):

    orglist = json.loads(requests.get(baseurl+'/api/services/InvestargetApi/organization/GetOrgs?input.name=%s'%orgname,headers=headers).content).get('result',{}).get('data',[])
    if len(orglist) > 0:
        orgid = orglist[0]['id']
    else:
        orgid = None
    return orgid


def checkMobileExist(mobile):
    if mobile:
        if isinstance(mobile,float):
            mobile = int(mobile)
            mobile = str(mobile)
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        sql = "SELECT * FROM InvestargetDb_v2.dbo.\"User\" WHERE IsDeleted = 0 AND Mobile = '%s'" % mobile
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res
    return []


def checkEmailExist(email):
    if email:
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        sql = "SELECT * FROM InvestargetDb_v2.dbo.\"User\" WHERE IsDeleted = 0 AND EmailAddress = '%s'"%email
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res
    return []


