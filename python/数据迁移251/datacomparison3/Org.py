import json

import requests
from config import baseurl, headers
from Orgtype import getOrgTypeId


def getOrgId(orgname):

    orglist = json.loads(requests.get(baseurl+'org/?search=%s'%orgname,headers=headers).content).get('result',{}).get('data',[])
    if len(orglist) > 0:
        orgid = orglist[0]['id']
        # orgtypeid = getOrgTypeId(row['orgytype'])
        # if orgtypeid:
        #     data = {
        #         "orgtype": orgtypeid
        #     }
        #     response = requests.put(baseurl + 'org/%s/' % orgid, data=json.dumps(data), headers=headers).content
        #     response = json.loads(response)
        # else:
        #     pass
    else:
        orgid = None
    return orgid