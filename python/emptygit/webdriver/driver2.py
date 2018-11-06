#coding=utf-8
import json
import random


import datetime
import requests
import time
from bs4 import BeautifulSoup

from selenium import webdriver
# 引入配置对象DesiredCapabilities
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import FirefoxProfile

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from data2.itjuzi_config import base_url, token,  iplist
import sys

from webdriver.parseItjuziHtml import parseComDetailHtml, parseComMemberByDriver, parseComFinanceByDriver, \
    getComIndustryInfo, getComBasic, parseComIndustryInfoByDriver

reload(sys)
sys.setdefaultencoding('utf-8')

session = requests.Session()
session.trust_env = False

def rand_proxie():
    return {'http':'http://%s' % iplist[random.randint(0, len(iplist)) - 1],}


def saveCompanyIndustyInfoToMongo(info):
    try:
        res = session.post(base_url + 'mongolog/projinfo', data=json.dumps(info),
                        headers={'Content-Type': 'application/json', 'token': token}).content
    except requests.exceptions.ProxyError:
        print('保存工商信息，链接失败，重试')
        time.sleep(5)
        saveCompanyIndustyInfoToMongo(info)
    except Exception:
        print('保存工商信息，链接失败，失败')
        pass
    else:
        res = json.loads(res)
        if res['code'] == 1000:
            pass
        elif res['code'] == 8001:
            pass
        else:
            print('错误数据indus_info----' + 'com_id=%s' % info['com_id'])
            print(res)


def saveCompanyNewsToMongo(newslist,com_id=None,com_name=None):
    for news in newslist:
        if news.get('linkurl'):
            news['com_id'] = com_id if isinstance(com_id, int) else int(com_id)
            news['com_name'] = com_name
            saverequest(url=(base_url + 'mongolog/projnews'), data=news, headers={'Content-Type': 'application/json', 'token': token})


def saverequest(url, data , headers):
    try:
        res = session.post(url, data=json.dumps(data),headers=headers).content
    except requests.exceptions.ProxyError:
        print('保存新闻信息，链接失败，重试')
        time.sleep(5)
        saverequest(url, data, headers)
    except Exception:
        print('保存新闻信息，链接失败，失败')
    else:
        res = json.loads(res)
        if res['code'] == 1000:
            pass
        elif res['code'] == 8001:
            pass
        else:
            print('错误数据news----' + 'com_id=%s' % data['com_id'])
            print(res)



def updateCompanyToMongo(info):
    try:
        res = session.post(base_url + 'mongolog/proj', data=json.dumps(info), headers={'Content-Type': 'application/json', 'token': token}).content
    except requests.exceptions.ProxyError:
        print('更新公司名称，链接失败，重试')
        time.sleep(5)
        updateCompanyToMongo(info)
    except Exception:
        print('更新公司名称，链接失败，跳过')
    else:
        res = json.loads(res)
        if res['code'] == 1000:
            pass
        elif res['code'] == 8001:
            pass
        else:
            print('错误数据' + 'com_id：%s' % str(info['com_id']))
            print(res)



def get_companglist(page_index):
    projlist = None
    res = session.get(base_url + 'mongolog/proj?page_size=10&sort=&page_index=%s&com_name=...' % page_index, headers={'Content-Type': 'application/json', 'token': token})
    if res.status_code == 200:
        res = json.loads(res.content)
        if res['code'] == 1000:
            projlist = res['result']['data']
        else:
            print('获取全库项目列表有误----' + 'page_index=%s' % page_index)
            print(res)
    return projlist



def saveEventToMongo(events, com_id):
    for event in events:
        moneystr = str(event.get('money',''))
        if '$' in moneystr or '美元' in moneystr:
            event['currency'] = '美元'
        elif '￥' in moneystr or '人民币' in moneystr:
            event['currency'] = '人民币'
        elif '€' in moneystr or '欧元' in moneystr:
            event['currency'] = '欧元'
        elif '£' in moneystr or '英镑' in moneystr:
            event['currency'] = '英镑'
        elif '￥' in moneystr or '日元' in moneystr:
            event['currency'] = '日元'
        elif '₩' in moneystr or '韩元' in moneystr:
            event['currency'] = '韩元'
        elif '₹' in moneystr or '卢比' in moneystr:
            event['currency'] = '卢比'
        elif '￥' in moneystr or '港元' in moneystr:
            event['currency'] = '港元'
        event['com_id'] = com_id
        res = session.post(base_url + 'mongolog/event', data=json.dumps(event),
                            headers={'Content-Type': 'application/json', 'token': token}).content
        res = json.loads(res)
        if res['code'] == 1000:
            print('新增invse--' + str(res['result'].get('invse_id', res['result'].get('merger_id', None))))
        elif res['code'] == 8001:
            print('重复invest')
        else:
            print('错误event数据--%s'%repr(event))
            print(res)

orglist = []
with open("/Users/investarget/pythons/python/emptygit/addInvestEvent/name_id_comparetable","r") as f:
    lines = f.readlines()
    for line in lines:
        orglist.append(json.loads(line.replace('\n','')))



def getOrgIdByOrgname(orgname):
    orgid = None
    if orgname and orgname != u'未透露':
        for org in orglist:
            if org['itjuzi_name'] == orgname:
                orgid = org['haituo_id']
    return orgid


def saveEventToMySqlOrg(events, com_id, com_name, industryType):
    for event in events:
        orglist = []
        if event['investormerge'] == 1:
            for invst_dic in event['invsest_with']:
                orglist.append(invst_dic['invst_name'])
        else:
            orglist.append(event['merger_with'])
        for orgname in orglist:
            orgid = getOrgIdByOrgname(orgname)
            if orgid:
                data = {
                    'org': orgid,
                    'comshortname': com_name,
                    'com_id': com_id,
                    'industrytype': industryType,
                    'investDate': str(event['date'] ) + 'T12:00:00' if event['date']  else None,
                    'investType': event['round'],
                    'investSize': event['money'],
                }
                res = session.post(base_url + 'org/investevent/', data=json.dumps(data),
                                    headers={'Content-Type': 'application/json', 'token': token}).content
                res = json.loads(res)
                if res['code'] == 1000:
                    print('新增org_invest--' + str(res['result'].get('id', None)))
                elif res['code'] == 5007:
                    print('重复org_invest')
                else:
                    print('错误org_invest数据--%s'%repr(res))
                    print(res)


def getpage(driver,com_id,wait):
    try:
        driver.get("https://www.itjuzi.com/company/%s" % com_id)
        time.sleep(2)
        page = driver.page_source
        resdic, com_name, full_name = parseComDetailHtml(page)
        if resdic:
            resdic['com_id'] = int(com_id)
            print(com_name)
            news = resdic['news']
            saveCompanyNewsToMongo(news, resdic['com_id'], com_name)

            eventlist = parseComFinanceByDriver(driver)
            indus_member = parseComMemberByDriver(driver)
            saveEventToMongo(eventlist, resdic['com_id'])

            basicDic = getComBasic(driver, com_id)
            resdic.update(basicDic)
            updateCompanyToMongo(resdic)

            industryInfoDic = parseComIndustryInfoByDriver(driver, com_id)
            industryInfoDic['indus_member'] = indus_member
            saveCompanyIndustyInfoToMongo(industryInfoDic)
        else:
            if com_name:
                if com_name in (u'找不到您访问的页面',):
                    print('com_id:%s 未找到'%str(com_id))
                    print(com_name)
                elif com_name in (u'www.itjuzi.com', u'502 Bad Gateway',u'403'):
                    print('空页面--%s' % com_id)
                    print('现在的时间是：%s' % datetime.datetime.now())
                    print('等待%s分钟后重试' % wait)
                    time.sleep(wait)
                    getpage(driver, com_id, wait)
                else:
                    print('com_id:%s' % str(com_id))
                    print(com_name)
            else:
                print('空页面--%s' % com_id)
                print('现在时间：%s' % datetime.datetime.now())
                print('等待%s分钟后重试'%wait)
                time.sleep(wait)
                getpage(driver,com_id,wait)
    except TimeoutException:
        print('打开页面超时，跳过公司：id--%s'%com_id)

chrome_options = webdriver.ChromeOptions()
prefs={
     'profile.default_content_setting_values': {
        'images': 2,   #禁用图片
        # 'javascript':2   #禁用JS
    }
}
chrome_options.add_experimental_option('prefs',prefs)
# chrome_options.add_argument('--proxy-server=http://118.31.223.194:3128')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
driver.set_window_size('1280','800')
print('正在打开网站...')
driver.get("https://www.itjuzi.com/login?url=%2F")
time.sleep(5)
print('正在输入账号...')
account = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/div[1]/input')
account.click()
# account.send_keys("18616837957",)
account.send_keys("18964687678",)
time.sleep(1)
print('正在输入密码...')
paswd = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/div[2]/input')
# paswd.send_keys("x81y0122",)
paswd.send_keys("123456789")
time.sleep(1)
print('正在登录...')
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/button').click()
time.sleep(1)

acc_token = driver.execute_script("return localStorage.getItem('accessToken')")

page_index = 1
while page_index <= 6:
    projlist = get_companglist(1)

    print('当前页码：page_index = %s' % str(page_index))
    print(datetime.datetime.now())
    page_index += 1
    if projlist:
        for proj in projlist:
            com_id = proj['com_id']
            # com_id = 2
            getpage(driver, com_id, 10)

driver.quit()



