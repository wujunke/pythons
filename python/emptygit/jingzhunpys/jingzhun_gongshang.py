#coding=utf-8
import json

import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup

base_url = 'https://api.investarget.com/'
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
headers = {'Content-Type': 'application/json', 'token': token}

saltfactor = 111234567890


def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    source = soup.find('div', class_='main')
    base_info_element = source.find('div', class_='base-info')
    partner_info_element = source.find('div', class_='partner-info')
    employ_info_element = source.find('div', class_='employ-info')
    record_info_element = source.find('div', class_='record-info')
    base_info = []
    base_info_divs = base_info_element.find_all('div', class_='group')
    for base_info_div in base_info_divs:
        describe = base_info_div.find('div', class_='describe').text
        content = base_info_div.find('span', class_='ng-binding').text
        base_info.append({describe: content})

    partner_info = []
    partner_info_divs = partner_info_element.find_all('div', class_='group ng-scope')
    for partner_info_div in partner_info_divs:
        describe = partner_info_div.find('div', class_='describe').text
        content = partner_info_div.find('span', class_='ng-binding').text
        partner_info.append({describe: content})

    employ_info = []
    employ_info_divs = employ_info_element.find_all('div', class_='group ng-scope')
    for employ_info_div in employ_info_divs:
        describe = employ_info_div.find('div', class_='describe').text
        content = employ_info_div.find('span', class_='ng-binding').text
        employ_info.append({describe: content})

    record_info = []
    record_info_table = record_info_element.find('table')
    if record_info_table['class'] =='ng-hide':
        pass
    else:
        table_header = []
        table_header_tr = record_info_table.find('tr')
        table_header_tds = table_header_tr.find_all('td')
        for td in table_header_tds:
            table_header.append(td.text)
        table_trs = record_info_table.find_all('tr', class_='ng-scope')
        for table_tr in table_trs:
            tds = table_tr.find_all('td')
            record_one = {}
            record_one[table_header[0]] = tds[0].text + tds[2].text
            # record_one[table_header[1]] = tds[2].text
            record_one[table_header[2]] = tds[4].text
            record_one[table_header[3]] = tds[6].text

            record_info.append(record_one)

    res = {
        'base': base_info,
        'partner': partner_info,
        'employ': employ_info,
        'record': record_info,
    }
    return res




def getJingZhunCom_id(page):
    url = base_url + 'mongolog/proj?source=2&page_index=%s' % page
    res = requests.get(url, headers=headers).content
    res = json.loads(res)
    result = res['result']
    data = result['data']
    if len(data) > 0:
        return data
    return []





chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://49.84.151.217:4216')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)


driver.set_window_size('1280','800')
print '正在打开网站...'
driver.get("https://passport.36kr.com/pages/?ok_url=https%3A%2F%2Frong.36kr.com%2F#/login")
time.sleep(5)
print '正在输入账号...'
account = driver.find_element_by_id('kr-shield-username')
account.click()
account.send_keys("18637760716",)
print '正在输入密码...'
paswd = driver.find_element_by_id('kr-shield-password')
paswd.send_keys("123921013le",)
print '正在登录...'
driver.find_element_by_id('kr-shield-submit').click()




def getGongShang(driver, jingzhun_id):
    time.sleep(10)
    js= 'window.open("https://rong.36kr.com/commercial/%s");' % jingzhun_id
    driver.execute_script(js)

    handles = driver.window_handles # 获取当前窗口句柄集合（列表类型）
    driver.switch_to.window(handles[1])

    html = driver.page_source

    res = parseHtml(html)




    driver.close()
    driver.switch_to.window(handles[0])
    return res






def saveCompanyIndustyInfoToMongo(info):
    try:
        res = requests.post(base_url + 'mongolog/projinfo', data=json.dumps(info),
                        headers=headers).content
    except requests.exceptions.ProxyError:
        print '保存工商信息，链接失败，重试'
        time.sleep(5)
        saveCompanyIndustyInfoToMongo(info)
    except Exception:
        print '保存工商信息，链接失败，失败'
        pass
    else:
        res = json.loads(res)
        if res['code'] != 1000 and res['code'] != 8001:
            print '错误数据indus_info----' + 'com_id=%s' % info['com_id']
            print res



for i in range(0, 100):
    i += 1
    projlist =  getJingZhunCom_id(page=i)
    for proj in projlist:
        jingzhunid = int(proj['com_id']) - saltfactor

        info = getGongShang(driver=driver, jingzhun_id=jingzhunid)
        info['com_id'] = int(proj['com_id'])
        saveCompanyIndustyInfoToMongo(info)








driver.quit()