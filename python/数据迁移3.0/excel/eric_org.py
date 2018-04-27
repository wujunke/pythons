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
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
# baseurl = 'http://192.168.1.201:8000/'
baseurl = 'http://39.107.14.53:8080/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }



def main():
    times = 0
    tables = excel_table_byindex('/Users/investarget/Desktop/python/数据迁移3.0/excel/exceldata/eric.xlsx')
    for row in tables:
        times = times + 1
        try:
            dic = {
                'orgnameC':row['name'],
                'description':row['desc'],
                'webSite':row['web'],
            }
            orglist = json.loads(requests.get(baseurl+'org/?orgname=%s'%dic['orgnameC'],headers=headers).content).get('result',{}).get('data',[])
            if len(orglist) > 0:
                orgid = orglist[0]['id']
                response = requests.put(baseurl+'org/%s/' % orgid, data=json.dumps(dic),headers=headers).content
                response = json.loads(response)
                if response['code'] != 1000:
                    print '覆盖失败--%s'%row['name'] + str(response)
            # else:
            #     response = requests.post(baseurl + 'org/' , data=json.dumps(dic), headers=headers).content
            #     response = json.loads(response)
            #     if response['code'] != 1000:
            #         print '新增失败--%s'%row['name'] + str(response)
            #         orgid = None
            #     else:
            #         orgid = response['result']['id']
            # if orgid:
            #     remark = '投资规模：%s；    投资领域：%s'%(row['fund'], row['industry'])
            #     addOrgRemark(orgid, remark ,dic['orgnameC'])
        except Exception:
            print '失败--%s'%row['name']
            print traceback.format_exc()


def addOrgRemark(orgid, remark, orgname):
    dic = {
        'org':orgid,
        'remark':remark,
    }
    response = requests.post(baseurl + 'org/remark/', data=json.dumps(dic), headers=headers).content
    response = json.loads(response)
    if response['code'] != 1000:
        print '新增备注失败--%s--%s' % (orgname, orgid) + str(response)

   # tables = excel_table_byname('/Users/investarget/Desktop/2017.xlsx')
   # for row in tables:
   #     print row

if __name__=="__main__":
    main()