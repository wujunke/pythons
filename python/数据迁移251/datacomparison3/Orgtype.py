import json

import requests
from config import baseurl, headers



def getAllOrgType():
    res = json.loads(requests.get(baseurl+'source/orgtype',headers=headers).content)
    re = res.get('result')
    return re

allOrgType = getAllOrgType()
def getOrgTypeId(orgtypename):
    orgtypeid = None
    for orgType in allOrgType:
        tagnameC = orgType.get('nameC')
        if tagnameC == orgtypename:
            orgtypeid = orgType.get('id')
    return orgtypeid