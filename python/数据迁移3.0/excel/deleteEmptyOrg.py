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




token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
# baseurl = 'http://192.168.1.201:8000/'
baseurl = 'https://api.investarget.com/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }



from future.backports.urllib import parse


tables = excel_table_byindex('/Users/investarget/pythons/python/数据迁移3.0/excel/exceldata/emptyorg.xlsx')
i = 1


def getOrgID(orgname=None):
    if orgname:
        url = baseurl + 'org/?orgname=%s' % parse.quote(orgname,encoding='utf-8')
        orglist = json.loads(requests.get(url, headers=headers).content).get('result', {}).get('data', [])
        if len(orglist) > 1:
            print('有多个搜索结果--%s' % orgname)
        elif len(orglist) == 1:
            return orglist[0]['id']
    return None


def deleteOrg(org_id):

    url = baseurl + 'org/%s/' % org_id
    res = requests.delete(url, headers=headers).content
    res = json.loads(res)
    if res['code'] != 1000:
        print('######删除失败----%s' % org_id)
        print(res)
    else:
        print('******删除成功----%s' % org_id)


for row in tables:
    i += 1
    if i <= 1422:
        orgname = row[u'机构名称']
        isDelete = row.get(u'保留')
        if isDelete in [u'', None, u' ']:
            org_id = getOrgID(orgname)
            if org_id:
                deleteOrg(org_id)
            else:
                print('未找到--%s' % i)

