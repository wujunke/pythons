#coding=utf-8
import json
import random


import datetime
import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver

import sys


reload(sys)
sys.setdefaultencoding('utf-8')

session = requests.Session()
session.trust_env = False



chrome_options = webdriver.ChromeOptions()
proxy = '60.191.201.38:45461'
chrome_options.add_argument('--proxy-server=http://%s' % proxy)
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
driver.set_window_size('1280','800')
print('正在打开网站...')
driver.get("https://itjuzi.com/login?url=%2Finvestfirm")
time.sleep(5)
print('正在输入账号...')
account = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/div[1]/input')
account.click()
account.send_keys("wjk1397@163.com",)
# account.send_keys("18964687678",)
time.sleep(1)
print('正在输入密码...')
paswd = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/div[2]/input')
paswd.send_keys("Aa123456")
# paswd.send_keys("123456789")
time.sleep(1)
print('正在登录...')
driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div/form/button').click()
time.sleep(5)




def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    comtable = soup.find('div', class_='juzi-table')
    alltrs = comtable.find('tbody').find_all('tr')
    comDict = []


    for tr in alltrs:
        tds = tr.find_all('td')
        comleftdata = {
            'org_name': tds[1].text,
            'url': 'https://itjuzi.com/' + tds[4].find('a').get('href')
        }
        comDict.append(comleftdata)
    return comDict


def nextPage():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    nextbutton = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[3]/div[1]/div[4]/ul/li[8]/a')
    nextbutton.click()
    html = driver.page_source
    comlist = parseHtml(html)
    print('保存page————', i)
    saveComList(comlist)



def saveComList(comDict):
    with open('org.json', 'a') as f:
        for org in comDict:
            f.write(json.dumps(org))
            f.write('\n')


# driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[3]/div[1]/div/div[1]/div/div/ul/li[3]/a').click()
driver.get('https://itjuzi.com/investfirm')
time.sleep(5)
locationout = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[3]/div[1]/div[2]/div[3]/div[1]/div[2]/span[3]')
locationout.click()
time.sleep(5)
html = driver.page_source


comDict = parseHtml(html)
saveComList(comDict)


for i in range(2, 63):
    time.sleep(5)
    nextPage()
