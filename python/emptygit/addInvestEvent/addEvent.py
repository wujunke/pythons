#coding=utf-8
import json
import requests
from datetime import datetime
import time
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

session = requests.Session()
# session.trust_env = False
# http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=11&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=
# http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=

base_url = 'https://api.investarget.com/'
# base_url = 'http://192.168.1.201:8000/'

token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'

proxy_ip = '140.143.96.216:80'

start_id = 1694

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://%s' % proxy_ip)
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
driver.set_window_size('1280','800')



def getAllEventWith_ItjuziOrgId(itjuziOrgId, page=None, events=None):
    global driver
    print(datetime.now())
    page = page if page else 1
    events = events if events else []
    # 发现这个接口不用登录也可以调用
    url = 'https://www.itjuzi.com/investment/info/search?id=%s&page=%s&scope=all&state=all&feature=all&sort=time' % (itjuziOrgId, page)
    try:
        driver.get(url)
        data = driver.page_source
        data = data.replace('<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>', '').replace(
            '</body></html>', '')
        res = json.loads(data)
    except ValueError:
        print('获取失败--%s-%s' % (itjuziOrgId, page))
        events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    except requests.exceptions.ConnectionError:
        print('代理连接失败--%s-%s' % (itjuziOrgId, page))
        events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    except requests.exceptions.ReadTimeout:
        print('请求超时--%s-%s' % (itjuziOrgId, page))
        events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    else:
        print('成功--%s-%s' % (itjuziOrgId, page))
        if isinstance(res['data'], list):
            events = events + res['data']
        pages = res['page']
        if pages:
            if pages['totalPages'] > pages['currentPage']:
                page += 1
                if page < 2:
                    events = getAllEventWith_ItjuziOrgId(itjuziOrgId, page, events)
    return events




def getAndSaveEvent(itjuzi_id, haituo_id):
    events = getAllEventWith_ItjuziOrgId(itjuzi_id)
    print('%s--抓取完成'%itjuzi_id)
    for event in events:
        data = {
            'org': haituo_id,
            'comshortname': event['invest_name'],
            'com_id': event['com_id'],
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
            print('新增投资事件失败--%s' % data['comshortname'] + str(response))



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