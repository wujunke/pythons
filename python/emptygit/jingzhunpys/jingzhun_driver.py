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






chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=http://211.161.103.247:9999')
prefs={
     'profile.default_content_setting_values': {
        'images': 2,   #禁用图片
    }
}
chrome_options.add_experimental_option('prefs',prefs)
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)
driver.set_window_size('1280','800')
driver.get("https://passport.36kr.com/pages/?ok_url=https%3A%2F%2Frong.36kr.com%2Flist%2Fdetail%26%3FsortField%3DHOT_SCORE#/login")
time.sleep(5)
print '正在输入账号...'
driver.find_element_by_xpath('//*[@id="kr-shield-username"]').send_keys("wjk1397@126.com",)
print '正在输入密码...'
driver.find_element_by_xpath('//*[@id="kr-shield-password"]').send_keys("123456",)
print '正在登录...'
driver.find_element_by_xpath('//*[@id="kr-shield-submit"]').click()

time.sleep(3)
def searchCompanyName(com_name):
    # driver.find_element_by_xpath('/html/body/header/div/div[1]/div/span/input').send_keys(com_name)

    if not isinstance(com_name, unicode):
        com_name = com_name.decode('utf-8')

    driver.find_element_by_css_selector('body > header > div > div:nth-child(1) > div > span > input').send_keys(com_name)
    # driver.find_element_by_xpath('/html/body/header/div/div[1]/div/span/span').click()
    driver.find_element_by_css_selector('body > header > div > div:nth-child(1) > div > span > span').click()
    time.sleep(5)

    try:
        first_com = driver.find_element_by_xpath('//*[@id="searchResult"]/table/tbody/tr[2]/td[1]/div/div[1]/span')
        first_com.click()
        html = driver.page_source
        parseComHtml(html)
        print html
    except Exception:
        pass
    else:
        for i in range(2, 4):
            xpath = '//*[@id="cloumn3ProjectList"]/ul/li[%s]' % i
            try:
                com = driver.find_element_by_xpath(xpath)
                com.click()
                time.sleep(3)
                html = driver.page_source
                parseComHtml(html)
                print html
            except Exception:
                break




def parseComHtml(com_html):
    pass


def saveCom(com_data):
    pass

searchCompanyName('爬藤网')





# driver.find_element_by_css_selector('body > header > div > div:nth-child(7) > div > div > pane-trigger > img').click()
# driver.quit()