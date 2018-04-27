#coding=utf-8


import json
import random
import requests
import time
from data2.itjuzi_config import base_url, token, iplist, iplist2
import xlwt, xlrd
import sys
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


def rand_proxie():
    return {'http':'http://%s' % iplist[random.randint(0, len(iplist)) - 1],}

def rand_proxie2():
    return {'https':'https://%s' % iplist2[random.randint(0, len(iplist2)) - 1],}





def getAllEventWith_ItjuziOrgId(itjuziOrgId, page=None, events=None):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Connection': 'keep-alive',
        'Host': 'www.itjuzi.com',
        'Referer': 'https://www.itjuzi.com/investfirm/%s'%itjuziOrgId,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'acw_tc=AQAAANXvAzs4+QkABSXBfIW0a8aGRUQf; gr_user_id=55dc8af7-7401-49bc-bcfc-f1d93f716d15; MEIQIA_EXTRA_TRACK_ID=0zsxMGF1VQND1EHLYrVanekuTyE; identity=18616837957%40test.com; remember_code=e9ER51bLu8; unique_token=439977; paidtype=vip; acw_sc__=5abdc688b88feeaa5d00e625377472cf32b3760f; gr_session_id_eee5a46c52000d401f969f4535bdaa78=8985f86e-8f6d-47aa-8f2b-570a7dc46fd9; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1522029503,1522032015,1522032547,1522306319; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1522386577; session=0811c0e45269ca6f84bba2d7d09905400f385564; _gat=1; _ga=GA1.2.136595813.1522306319; _gid=GA1.2.1058318448.1522306319'
    }
    page = page if page else 1
    events = events if events else []
    url = 'https://www.itjuzi.com/investment/info/search?id=%s&page=%s&scope=all&state=all&feature=all&sort=time' % (itjuziOrgId, page)
    proxy = rand_proxie2()
    try:
        res = requests.get(url, headers=headers, proxies=proxy, timeout=30)
        if res.status_code == 200:
            res = json.loads(res.content)
        else:
            raise ValueError
    except ValueError:
        print '获取失败--%s-%s-%s' % (itjuziOrgId, page, proxy)
        events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    except requests.exceptions.ConnectionError:
        print '代理连接失败--%s-%s-%s' % (itjuziOrgId, page, proxy)
        events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    except requests.exceptions.ReadTimeout:
        print '请求超时--%s-%s-%s' % (itjuziOrgId, page, proxy)
        events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    else:
        print '成功--%s-%s-%s' % (itjuziOrgId, page, proxy)
        events = events + res['data']
        pages = res['page']
        if pages:
            if pages['totalPages'] > pages['currentPage']:
                page += 1
                events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    return events




def getAndSaveEvent(itjuzi_id, haituo_id):
    events = getAllEventWith_ItjuziOrgId(itjuzi_id)
    print '%s--抓取完成'%itjuzi_id
    for event in events:
        data = {
            'org': haituo_id,
            'comshortname': event['invest_name'],
            'com_id': event['id'],
            'industrytype': event['invest_scope'],
            'investDate': str(event['time']) + 'T12:00:00' if event['time'] else None,
            'investType': event['invest_round'],
            'investSize': event['invest_money'],
        }
        headers = {
            'token': token,
            'source': '1',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        response = requests.post(base_url + 'org/investevent/', data=json.dumps(data), headers=headers).content
        response = json.loads(response)
        if response['code'] != 1000:
            print '新增投资事件失败--%s' % data['comshortname'] + str(response)




# def getAndDeleteOrgEvent(haituo_id):
#     headers = {
#         'token': token,
#         'source': '1',
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#     }
#     response = requests.get(base_url + 'org/investevent/?org=%s'%haituo_id, headers=headers).content
#     response = json.loads(response)
#     if response['code'] != 1000:
#         print '获取机构投资事件失败--%s' % haituo_id + str(response)
#     else:
#         events = response['result']
#         for event in events:
#             response = requests.delete(base_url + 'org/investevent/%s/'%event['id'] % haituo_id, headers=headers).content
#             response = json.loads(response)
#             if response['code'] != 1000:
#                 print '删除机构投资事件失败--%s' % event['id'] + str(response)


def addOrg(orgname):
    data = {
        'orgnameC': orgname,
        'orgnameE': orgname,
        'orgfullname': orgname,
    }
    headers = {
        'token': token,
        'source': '1',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.post(base_url + 'org/', data=json.dumps(data), headers=headers).content
    response = json.loads(response)
    if response['code'] != 1000:
        print '新增机构失败--%s' % orgname + str(response)
        return None
    else:
        return response['result']['id']


tables = excel_table_byindex('/Users/investarget/Desktop/IT桔子机构对照表1-835.xlsx')

for row in tables:
    itjuzi_id = row.get('itjuzi_id', None)
    if itjuzi_id > 12:
        haituo_id = row.get('haituo_id', None)
        if itjuzi_id:
            if not haituo_id:
                # 机构不存在，新增机构，在增加投资事件
                haituo_id = addOrg(row['itjuzi_name'])
                if haituo_id:
                    getAndSaveEvent(int(itjuzi_id), int(haituo_id))
            else:
                # if not row['isrepeat']:
                    # 没有重复，先删除之前的
                    # getAndDeleteOrgEvent(int(haituo_id))
                # 有重复，不删除之前的，直接新增投资事件
                getAndSaveEvent(int(itjuzi_id), int(haituo_id))