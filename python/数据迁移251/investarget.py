# -*- coding: utf-8 -*-
import traceback
import  xdrlib ,sys
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
baseurl = 'http://192.168.1.201:8000/'

headers = {
        'token':'9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00',
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



def main():
    times = 0
    tables = excel_table_byindex('/Users/investarget/Desktop/消费升级 投资人.xlsx')
    for row in tables:
        times = times + 1
        if row['phone'] in [None,'',u'']:
            print '手机号缺失，暂不增加--%s'%row['name']
            continue
        try:
            a = ''
            dic = {
                'usernameC':row['name'],
                'mobile':int(row['phone']),
                'email':None,
                'title':getTitleId(row['position']),
                'wechat':row['weixin'],
                'org':row['company'],
                'tags':row['tag'],
                'orgarea':getCountryId(row['city'].split('、')[0]),
                # 'remark':row['remark'],
                'groups':[4],
            }

            orglist = json.loads(requests.get(baseurl+'org/?search=%s'%dic['org'],headers=headers).content).get('result',{}).get('data',[])
            if len(orglist) > 0:
                orgid = orglist[0]['id']
                # orgtypeid = getOrgTypeId(row['orgytype'])
                # if orgtypeid:
                #     data = {
                #         "orgtype": orgtypeid
                #     }
                #     response = requests.put(baseurl+'org/%s/' % orgid, data=json.dumps(data),headers=headers).content
                #     response = json.loads(response)
                # else:
                #     pass
            else:
                print '未匹配到相应机构--%s' % row['name']
                orgid = None
            email = hanzizhuanpinpin(row['name'], separator='').split(' ')[0]
            dic['email'] = email + '@investarget3.com'
            dic['org'] = orgid
            tags = [42]
            # tagnames = row['tag'].encode("utf-8")
            # for tagname in tagnames.split('、'):
            #     tagid = getTagId(tagname)
            #     if tagid:
            #         tags.append(tagid)
            dic['tags'] = tags
            response = requests.post(baseurl + 'user/' , data=json.dumps(dic), headers=headers).content
            response = json.loads(response)
            if response['code'] != 1000:
                print '新增失败--%s'%row['name'] + str(response)
        except Exception:
            print 'shibai--%s'%row['name']
            print traceback.format_exc()





   # tables = excel_table_byname('/Users/investarget/Desktop/2017.xlsx')
   # for row in tables:
   #     print row

if __name__=="__main__":
    main()