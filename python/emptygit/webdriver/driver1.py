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
from data2.itjuzi_config import base_url, token,  iplist

#会话不使用代理，用于更新/插入数据
session = requests.Session()
session.trust_env = False

#解析driver页面信息
def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.title:
        com_name = soup.title.text
        if com_name in (u'www.itjuzi.com', u'找不到您访问的页面', u'502 Bad Gateway', u'403'):
            return None, com_name
        com_web = None
        a_s = soup.find('i', class_='fa fa-link t-small', )
        if a_s:
            com_web = a_s.parent['href']
        name = soup.find('h1', class_='seo-important-title', )
        # full_name = ''
        if name:
            com_name = name.text.replace(u'\t', u'')
            com_name = com_name.split('\n')[1]
            # full_name = name['data-fullname']
        # 联系方式
        ll = ['mobile', 'email', 'detailaddress']
        response = {}
        contact_ul = soup.find('ul',class_='list-block aboutus')
        if contact_ul:
            for info in contact_ul.find_all('li'):
                if info.find('i',class_='fa icon icon-phone-o'):
                    response['mobile'] = info.text.replace('\n','').replace('\t','')
                if info.find('i',class_='fa icon icon-email-o'):
                    response['email'] = info.text.replace('\n','').replace('\t','')
                if info.find('i',class_='fa icon icon-address-o'):
                    response['detailaddress'] = info.text.replace('\n','').replace('\t','')

        #投资信息


        #融资信息
        investents = soup.find(id='invest-portfolio')
        eventtable = investents.find('table')
        eventtrlist = eventtable.find_all('tr')
        eventlist = []
        for eventtr in eventtrlist:
            if eventtr.find(class_='date'):
                date = eventtr.find(class_='date').text
                round = eventtr.find(class_='round').text
                money = eventtr.find(class_='finades').text

                link = eventtr.find(class_='finades').a['href']
                type = link.split('/')[-2]
                event_id = link.split('/')[-1]
                data = {
                    'date': date,
                    'round': round,
                    'money': money,
                }
                if type == 'merger':
                    data['investormerge'] = 2
                    data['merger_id'] = event_id
                    data['merger_with'] = eventtr.find('a', class_='line1 c-gray').text if eventtr.find('a',
                                                                                                        class_='line1 c-gray') else ''
                else:
                    data['investormerge'] = 1
                    data['invse_id'] = event_id
                    line1s = eventtr.find_all('a', class_='line1')
                    invsest_with = []
                    for line1 in line1s:
                        url = line1.get('href', None)
                        invst_name = line1.text
                        invsest_with.append({'url': url, 'invst_name': invst_name})
                    data['invsest_with'] = invsest_with
                eventlist.append(data)
        response['events'] = eventlist

        industryType = soup.find('a', class_='one-level-tag').text if soup.find('a', class_='one-level-tag') else ''
        response['industryType'] = industryType


        # 团队信息
        members = []
        membersul = soup.find('ul', class_='list-unstyled team-list limited-itemnum')
        if membersul:
            lilist = membersul.find_all('li')
            for li in lilist:
                dic = {}
                dic['姓名'] = li.find('a', class_='person-name').text.replace('\n','').replace('\t','') if li.find('a', class_='person-name') else None
                dic['职位'] = li.find('div', class_='per-position').text.replace('\n','').replace('\t','') if li.find('div', class_='per-position') else None
                dic['简介'] = li.find('div', class_='per-des').text.replace('\n','').replace('\t','') if li.find('div', class_='per-des') else None
                members.append(dic)
        response['indus_member'] = members

        # 新闻
        res = soup.find_all('ul', class_='list-unstyled news-list')
        news = []
        for ss in res:
                # print ss.name
                lilist = ss.find_all('li')
                for li in lilist:
                    dic = {}
                    dic['newsdate'] = li.find('span', class_='news-date').text.replace('\n','').replace('\t','') if li.find('span', class_='news-date') else None
                    a = li.find('a', class_='line1')
                    dic['title'] = a.text.replace('\n','').replace('\t','')
                    dic['linkurl'] = a['href']
                    dic['newstag'] = li.find('span', class_='news-tag').text.replace('\n','').replace('\t','') if li.find('span', class_='news-tag') else None
                    news.append(dic)
        response['news'] = news
        response['com_web'] = com_web

        # 工商信息
        # recruit-info
        recruit_info = soup.find('div',id='recruit-info')
        if recruit_info:
            tablistul = recruit_info.find('ul',class_='nav-tabs list-inline stock_titlebar')
            tablistli = tablistul.find_all('li')
            for tabli in tablistli:
                tabhref = tabli.a['href'].replace('#','')
                if tabhref in ['indus_base',u'indus_base']:   # 基本信息
                    indus_base = recruit_info.find('div', id=tabhref)
                    com_full_name = indus_base.find('th').text
                    infolisttd = indus_base.find_all('td')
                    infodic = {}
                    for info in infolisttd:
                        if info:
                            if info.find('span', class_='tab_title') and info.find('span', class_='tab_main'):
                                if info.find('span', class_='tab_title').text:
                                    infodic[info.find('span', class_='tab_title').text] = info.find('span', class_='tab_main').text.replace('\n','').replace('\t','')
                    infodic[u'公司名称:'] = com_full_name.replace('\n','').replace('\t','')
                    response[tabhref] = infodic

                if tabhref in ['indus_shareholder', u'indus_shareholder','indus_foreign_invest', u'indus_foreign_invest', 'indus_busi_info', u'indus_busi_info']:   #  股东信息、企业对外投资信息、工商变更信息
                    indus_shareholder = recruit_info.find('div', id=tabhref)
                    thead = indus_shareholder.find('thead')
                    if thead:
                        theadthlist = thead.find_all('th')
                        theadlist = []
                        for theaditem in theadthlist:
                            theadlist.append(theaditem.text)
                        tbody = indus_shareholder.find('tbody')
                        infolist = []
                        if tbody:
                            trlist = tbody.find_all('tr')
                            for tr in trlist:
                                infodic = {}
                                tdlist = tr.find_all('td')
                                for i in range(0, len(theadlist)):
                                    try:
                                        infodic[theadlist[i]] = tdlist[i].text.replace('\n','').replace('\t','') if tdlist[i].text else None
                                    except IndexError:
                                        print '数组越界',len(theadlist),len(tdlist)
                                        pass
                                if infodic != {}:
                                    infolist.append(infodic)
                        response[tabhref] = infolist
        return response, com_name
    else:
        return None, None

#保存项目工商信息
def saveCompanyIndustyInfoToMongo(info):
    try:
        res = session.post(base_url + 'mongolog/projinfo', data=json.dumps(info),
                        headers={'Content-Type': 'application/json', 'token': token}).content
    except requests.exceptions.ProxyError:
        print '保存工商信息，链接失败，重试'
        time.sleep(5)
        saveCompanyIndustyInfoToMongo(info)
    except Exception:
        print '保存工商信息，链接失败，失败'
        pass
    else:
        res = json.loads(res)
        if res['code'] == 1000:
            pass
        elif res['code'] == 8001:
            pass
        else:
            print '错误数据indus_info----' + 'com_id=%s' % info['com_id']
            print res

#保存项目新闻信息列表
def saveCompanyNewsToMongo(newslist,com_id=None,com_name=None):
    for news in newslist:
        if news.get('linkurl'):
            news['com_id'] = com_id if isinstance(com_id, int) else int(com_id)
            news['com_name'] = com_name
            saverequest(url=(base_url + 'mongolog/projnews'), data=news, headers={'Content-Type': 'application/json', 'token': token})

#保存项目新闻信息
def saverequest(url, data , headers):
    try:
        res = session.post(url, data=json.dumps(data),headers=headers).content
    except requests.exceptions.ProxyError:
        print '保存新闻信息，链接失败，重试'
        time.sleep(5)
        saverequest(url, data, headers)
    except Exception:
        print '保存新闻信息，链接失败，失败'
        pass
    else:
        res = json.loads(res)
        if res['code'] == 1000:
            pass
        elif res['code'] == 8001:
            pass
        else:
            print '错误数据news----' + 'com_id=%s' % data['com_id']
            print res


#更新项目信息
def updateCompanyToMongo(info):
    try:
        res = session.post(base_url + 'mongolog/proj', data=json.dumps(info), headers={'Content-Type': 'application/json', 'token': token}).content
    except requests.exceptions.ProxyError:
        print '更新公司名称，链接失败，重试'
        time.sleep(5)
        updateCompanyToMongo(info)
    except Exception:
        print '更新公司名称，链接失败，跳过'
        pass
    else:
        res = json.loads(res)
        if res['code'] == 1000:
            pass
        elif res['code'] == 8001:
            pass
        else:
            print '错误数据' + 'com_id：%s' % str(info['com_id'])
            print res


#获取项目列表（从服务器mongo数据库获取）
def get_companglist(page_index):
    projlist = None
    res = session.get(base_url + 'mongolog/proj?page_size=10&sort=com_id&page_index=%s' % page_index, headers={'Content-Type': 'application/json', 'token': token})
    if res.status_code == 200:
        res = json.loads(res.content)
        if res['code'] == 1000:
            projlist = res['result']['data']
        else:
            print '获取全库项目列表有误----' + 'page_index=%s' % page_index
            print res
    return projlist


#保存项目投融资历史
def saveEventToMongo(events, com_id):
    for event in events:
        event['com_id'] = com_id
        res = session.post(base_url + 'mongolog/event', data=json.dumps(event),
                            headers={'Content-Type': 'application/json', 'token': token}).content
        res = json.loads(res)
        if res['code'] == 1000:
            print '新增invse--' + str(res['result'].get('invse_id', None))
        elif res['code'] == 8001:
            print '重复invest'
        else:
            print '错误event数据--%s'%repr(event)
            print res

#打开页面，获取html，解析，保存
def getpage(driver,com_id,wait):
    try:
        driver.get("https://www.itjuzi.com/company/%s" % com_id)
        time.sleep(1)
        page = driver.page_source
        resdic, com_name = parseHtml(page)
        if resdic:
            resdic['com_id'] = int(com_id)
            print com_name
            news = resdic['news']
            saveCompanyNewsToMongo(news, resdic['com_id'], com_name)
            saveCompanyIndustyInfoToMongo(resdic)
            saveEventToMongo(resdic['events'], resdic['com_id'])
            dic = {}
            dic['com_id'] = int(resdic.get('com_id'))
            dic['tags'] = resdic.get('tags', [])
            dic['com_web'] = resdic.get('com_web', None)
            dic['mobile'] = resdic.get('mobile', None)
            dic['email'] = resdic.get('email', None)
            dic['detailaddress'] = resdic.get('detailaddress', None)
            dic['com_name'] = com_name
            updateCompanyToMongo(dic)
        else:
            if com_name:
                if com_name in (u'找不到您访问的页面',):
                    print 'com_id:%s 未找到'%str(com_id)
                    print com_name
                elif com_name in (u'www.itjuzi.com', u'502 Bad Gateway',u'403'):
                    print '空页面--%s' % com_id
                    print '现在的时间是：%s' % datetime.datetime.now()
                    print '等待%s秒后重试' % wait
                    time.sleep(wait)
                    getpage(driver, com_id, wait)
                else:
                    print 'com_id:%s' % str(com_id)
                    print com_name
            else:
                print '空页面--%s' % com_id
    except TimeoutException:
        print '打开页面超时，公司：id--%s'%com_id
        getpage(driver, com_id, wait)


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://180.101.205.253:8888')
prefs={'profile.default_content_setting_values': {
        'images': 2,   #禁用图片
    }}
chrome_options.add_experimental_option('prefs',prefs)
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
driver.set_window_size('1280','800')
driver.get("https://www.itjuzi.com/user/login")
time.sleep(5)
print '正在输入账号...'
driver.find_element_by_xpath('//*[@id="create_account_email"]').send_keys("18616837957",)
print '正在输入密码...'
driver.find_element_by_xpath('//*[@id="create_account_password"]').send_keys("x81y0122",)
print '正在登录...'
driver.find_element_by_id('login_btn').click()

page_index = 7487
while page_index <= 12000:
    projlist = get_companglist(page_index)
    print '当前页码：page_index = %s' % str(page_index)
    print datetime.datetime.now()
    page_index += 1
    if projlist:
        for proj in projlist:
            com_id = proj['com_id']
            # com_id = 1556
            getpage(driver, com_id, 10)


driver.quit()




