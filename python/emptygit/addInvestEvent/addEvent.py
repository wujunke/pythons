#coding=utf-8


import json
import random
import requests
import time

from datetime import datetime
from selenium import webdriver

from data2.itjuzi_config import base_url, token, iplist, iplist2
import xlwt, xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# sys.setrecursionlimit(10000000)
session = requests.Session()
# session.trust_env = False


proxy_ip = '112.87.80.244:6915'
start_id = 6912


def getAllEventWith_ItjuziOrgId(itjuziOrgId, page=None, events=None):
    print datetime.now()
    # headers = {
    #     'Accept': 'application/json, text/javascript, */*; q=0.01',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    #     'Connection': 'keep-alive',
    #     'Host': 'www.itjuzi.com',
    #     'Referer': 'https://www.itjuzi.com/investfirm/%s'%itjuziOrgId,
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    #     'X-Requested-With': 'XMLHttpRequest',
    #     'Cookie': 'acw_tc=AQAAANXvAzs4+QkABSXBfIW0a8aGRUQf; gr_user_id=55dc8af7-7401-49bc-bcfc-f1d93f716d15; MEIQIA_EXTRA_TRACK_ID=0zsxMGF1VQND1EHLYrVanekuTyE; identity=18616837957%40test.com; remember_code=e9ER51bLu8; unique_token=439977; paidtype=vip; acw_sc__=5abdb8587239a8b9d69e4c56a3cdb964bcb606fa; _ga=GA1.2.136595813.1522306319; _gid=GA1.2.1058318448.1522306319; _gat=1; gr_session_id_eee5a46c52000d401f969f4535bdaa78=8985f86e-8f6d-47aa-8f2b-570a7dc46fd9; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1522029503,1522032015,1522032547,1522306319; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1522383104; session=38333bcd85ed3e26da1ff7efb11596129aacf9f8'
    # }
    page = page if page else 1
    events = events if events else []
    # 发现这个接口不用登录也可以调用，不过每个ip大概十分钟就被屏蔽了，需要更换代理
    url = 'https://www.itjuzi.com/investment/info/search?id=%s&page=%s&scope=all&state=all&feature=all&sort=time' % (itjuziOrgId, page)
    try:
        driver.get(url)
        data = driver.page_source
        data = data.replace('<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>', '').replace(
            '</body></html>', '')
        res = json.loads(data)
    except ValueError:
        print '获取失败--%s-%s' % (itjuziOrgId, page)
        events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    except requests.exceptions.ConnectionError:
        print '代理连接失败--%s-%s' % (itjuziOrgId, page)
        events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    except requests.exceptions.ReadTimeout:
        print '请求超时--%s-%s' % (itjuziOrgId, page)
        events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    else:
        print '成功--%s-%s' % (itjuziOrgId, page)
        if isinstance(res['data'], list):
            events = events + res['data']
        pages = res['page']
        if pages:
            if pages['totalPages'] > pages['currentPage']:
                page += 1
                if page < 4:
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
        response = session.post(base_url + 'org/investevent/', data=json.dumps(data), headers=headers)
        response = response.content
        response = json.loads(response)
        if response['code'] != 1000 and response['code'] != 5007:
            print '新增投资事件失败--%s' % data['comshortname'] + str(response)




chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://%s' % proxy_ip)
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
driver.set_window_size('1280','800')



orglist = []
with open("/Users/investarget/pythons/python/emptygit/addInvestEvent/name_id_comparetable","r") as f:
    lines = f.readlines()
    for line in lines:
        orglist.append(json.loads(line.replace('\n','')))

for row in orglist:
    itjuzi_id = row.get('itjuzi_id', None)
    haituo_id = row.get('haituo_id', None)
    if itjuzi_id >= start_id:
        getAndSaveEvent(int(itjuzi_id), int(haituo_id))