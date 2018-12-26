#coding=utf-8
import threading

import requests
from bs4 import BeautifulSoup
import sys
import time, json
from selenium import webdriver
import Tkinter as tk

driver = None
isRun = False
isCatch = False
window = tk.Tk()
window.title = '盈钛爬虫'
width, height = 800, 700   # 窗口大小
screenwidth, screenheight = window.winfo_screenwidth(), window.winfo_screenheight()    # 屏幕大小
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
window.geometry(alignstr)


reload(sys)
sys.setdefaultencoding('utf-8')


base_url = 'https://api.investarget.com/'
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'



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
            'com_name': tds[1].find('a', class_='target').text + '...',
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
            consoleRes('新增com--' + str(res['result'].get('com_id', None)))
        elif res['code'] == 8001:
            pass
        else:
            consoleRes('错误com数据--%s' % repr(com))
            print(res)


def nextPage():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    nextbutton = driver.find_element_by_css_selector('#table > ul > li:nth-child(8) > a')
    nextbutton.click()
    html = driver.page_source
    comlist = parseHtml(html)
    saveComList(comlist)

def consoleRes(res):
    global consoleText
    consoleText.insert(tk.END, res + '\n')
    consoleText.update()


def openWeb():
    global driver, isRun
    if not driver:
        driver = webdriver.Chrome('/usr/local/bin/chromedriver')
        driver.set_window_size('1280', '800')
        consoleRes('正在打开网站...')
        driver.get('http://radar.itjuzi.com/company')
        consoleRes('网页加载完成')

    else:
        consoleRes('重新启动浏览器')

def start():
    global isRun, driver, isCatch
    if driver:
        if not isRun:
            isRun = True
            isCatch = True
            t = threading.Thread(target=catchHtml)
            t.setDaemon(True)
            t.start()
            consoleRes('开始爬取网页内容')
    else:
        consoleRes('浏览器未启动')


def catchHtml():
    global isCatch
    sleeptime = vars_catchTime.get()
    try:
        html = driver.page_source
        comDict = parseHtml(html)
        saveComList(comDict)
        i = 1
        while isCatch:
            i += 1
            consoleRes('抓取page-%s' % i)
            nextPage()
            time.sleep(int(sleeptime))
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
    global driver, isRun, isCatch
    driver.quit()
    driver = None
    isCatch = False
    isRun = False
    consoleRes('已关闭浏览器')



def creatOneEntry(text, point):
    x = point[0]
    y = point[1]
    tk.Label(window, text=text).place(x=x, y=y)
    var_iuput = tk.StringVar()
    tk.Entry(window, textvariable=var_iuput).place(x=x + 140, y=y, w=60, h=25)
    return var_iuput


vars_catchTime = creatOneEntry('爬取间隔（单位：秒）', (50 , 300))
vars_catchTime.set(5)
tk.Button(window, text="打开网页", font=("Arial", 20), command=openWeb).place(x=50, y=50, w=150, h=50)
tk.Button(window, text="开始爬取", font=("Arial", 20), command=start).place(x=50, y=100, w=150, h=50)
tk.Button(window, text="结束爬取", font=("Arial", 20), command=stop).place(x=50, y=150, w=150, h=50)
tk.Button(window, text="关闭网页", font=("Arial", 20), command=close).place(x=50, y=200, w=150, h=50)
tk.Label(window, text='程序输出', font=("Arial", 16)).place(x=400, y=70)
consoleText = tk.Text(window, bg='gray')
consoleText.place(x=430, y=100, w=300, h=500)

window.mainloop()