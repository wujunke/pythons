# -*- coding: utf-8 -*-
import random
import traceback
import  xdrlib ,sys

import time
from pypinyin import slug as hanzizhuanpinpin
import requests
import xlrd
import json

reload(sys)
sys.setdefaultencoding('utf-8')



def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print str(e)
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的索引  ，by_index：表的索引
def excel_table_byindex(file,colnameindex=0,by_index=0):
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

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file,colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数
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
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
# baseurl = 'http://192.168.1.201:8000/'
baseurl = 'https://api.investarget.net/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }

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
def getAllTag():

    res = json.loads(requests.get(baseurl+'source/tag',headers=headers).content)
    re = res.get('result')
    return re

alltags = getAllTag()

def getTagId(tagname):
    tagid = None
    for tag in alltags:
        tagnameC = tag.get('nameC')
        if tagnameC == tagname:
            tagid = tag.get('id')
    return tagid

def getAllCountry():

    res = json.loads(requests.get(baseurl+'source/orgarea',headers=headers).content)
    re = res.get('result')
    return re

allcountry = getAllCountry()
def getCountryId(countryname):
    reid = None
    for country in allcountry:
        if country.get('nameC') == countryname:
            reid = country.get('id')
    return reid
def getAllTitle():

    res = json.loads(requests.get(baseurl+'source/title',headers=headers).content)
    re = res.get('result')
    return re

alltitle = getAllTitle()
def getTitleId(titlename):
    reid = None
    for title in alltitle:
        if title.get('nameC') == titlename:
            reid = title.get('id')
    return reid

traderlist = {
    '王菲':100000004,
    '叶璐蓓':100007593,
    '赵鹏云':100005504,
    '尹乐鸣':100010424,
    'Sara':100007593,

}


def main():
    times = 0
    tables = excel_table_byindex('/Users/investarget/Desktop/python/数据迁移3.0/excel/exceldata/18011502.xlsx',)
    for row in tables:
        times = times + 1
        if row['phone'] in [None,'',u'']:
            print '手机号缺失，暂不增加--%s'%row['name']
            continue
        if int(row['phone']) not in [18621266376]:
            continue
        try:
            time.sleep(1)
            dic = {
                'usernameC':row['name'],
                'mobile':int(row['phone']),
                'title':getTitleId(row['position']),
                'wechat':row['weixin'],
                'orgarea':getCountryId(row['city'].split('，')[0]),
                'userstatus':2,
                'groups':[1],
            }
            remarkdic = {
                'user':None,
                'remark':'联络情况备注：%s;'
                         '投资轮次：%s；'
                         '投资规模备注：%s；'
                         '投资关注领域：%s；' % (row['remark'] if row['remark'] else '暂无' ,row['round'] if row['round'] else '暂无', row['fundsize']if row['fundsize'] else '暂无', row['industry']if row['industry'] else '暂无'),
            }
            orglist = json.loads(requests.get(baseurl+'org/?orgname=%s'%row['company'],headers=headers).content).get('result',{}).get('data',[])
            if len(orglist) > 0:
                orgid = orglist[0]['id']
            else:
                print '未匹配到相应机构--%s' % row['name']
                orgid = None
            email = hanzizhuanpinpin(row['name'], separator='').split(' ')[0]
            dic['email'] = email + '@investarget11521.com'
            dic['org'] = orgid
            tags = [42]
            dic['tags'] = tags
            response = requests.post(baseurl + 'user/' , data=json.dumps(dic), headers=headers).content
            response = json.loads(response)
            if response['code'] != 1000:
                if response['code'] == 2004:
                    userlist = json.loads(
                        requests.get(baseurl + 'user/?search=%s' % int(row['phone']), headers=headers).content).get('result',{}).get('data', [])
                    if len(userlist) > 0:
                        userid = userlist[0]['id']
                    else:
                        print '未匹配到相应用户--%s' % int(row['phone'])
                        userid = None
                    if userid:
                        updatedic = {
                            'userlist':[userid],
                            'userdata':{
                                'title':dic['title'],
                                'wechat':dic['wechat'],
                                'tags':dic['tags'],
                                'org':dic['org'],
                                'orgarea':dic['orgarea'],
                                'userstatus':2,
                            }
                        }
                        response = requests.put(baseurl + 'user/', data=json.dumps(updatedic), headers=headers).content
                        response = json.loads(response)
                        if response['code'] != 1000:
                            print '更新用户失败--%s' % row['name'] + str(response)
                else:
                    print '新增用户失败--%s' % row['name'] + str(response)
                    userid = None
            else:
                userid = response['result']['id']
            if userid:
                remarkdic['user'] = userid
                response = requests.post(baseurl + 'user/remark/', data=json.dumps(remarkdic), headers=headers).content
                response = json.loads(response)
                if response['code'] != 1000:
                    print '新增用户备注失败--%s' % row['name'] + str(response)
        except Exception:
            print '失败--%s'%row['name']
            print traceback.format_exc()



if __name__=="__main__":
    main()