#coding=utf-8
import json

import requests
import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


base_url = 'https://api.investarget.com/'
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'

chrome_options = webdriver.ChromeOptions()
prefs={
     'profile.default_content_setting_values': {
        'images': 2,   #禁用图片
        # 'javascript':2   #禁用JS
    }
}
chrome_options.add_experimental_option('prefs',prefs)
# chrome_options.add_argument('--proxy-server=http://114.113.126.82:80')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
driver.set_window_size('1280','800')
print('正在打开网站...')
driver.get("https://www.itjuzi.com/user/login")
time.sleep(5)
print('正在输入账号...')
account = driver.find_element_by_xpath('//*[@id="create_account_email"]')
account.click()
# account.send_keys("18616837957",)
account.send_keys("18964687678",)
print('正在输入密码...')
paswd = driver.find_element_by_xpath('//*[@id="create_account_password"]')
# paswd.send_keys("x81y0122",)
paswd.send_keys("123456789")
print('正在登录...')
driver.find_element_by_id('login_btn').click()



def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser')

    comlistbox = soup.find('div', class_='company-list-box')

    leftbox = comlistbox.find('div', class_='company-list-left')

    comDict = {}

    leftlis = leftbox.find_all('li',)
    for li in leftlis:
        if li.get('data-id'):
            comleftdata = {
                'com_id': li.get('data-id', ''),
                'com_logo_archive': li.find('img').get('src', ''),
                'com_name': li.find_all('a')[1].text + '...',
                'com_des': li.find('p', class_='des').text,
            }
            comDict[li.get('data-id')] = comleftdata

    infobox = comlistbox.find('div', class_='company-list-info')
    infolis = infobox.find_all('li', )
    for li in infolis:
        if li.get('data-id'):
            infodivs = li.find_all('div')
            latestround = infodivs[2].find_all('span')
            cominfodata = {
                'com_cat_name': infodivs[0].text,
                'com_sub_cat_name': infodivs[1].text,
                'invse_total_money': infodivs[3].text,
                'guzhi': infodivs[4].text,
                'com_addr': infodivs[5].text,
                'com_born_date': infodivs[6].text,
                'com_status': infodivs[7].text,
                'com_scale': infodivs[8].text,
                'invse_date': latestround[0].text,
                'invse_round_id': latestround[1].text,
                'invse_detail_money': latestround[2].text,
            }
            comDict[li.get('data-id')].update(cominfodata)
    return comDict

def saveComList(comDict):
    for key, com in comDict.items():
        res = requests.post(base_url + 'mongolog/proj', data=json.dumps(com),
                            headers={'Content-Type': 'application/json', 'token': token}).content
        res = json.loads(res)
        if res['code'] == 1000:
            print('新增com--' + str(res['result'].get('com_id', None)))
        elif res['code'] == 8001:
            pass
        else:
            print('错误com数据--%s' % repr(com))
            print(res)

def nextPage():
    driver.find_element_by_xpath('//*[@id="page-selection"]/ul/li[13]/a').click()
    html = driver.page_source
    comlist = parseHtml(html)
    saveComList(comlist)




driver.get('http://radar.itjuzi.com/company')
html = driver.page_source
comDict = parseHtml(html)
saveComList(comDict)
while True:
    nextPage()



