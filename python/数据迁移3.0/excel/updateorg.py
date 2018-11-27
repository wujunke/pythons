# -*- coding: utf-8 -*-
import codecs
import os
import traceback
import  xdrlib ,sys

import re

from future.backports.urllib import parse
from pypinyin import slug as hanzizhuanpinpin
import requests
import xlrd
import json

reload(sys)
sys.setdefaultencoding('utf-8')

# 遍历文件夹下的文件，返回路径list
def eachFile(filepath):
    filelist = []
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        if child != '/Users/investarget/Desktop/投资机构/.DS_Store':
            filelist.append(child)
    return filelist

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
    colnames = table.row_values(colnameindex)  # 某一行数据
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list

# token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00' # 251 token
# baseurl = 'http://192.168.1.201:8000/'

token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf' # 39 token
baseurl = 'https://api.investarget.com/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }

orgidlist = [42571,42570,42564,42560,42557,42552,42549,42544,42538,42536,42533,42515,42474,42467,42230,42228,42221,42193,42186,42184,42171,42169,42167,42166,42164,42160,42155,42153,42148,42139,42127,42118,42096,42088,42053,42021,42003,41869,33888,33874,33864,33862,33860,33821,33818,33817,33811,33808,33807,33794]


def getOrgId(orgname=None, orgfullname=None):
    if orgfullname:
        url = baseurl + 'org/?orgfullname=%s' % parse.quote(orgfullname,encoding='utf-8')
        orglist = json.loads(requests.get(url, headers=headers).content).get('result', {}).get('data', [])
        if len(orglist) > 0:
            return orglist[0]['id']
    if orgname:
        url = baseurl + 'org/?orgname=%s' % parse.quote(orgname,encoding='utf-8')
        orglist = json.loads(requests.get(url, headers=headers).content).get('result', {}).get('data', [])
        if len(orglist) > 0:
            for org in orglist:
                if org['id'] in orgidlist:
                    return org['id']
    return None



def updateOrgTag(org_id, tagList):
    data = {'tags': tagList}
    url =  baseurl + 'org/%s/' % org_id
    res = requests.put(url, data=json.dumps(data), headers=headers).content
    res = json.loads(res)
    if res['code'] != 1000:
        print res



allTags = {}
tagUrl = baseurl + 'source/tag'
response = requests.get(tagUrl, headers=headers).content
res = json.loads(response)['result']
for tag in res:
    allTags[tag['nameC']] = tag['id']


def changeTagIdByName(tagNameStrings):
    tagNameList = tagNameStrings.split('、')
    resList = []
    for tagName in tagNameList:
        tagid = allTags.get(tagName)
        if tagid:
            resList.append(tagid)
    return resList



tables = excel_table_byindex('/Users/investarget/pythons/python/数据迁移3.0/excel/exceldata/updatetag.xlsx')
rowid = 0
for row in tables:
    rowid += 1
    print(rowid)
    if rowid >= 1:
        org_id = getOrgId(orgname=row[u'机构简称'])
        if org_id:
            tagids = changeTagIdByName(row[u'标签'])
            updateOrgTag(org_id, tagids)



