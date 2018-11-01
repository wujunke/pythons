# -*- coding: utf-8 -*-
import traceback
import  xdrlib ,sys

import time
from pypinyin import slug as hanzizhuanpinpin
import requests
import xlrd
import json

reload(sys)
sys.setdefaultencoding('utf-8')


token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
baseurl = 'http://192.168.1.201:8000/'
# token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
# baseurl = 'https://api.investarget.com/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print str(e)


#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的索引  ，by_index：表的索引
def excel_table_byindex(file,colnameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list



orgdic = {}





def getOrgByFullName(orgFullName):
    orgid = orgdic.get(orgFullName)
    if orgid:
        return orgid
    orglist = json.loads(requests.get(baseurl + 'org/?orgfullname=%s' % orgFullName, headers=headers).content).get(
        'result', {}).get('data', [])
    if len(orglist) > 0:
        orgid = orglist[0]['id']
        orgdic[orgFullName] = orgid
        return orgid
    else:
        data = {
            'orgfullname': orgFullName,
            'orgnameC': orgFullName,
            'orgnameE': orgFullName,
            'tags': [57],
        }
        response = requests.post(baseurl + 'org/', data=json.dumps(data), headers=headers).content
        response = json.loads(response)
        if response['code'] != 1000:
            print '新增失败--%s' % orgFullName + str(response)
            return None
        else:
            orgid = response['result']['id']
            orgdic[orgFullName] = orgid
            return orgid


def addOrgTag(orgid, tags):
    data = {
        'tags': tags + [57]
    }
    response = requests.put(baseurl + 'org/%s/' % orgid, data=json.dumps(data), headers=headers).content
    response = json.loads(response)
    if response['code'] != 1000:
        print '新增机构标签失败--%s' % orgid + str(response)



def checkUserExist(account):
    time.sleep(1)
    url = baseurl + 'user/checkexists/?' + 'account=%s' % account
    response = requests.get(url, headers=headers).content
    response = json.loads(response)
    res = response['result']
    userorg = res['user']['org'] if res['user'] else None
    userorgid = userorg['id'] if userorg else None
    orgtags = userorg['tags'] if userorg else None
    return res['result'], userorgid, orgtags



def addUser(data):
    response = requests.post(baseurl + 'user/', data=json.dumps(data), headers=headers).content
    response = json.loads(response)
    if response[u'code'] != 1000:
        print('新增用户失败--%s' % data['usernameC'])


def getAvailableEmail(email1, email2, salt=0):
    if salt > 0:
        email = email1 + str(salt) + '@' + email2
    else:
        email = email1 + '@' + email2
    emailExist, aa, bb = checkUserExist(email)
    if emailExist:
        salt += 1
        time.sleep(1)
        return getAvailableEmail(email1, email2, salt)
    else:
        return email

allTitles = {}
titleUrl = baseurl + 'source/title'
response = requests.get(titleUrl, headers=headers).content
res = json.loads(response)['result']
for title in res:
    allTitles[title['nameC']] = title['id']




def getAvailableTitle(titleName):
    if titleName in [u'', None, '']:
        return None
    if '/' in titleName:
        titleName = titleName.split('/')[0]
    return allTitles.get(titleName)



tables = excel_table_byindex(u'/Users/investarget/pythons/python/数据迁移3.0/excel/exceldata/914-2.xlsx')
rowid = 1
for row in tables:
    print(rowid)
    rowid += 1
    if rowid >= 9:
        mobile = row[u'号码']
        if isinstance(mobile, (unicode, str)):
            mobile = str(mobile).replace(' ', '').replace('-', '')
        elif isinstance(mobile, float):
            mobile = int(mobile)
        mobile = str(mobile) if mobile else None
        if mobile not in ['', None] and mobile.isdigit():
            mobileExist, userorgid, tags = checkUserExist(mobile)
            if not mobileExist:
                orgFullName = row[u'所在机构'].strip()
                orgId = getOrgByFullName(orgFullName)
                # username = str(row[u'姓名']).replace(' ', '')
                username = row[u'姓名'].replace(u'\u3000', '').replace(u'\u202d', '').replace(u'\u0020', '')
                userdata = {
                    u'usernameC': username,
                    u'title': getAvailableTitle(row[u'职位']),
                    u'groups': [1],
                    u'org': orgId,
                    u'mobile': str(mobile),
                    u'email': getAvailableEmail(hanzizhuanpinpin(username, separator=''), u'investarget.com'),
                }
                addUser(userdata)
            else:
                if userorgid:
                    addOrgTag(userorgid, tags)
                else:
                    orgFullName = row[u'所在机构'].strip()
                    orgId = getOrgByFullName(orgFullName)
        else:
            orgFullName = row[u'所在机构'].strip()
            orgId = getOrgByFullName(orgFullName)







