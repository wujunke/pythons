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
baseurl = 'https://api.investarget.com/'

headers = {
        'Authorization':'Bearer EpjCMXqTp3UK0mzW5DbCBzw7iJ6de-aVVrcehWQhESM9X1O2LZWWjaQF0LR8Q2P7Vsqy2QF_DMR4xADhRxz13hlmvSMTKl6e2yQsTPrwoF-zXsicjDLOwxeJv52ZMGe4Qj6vz0kBaQC3qRmY2oibi30IGfgxgua-zYZsh6aoU9ROMNfcIUXGmL3C-mpqUIN1O4HGZdYXZR8S9OQaN4LlxFi1xxgZyJz5tsGMEkmv2VNVnTNPFyY-7QsdNt5PDNjjRqKxhcjqB7t75Kr6s3RV4CBNOAiKvGHjh4hXhJU6TuQixcxLDNEtiQt3OE0aYqmNTYZFYCYwSfA3pbnpuKnx0sD2xQQ8ulK9boJuI47ULtm9IHPREyGJX9ztFjSrwVMPatWzGAkh5gkUJniwAE5rRXzl1xFGXq83YGiRbt8umjhKp7ecOYl062KH9KFnnm4Y6T_xup2RBAK9Jm-ib8y0kLxlYNty2HjCiJFkhpRadpLbWHi50JQE7VzHvTEXPlZoKWSwbommcugYsCT0GalcTQ',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }


def getAllCountry():

    res = json.loads(requests.get(baseurl+'/api/services/InvestargetApi/orgArea/GetOrgAreas?input.lang=cn',headers=headers).content)
    re = res.get('result')['items']
    return re

allcountry = getAllCountry()
def getCountryId(countryname):
    reid = None
    for country in allcountry:
        if country.get('areaName') == countryname:
            reid = country.get('id')
    return reid
def getAllTitle():

    res = json.loads(requests.get(baseurl+'/api/services/InvestargetApi/title/GetTitles?input.lang=cn',headers=headers).content)
    re = res.get('result')
    return re

alltitle = getAllTitle()
def getTitleId(titlename):
    reid = None
    for title in alltitle:
        if title.get('titleName') == titlename:
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
            dic = {
                'MobileAreaCode':"86",
                'auditStatus': "1",
                'cardBucket':"image",
                'cardKey':"",
                'company':row['company'],
                'countryId':42,
                'departMent':"",
                'gender':0,
                'head':'',
                'headId':2000045,
                'industryId':None,
                'mandate':0,
                'name_en':"",
                'partnerId': None,
                'photoBucket':"image",
                'photoKey':'',
                'registerSource':4,
                'name': row['name'],
                'mobile': int(row['phone']),
                'emailAddress': None,
                'titleId': getTitleId(row['position']),
                'weChat': row['weixin'],
                'orgId': None,
                'userTagses': 61,
                'orgAreaId': getCountryId(row['city'].split('、')[0]),
                'userType': 1,
                'isActive': True,
                'Password': 'Aa123456',
            }
            email = hanzizhuanpinpin(row['name'], separator='').split(' ')[0]
            dic['emailAddress'] = email + '@investarget3.com'
            response = requests.post(baseurl + '/api/services/InvestargetApi/user/CreateUser' , data=json.dumps(dic), headers=headers).content
            response = json.loads(response)
            if response['success'] is False:
                print '新增失败--%s'%row['name'] + str(response['error'])
        except Exception:
            print 'shibai--%s'%row['name']
            print traceback.format_exc()





   # tables = excel_table_byname('/Users/investarget/Desktop/2017.xlsx')
   # for row in tables:
   #     print row

if __name__=="__main__":
    main()