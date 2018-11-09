#coding=utf-8
import json

import requests
import time
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import sys

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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



def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser')

    comtable = soup.find('div', class_='juzi-table')

    alltrs = comtable.find('tbody').find_all('tr')

    comDict = []


    for tr in alltrs:
        tds = tr.find_all('td')
        comleftdata = {
            'com_id': tds[9].find('a').get('href').replace(u'/company/', u''),
            'com_logo_archive': tds[1].find('img').get('src', ''),
            'com_name': tds[1].find('span').text + '...',
            'com_des': tds[1].find('div', class_='onehang').text,
            'com_cat_name': tds[2].text,
            'invse_total_money': tds[4].text,
            'invse_round_id': tds[3].text,
        }
        comDict.append(comleftdata)
    return comDict

def saveComList(comDict):
    for com in comDict:
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
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    nextbutton = driver.find_element_by_css_selector('#table > ul > li:nth-child(8) > a')
    nextbutton.click()
    html = driver.page_source
    comlist = parseHtml(html)
    saveComList(comlist)





chrome_options.add_experimental_option('prefs',prefs)
chrome_options.add_argument('--proxy-server=http://221.6.201.18:9999')
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
print('正在输入密码...')
paswd = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/div[2]/input')
# paswd.send_keys("x81y0122",)
paswd.send_keys("123456789")
print('正在登录...')
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/button').click()

driver.get('http://radar.itjuzi.com/company')
time.sleep(5)
i = 1
html = driver.page_source
comDict = parseHtml(html)
saveComList(comDict)
while True:
    i += 1
    print('page-%s' % i)
    nextPage()



