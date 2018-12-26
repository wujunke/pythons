#coding=utf-8
import json
import datetime
import threading
import traceback

import requests
import time
from selenium import webdriver
import Tkinter as tk
from selenium.common.exceptions import TimeoutException
import sys
from parseHtml import parseComDetailHtml, parseComMemberByDriver, parseComFinanceByDriver, getComBasic, parseComIndustryInfoByDriver


token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
base_url = 'https://api.investarget.com/'


driver = None
isLogin = False
isCatch = False
window = tk.Tk()
width, height = 800, 700   # 窗口大小
screenwidth, screenheight = window.winfo_screenwidth(), window.winfo_screenheight()    # 屏幕大小
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
window.geometry(alignstr)
window.title = '盈钛爬虫'
reload(sys)
sys.setdefaultencoding('utf-8')

session = requests.Session()
session.trust_env = False



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
    res = session.get(base_url + 'mongolog/proj?page_size=10&sort='
                                 '&page_index=%s&com_name=...' % page_index,
                      headers={'Content-Type': 'application/json', 'token': token})
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
            consoleRes('新增invse--' + str(res['result'].get('invse_id', res['result'].get('merger_id', None))))
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
    proxy = vars_proxy.get()
    if proxy:
        proxy = proxy.replace(' ', '')
    try:
        driver.get("https://www.itjuzi.com/company/%s" % com_id)
        time.sleep(wait)
        page = driver.page_source
        resdic, com_name, full_name = parseComDetailHtml(page)
        if resdic:
            resdic['com_id'] = int(com_id)
            consoleRes(com_name)
            news = resdic['news']
            saveCompanyNewsToMongo(news, resdic['com_id'], com_name)

            eventlist = parseComFinanceByDriver(driver)
            indus_member = parseComMemberByDriver(driver)
            saveEventToMongo(eventlist, resdic['com_id'])

            basicDic = getComBasic(driver, com_id)
            resdic.update(basicDic)

            industryInfoDic = parseComIndustryInfoByDriver(driver, com_id, proxy)
            industryInfoDic['indus_member'] = indus_member

            updateCompanyToMongo(resdic)
            saveCompanyIndustyInfoToMongo(industryInfoDic)
        else:
            if com_name:
                if com_name in (u'找不到您访问的页面',u'IT桔子 | 泛互联网创业投资项目信息数据库及商业信息服务商'):
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
        consoleRes('打开页面超时，跳过公司：id--%s'%com_id)




def consoleRes(res):
    global consoleText
    consoleText.insert(tk.END, res + '\n')
    consoleText.update()


def openWeb():
    global driver
    if not driver:
        proxy = vars_proxy.get()
        if proxy:
            proxy = proxy.replace(' ', '')
        chrome_options = webdriver.ChromeOptions()
        if proxy and len(proxy) > 0:
            chrome_options.add_argument('--proxy-server=http://%s' % proxy)
        driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
        driver.set_window_size('1280', '800')
        consoleRes('正在打开网站...')
        driver.get("https://www.itjuzi.com/login?url=%2F")
        consoleRes('网页加载完成')
    else:
        consoleRes('重新启动浏览器')

def login():
    global isLogin
    if driver:
        if not isLogin:
            consoleRes('正在输入账号...')
            account = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/div[1]/input')
            accountstr = vars_account.get()
            account.send_keys(accountstr)
            time.sleep(1)
            consoleRes('正在输入密码...')
            paswd = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/div[2]/input')
            passwordstr = vars_password.get()
            paswd.send_keys(passwordstr)
            time.sleep(1)
            consoleRes('正在登录...')
            driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/button').click()
            time.sleep(2)
            isLogin = True
        else:
            consoleRes('已登录')
    else:
        consoleRes('浏览器未启动')


def start():
    global driver, isCatch, isLogin
    if driver:
        if isLogin:
            isCatch = True
            t = threading.Thread(target=catchHtml)
            t.setDaemon(True)
            t.start()
            consoleRes('开始爬取网页内容')
        else:
            consoleRes('未登录')
    else:
        consoleRes('浏览器未启动')


def catchHtml():
    global isCatch, driver
    sleeptime = vars_catchTime.get()
    try:
        page_index = 1
        while isCatch:
            projlist = get_companglist(1)
            consoleRes('当前页码：page_index = %s' % str(page_index))
            print(datetime.datetime.now())
            page_index += 1
            if projlist:
                for proj in projlist:
                    com_id = proj['com_id']
                    getpage(driver, com_id, float(sleeptime))
        consoleRes('结束抓取')
    except Exception:
        consoleRes('抓取出错')


def stop():
    global driver, isCatch
    if driver:
        isCatch = False
        consoleRes('当前页爬取完成结束爬取')
    else:
        consoleRes('浏览器未启动')

def close():
    global driver, isCatch
    driver.quit()
    driver = None
    isCatch = False
    consoleRes('已关闭浏览器')



def creatOneEntry(text, point, w):
    x = point[0]
    y = point[1]
    tk.Label(window, text=text).place(x=x, y=y)
    var_iuput = tk.StringVar()
    tk.Entry(window, textvariable=var_iuput).place(x=x + 140, y=y, w=w, h=25)
    return var_iuput




tk.Button(window, text="打开网页", font=("Arial", 20), command=openWeb).place(x=50, y=50, w=150, h=50)
tk.Button(window, text="登录", font=("Arial", 20), command=login).place(x=50, y=100, w=150, h=50)
tk.Button(window, text="开始爬取", font=("Arial", 20), command=start).place(x=50, y=150, w=150, h=50)
tk.Button(window, text="结束爬取", font=("Arial", 20), command=stop).place(x=50, y=200, w=150, h=50)
tk.Button(window, text="关闭网页", font=("Arial", 20), command=close).place(x=50, y=250, w=150, h=50)
tk.Label(window, text='程序输出', font=("Arial", 16)).place(x=400, y=70)
consoleText = tk.Text(window, bg='gray')
consoleText.place(x=430, y=100, w=300, h=500)
vars_catchTime = creatOneEntry('爬取间隔（单位：秒）', (50 , 330), 30)
vars_catchTime.set(5)
vars_proxy = creatOneEntry('网络代理', (50 , 360), 200)
# vars_proxy.set('221.6.201.18:9999')
vars_account = creatOneEntry('账号', (50 , 390), 200)
vars_account.set('18964687678')
vars_password = creatOneEntry('密码', (50 , 420), 200)
vars_password.set('123456789')


window.mainloop()
