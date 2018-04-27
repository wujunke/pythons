#coding=utf-8
#coding=utf-8
import _mssql
import json

import sys

import sys

import requests

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)



import xlwt, xlrd


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




def saveToFile(res):
    # style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('融资')
    hang = 0
    ws.write(hang, 0, '名称')
    ws.write(hang, 1, '时间')
    ws.write(hang, 2, '轮次')
    ws.write(hang, 3, '金额')
    ws.write(hang, 4, '投资方')

    ws2 = wb.add_sheet('并购')
    hang2 = 0
    ws2.write(hang2, 0, '名称')
    ws2.write(hang2, 1, '时间')
    ws2.write(hang2, 2, '金额')
    ws2.write(hang2, 3, '并购方')

    hang = hang + 1
    hang2 = hang2 + 1
    for row in res:
        lie = 0
        orgname = row['info']['com_name']  if row['info']['com_name'] else ''

        events = row['event'] if row['event'] else []
        dates = []
        rounds = []
        moneys = []
        invess = []
        for event in events:
            if event['investormerge'] == 1:
                invs = ''
                if event['invsest_with']:
                    invest = []
                    for inv in event['invsest_with']:
                        invest.append(inv['invst_name'])
                    invs = invs + '/'.join(invest)
                dates.append(event['date'])
                rounds.append(event['round'])
                moneys.append(event['money'])
                invess.append(invs)
        if len(dates) > 0:
            datestr = '；\t'.join(dates) if len(dates) > 0 else '暂无'
            roundstr = '；\t'.join(rounds) if len(rounds) > 0 else '暂无'
            moneystr = '；\t'.join(moneys) if len(moneys) > 0 else '暂无'
            invesstr = '；\t'.join(invess) if len(invess) > 0 else '暂无'
            ws.write(hang, lie + 0, str(orgname))
            ws.write(hang, lie + 1, str(datestr))
            ws.write(hang, lie + 2, str(roundstr))
            ws.write(hang, lie + 3, str(moneystr))
            ws.write(hang, lie + 4, str(invesstr))
            hang = hang + 1

        dates2 = []
        moneys2 = []
        invess2 = []
        for event in events:
            if event['investormerge'] == 2:
                dates2.append(event['date'])
                moneys2.append(event['money'])
                invess2.append(event['merger_with'])

        if len(dates2) > 0:
            datestr = '；\t'.join(dates2) if len(dates2) > 0 else '暂无'
            moneystr = '；\t'.join(moneys2) if len(moneys2) > 0 else '暂无'
            invesstr = '；\t'.join(invess2) if len(invess2) > 0 else '暂无'

            ws2.write(hang2, lie + 0, str(orgname))
            ws2.write(hang2, lie + 1, str(datestr))
            ws2.write(hang2, lie + 2, str(moneystr))
            ws2.write(hang2, lie + 3, str(invesstr))
            hang2 = hang2 + 1

    wb.save('sara_文娱体育社交.xls')





# token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'
# baseurl = 'http://192.168.1.201:8000/'

token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
baseurl = 'https://api.investarget.com/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }
url = 'http://192.168.1.201:8000/mongolog/proj?page_size=100&com_name=&com_cat_name=文化娱乐,体育运动,社交网络&com_fund_needs_name=&lang=cn'

def getOrg(page_index):
    orglist = json.loads(requests.get(url + '&page_index=%s'%page_index , headers=headers).content)
    orglist = orglist.get('result', {}).get('data', [])
    if len(orglist) > 0:
        return orglist
    else:
        print 'error'
        return []


def getOrginfo(orgid):

    orginfo = json.loads(requests.get('https://api.investarget.com/mongolog/proj?com_id=%s&lang=cn' % orgid, headers=headers).content).get(
                'result', {}).get('data', {})
    if orginfo:
        return orginfo[0]
    else:
        print '公司信息-未匹配--%s' % orgid
        return None



def getOrgEvent(orgid):
    page_size = 100
    if orgid:
        enentlist = json.loads(requests.get('https://api.investarget.com/mongolog/event?com_id=%s&lang=cn&page_size=%s&date=2016' % (orgid, page_size), headers=headers).content).get(
            'result', {}).get('data', [])
        if len(enentlist) > 0:
            return enentlist
    print '公司事件没有'
    return None

orglist = []
i = 1
while i <= 15:
    li = getOrg(i)
    orglist.extend(li)
    i += 1

resdata = []
for org in orglist:
    orgid = org['com_id']
    orginfo = getOrginfo(orgid)
    orgevent = getOrgEvent(orgid)
    resdata.append({'info':orginfo,'event':orgevent})





saveToFile(resdata)