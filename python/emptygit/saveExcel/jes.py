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
    ws = wb.add_sheet('金融')
    hang = 0
    ws.write(hang, 0, '名称')
    ws.write(hang, 1, '简介')
    ws.write(hang, 2, '网址')
    ws.write(hang, 3, '轮次')
    ws.write(hang, 4, '地区')
    ws.write(hang, 5, '行业')
    ws.write(hang, 6, '电话')
    ws.write(hang, 7, '邮箱')
    ws.write(hang, 8, '地址')
    ws.write(hang, 9, '历史融资')

    hang = hang + 1
    for row in res:
        lie = 0
        orgname = row['info']['com_name']  if row['info']['com_name'] else ''
        desc = row['info']['com_des'] if row['info']['com_des'] else ''
        web = row['info']['com_web'] if row['info']['com_web'] else ''
        lunci = row['info']['invse_round_id'] if row['info']['invse_round_id'] else ''
        area = row['info']['com_addr'] if row['info']['com_addr'] else ''
        indus = row['info']['com_sub_cat_name'] if row['info']['com_sub_cat_name'] else ''
        phone = row['info']['mobile'] if row['info']['mobile'] else ''
        email = row['info']['email'] if row['info']['email'] else ''
        address = row['info']['detailaddress'] if row['info']['detailaddress'] else ''
        events = row['event'] if  row['event'] else []
        eve = []
        for event in events:
            if event['investormerge'] == 1:
                invs = ''
                if event['invsest_with']:
                    invest = []
                    for inv in event['invsest_with']:
                        invest.append(inv['invst_name'])
                    invs = invs + ','.join(invest)
                eve.append('时间：%s   投资方：%s   轮次：%s   投资金额：%s'%(event['date'], invs, event['round'], event['money']))
            else:
                eve.append('时间：%s   并购方：%s   轮次：%s   并购金额：%s'%(event['date'], event['merger_with'], event['round'], event['money']))
        evestr = '\n'.join(eve) if len(eve) > 0 else '暂无'

        ws.write(hang, lie + 0, str(orgname))
        ws.write(hang, lie + 1, str(desc))
        ws.write(hang, lie + 2, str(web))
        ws.write(hang, lie + 3, str(lunci))
        ws.write(hang, lie + 4, str(area))
        ws.write(hang, lie + 5, str(indus))
        ws.write(hang, lie + 6, str(phone))
        ws.write(hang, lie + 7, str(email))
        ws.write(hang, lie + 8, str(address))
        ws.write(hang, lie + 9, str(evestr))



        # f = open('user-1.txt', 'a')
        # f.writelines(str(row[1])+';'+str(row[2])+';'+str(row[3])+';'+str(row[4])+';'+str(row[5])+';'+str(row[6])+';'+tags+';'+remarks)
        # f.writelines('\n')
        # f.close()
        hang = hang + 1
    wb.save('jes_project2.xls')





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
url = 'https://api.investarget.com/mongolog/proj?page_size=50&com_name=&com_sub_cat_name=%E8%82%A1%E7%A5%A8%2C%E5%80%9F%E8%B4%B7%2C%E6%94%AF%E4%BB%98%2C%E4%BF%9D%E9%99%A9%2C%E7%90%86%E8%B4%A2%2C%E6%8A%95%E8%9E%8D%E8%B5%84%2C%E8%99%9A%E6%8B%9F%E8%B4%A7%E5%B8%81%2C%E9%87%91%E8%9E%8D%E4%BF%A1%E6%81%AF%E5%8C%96%2C%E9%87%91%E8%9E%8D%E7%BB%BC%E5%90%88%E6%9C%8D%E5%8A%A1%2C%E5%A4%96%E6%B1%87%E6%9C%9F%E8%B4%A7%E8%B4%B5%E9%87%91%E5%B1%9E%2C%E5%85%B6%E4%BB%96%E9%87%91%E8%9E%8D%2C%E4%BF%A1%E7%94%A8%E5%8F%8A%E5%BE%81%E4%BF%A1%2C%E6%B6%88%E8%B4%B9%E9%87%91%E8%9E%8D%2C%E5%BD%A9%E7%A5%A8&com_born_date=&com_addr=%E5%8C%97%E4%BA%AC%2C%E4%B8%8A%E6%B5%B7%2C%E6%B5%99%E6%B1%9F%2C%E5%B9%BF%E4%B8%9C%2C%E6%B1%9F%E8%8B%8F%2C%E7%A6%8F%E5%BB%BA%2C%E6%B9%96%E5%8C%97%2C%E5%9B%9B%E5%B7%9D%2C%E9%87%8D%E5%BA%86&invse_round_id=Pre-A%E8%BD%AE%2CA%E8%BD%AE%2CA%2B%E8%BD%AE%2CPre-B%E8%BD%AE%2CB%E8%BD%AE%2CB%2B%E8%BD%AE%2CC%E8%BD%AE%2CC%2B%E8%BD%AE%2CD%E8%BD%AE&com_status=&com_fund_needs_name=&lang=cn'
# 股票,借贷,支付,保险,理财,投融资,虚拟货币,金融信息化,金融综合服务,外汇期货贵金属,其他金融,信用及征信,消费金融,彩票
def getOrg(page_index):
    headers = {
        'token': '85906a6cf0bb6c1542a43984eb0884bc20e41ed11411a66b',
        'source': '1',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    orglist = json.loads(requests.get(url + '&page_index=%s'% page_index , headers=headers).content)
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
        enentlist = json.loads(requests.get('https://api.investarget.com/mongolog/event?com_id=%s&lang=cn&page_size=%s' % (orgid, page_size), headers=headers).content).get(
            'result', {}).get('data', [])
        if len(enentlist) > 0:
            return enentlist
    print '公司事件没有'
    return None

orglist = []
i = 1
while i <= 24:
    li = getOrg(i)
    orglist.extend(li)
    print 'page = %s' % str(i)
    i += 1


resdata = []
for org in orglist:
    orgid = org['com_id']
    orginfo = getOrginfo(orgid)
    orgevent = getOrgEvent(orgid)
    resdata.append({'info':orginfo,'event':orgevent})





saveToFile(resdata)