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


session = requests.Session()
session.trust_env = False

def rand_proxie():
    return {'http':'http://%s' % iplist[random.randint(0, len(iplist)) - 1],}



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
        if name:
            com_name = name.text.replace(u'\t', u'')
            com_name = com_name.split('\n')[1]
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
                                infolist.append(infodic)
                        response[tabhref] = infolist
        return response, com_name
    else:
        return None, None


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


def saveCompanyNewsToMongo(newslist,com_id=None,com_name=None):
    for news in newslist:
        if news.get('linkurl'):
            news['com_id'] = com_id if isinstance(com_id, int) else int(com_id)
            news['com_name'] = com_name
            saverequest(url=(base_url + 'mongolog/projnews'), data=news, headers={'Content-Type': 'application/json', 'token': token})
            # res = requests.post(base_url + 'mongolog/projnews', data=json.dumps(news),
            #                     headers={'Content-Type': 'application/json', 'token': token}).content
            # res = json.loads(res)
            # if res['code'] == 1000:
            #     pass
            # elif res['code'] == 8001:
            #     pass
            # else:
            #     print '错误数据news----' + 'com_id=%s' % news['com_id']
            #     print res

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



def get_companglist(page_index):
    projlist = None
    res = session.get(base_url + 'mongolog/proj?page_size=10&sort=true&page_index=%s' % page_index, headers={'Content-Type': 'application/json', 'token': token})
    if res.status_code == 200:
        res = json.loads(res.content)
        if res['code'] == 1000:
            projlist = res['result']['data']
        else:
            print '获取全库项目列表有误----' + 'page_index=%s' % page_index
            print res
    return projlist



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
                    print '新增org_invest--' + str(res['result'].get('id', None))
                elif res['code'] == 5007:
                    print '重复org_invest'
                else:
                    print '错误org_invest数据--%s'%repr(res)
                    print res



def getpage(driver,com_id,wait):
    try:
        driver.get("https://www.itjuzi.com/company/%s" % com_id)
        time.sleep(random.randint(5, 8))
        page = driver.page_source
        resdic, com_name = parseHtml(page)
        if resdic:
            resdic['com_id'] = int(com_id)
            print com_name
            news = resdic['news']
            saveCompanyNewsToMongo(news, resdic['com_id'], com_name)
            saveCompanyIndustyInfoToMongo(resdic)
            saveEventToMongo(resdic['events'], resdic['com_id'])
            # saveEventToMySqlOrg(resdic['events'], resdic['com_id'], com_name, resdic['industryType'])
            # dic = {}
            # dic['com_id'] = int(resdic.get('com_id'))
            # dic['tags'] = resdic.get('tags', [])
            # dic['com_web'] = resdic.get('com_web', None)
            # dic['mobile'] = resdic.get('mobile', None)
            # dic['email'] = resdic.get('email', None)
            # dic['detailaddress'] = resdic.get('detailaddress', None)
            # dic['com_name'] = com_name
            # updateCompanyToMongo(dic)
            # time.sleep(random.randint(3, 5))
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
                # print '现在时间：%s' % datetime.datetime.now()
                # print '等待%s秒后重试'%wait
                # time.sleep(wait)
                # getpage(driver,com_id,wait)
    except TimeoutException:
        print '打开页面超时，公司：id--%s'%com_id
        getpage(driver, com_id, wait)

# desired_capabilities = dict(DesiredCapabilities.PHANTOMJS)
# desired_capabilities["phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 Safari/537.36'
# desired_capabilities["phantomjs.page.settings.loadImages"] = False
# driver = webdriver.PhantomJS('/Users/investarget/wxNLP-env/selenium/webdriver/phantomjs-2.1.1-macosx/bin/phantomjs', desired_capabilities=desired_capabilities,service_args=['--ssl-protocol=any','--ignore-ssl-errors=true'])

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://112.115.57.20:3128')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)

# driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', )

driver.set_window_size('1280','800')
print '正在打开网站...'
driver.get("https://www.itjuzi.com/user/login")
# driver.get('https://www.itjuzi.com/user/login?redirect=index.php?m=bbs?phpSessId=983d31fb953dc8a76973e6ec6a44cdfff234fd6c%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%83%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%83%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%82%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%A3%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%83%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%82%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%82%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%80%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%83%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%82%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%82%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%81?phpSessId=10876e213c50e234d56347a680d1391fc18168e6?phpSessId=e0722e635a688a9fe548ec78d5f40756b9e435c5?phpSessId=ac390ac897bfe517b50b2b014f75f5f4370b359a?phpSessId=dcbe021bdd12f6743f9c9ca3b49bc551529fb22b?phpSessId=94bf36bed7eaa3fc1deb805f6e8b71b0d3344672?phpSessId=b081aba40b934e50d83acd786e3b2626cf51afc2')
time.sleep(5)
print '正在输入账号...'
account = driver.find_element_by_xpath('//*[@id="create_account_email"]')
account.click()
account.send_keys("18616837957",)
print '正在输入密码...'
paswd = driver.find_element_by_xpath('//*[@id="create_account_password"]')
paswd.send_keys("x81y0122",)
print '正在登录...'
driver.find_element_by_id('login_btn').click()



page_index = 5411
while page_index <= 10000:
    projlist = get_companglist(page_index)

    print '当前页码：page_index = %s' % str(page_index)
    print datetime.datetime.now()
    page_index += 1
    if projlist:
        for proj in projlist:
            com_id = proj['com_id']
            # com_id = 17481
            getpage(driver, com_id, 10)


driver.quit()


# def startdriver(page_index, proxy_ip):
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument('--proxy-server=http://%s' % proxy_ip)
#     driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
#
#     # driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', )
#
#     driver.set_window_size('1280', '800')
#     print '正在打开网站...'
#     driver.get("https://www.itjuzi.com/user/login")
#     # driver.get('https://www.itjuzi.com/user/login?redirect=index.php?m=bbs?phpSessId=983d31fb953dc8a76973e6ec6a44cdfff234fd6c%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%83%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%83%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%82%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%A3%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%83%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%82%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%82%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%80%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%83%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%82%C3%83%C2%83%C3%82%C2%83%C3%83%C2%82%C3%82%C2%82%C3%83%C2%83%C3%82%C2%82%C3%83%C2%82%C3%82%C2%81?phpSessId=10876e213c50e234d56347a680d1391fc18168e6?phpSessId=e0722e635a688a9fe548ec78d5f40756b9e435c5?phpSessId=ac390ac897bfe517b50b2b014f75f5f4370b359a?phpSessId=dcbe021bdd12f6743f9c9ca3b49bc551529fb22b?phpSessId=94bf36bed7eaa3fc1deb805f6e8b71b0d3344672?phpSessId=b081aba40b934e50d83acd786e3b2626cf51afc2')
#     time.sleep(5)
#     print '正在输入账号...'
#     account = driver.find_element_by_xpath('//*[@id="create_account_email"]')
#     account.click()
#     account.send_keys("18616837957", )
#     print '正在输入密码...'
#     paswd = driver.find_element_by_xpath('//*[@id="create_account_password"]')
#     paswd.send_keys("x81y0122", )
#     print '正在登录...'
#     driver.find_element_by_id('login_btn').click()
#     res = False
#     while page_index <= 10000:
#         projlist = get_companglist(page_index)
#
#         print '当前页码：page_index = %s' % str(page_index)
#         print datetime.datetime.now()
#         page_index += 1
#         if projlist:
#             for proj in projlist:
#                 com_id = proj['com_id']
#                 res = getpage(driver, com_id, 2)
#                 if res:
#                     driver.quit()
#                     return page_index - 1
#
#
# page_index = 1050
# for ip in proxy_iplist:
#     page_index = startdriver(page_index, ip)




