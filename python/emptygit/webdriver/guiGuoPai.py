#coding=utf-8
import threading
import traceback

import pyautogui as pg
import time, datetime, os, json
from PIL import ImageGrab
from aip import AipOcr
from selenium import webdriver
try:
    import sys
    import Tkinter as tk
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    pass
except ImportError:
    import tkinter as tk

driver = None
isMoni = True
window = tk.Tk()
width, height = 800, 700   # 窗口大小
screenwidth, screenheight = window.winfo_screenwidth(), window.winfo_screenheight()    # 屏幕大小
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
window.geometry(alignstr)


APP_ID = '11546435'
API_KEY = 'w9646O4Ug0H2XNwXQX0WLcen'
SECRET_KEY = '4kPgOiOsSGH35asD1ifi3SzBgniLY00u'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
sleeptime = 0.01  #鼠标反应时间


url_moni = 'http://moni.51hupai.org/'
url_guopai = ''
driverPath = os.path.join(os.getcwd(), 'IEDriverServer.exe')



def openMoNiWeb():
    global driver, isMoni
    isMoni = True
    # if not driver:
    #     driver = webdriver.Ie(executable_path=driverPath)
    #     driver.set_window_position(0, 0)
    #     driver.set_window_size(950, 950)
    #     driver.get(url_moni)
    # else:
    #     driver.get(url_moni)
    consoleRes('打开- %s -网页' % ('模拟程序' if isMoni else '真实程序'))

def openGuoPaiWeb():
    global driver, isMoni
    isMoni = False
    # if not driver:
    #     driver = webdriver.Ie(executable_path=driverPath)
    #     driver.set_window_position(0, 0)
    #     driver.set_window_size(950, 950)
    #     driver.get(url_guopai)
    # else:
    #     driver.get(url_guopai)
    consoleRes('打开- %s -网页' % ('模拟程序' if isMoni else '真实程序'))


def refreshWeb():
    global driver
    if driver:
        driver.refresh()
        consoleRes('刷新- %s -网页' % ('模拟程序' if isMoni else '真实程序'))

def closeWeb():
    global driver
    if driver:
        driver.quit()
        driver = None
        consoleRes('关闭- %s -网页' % ('模拟程序' if isMoni else '真实程序'))

tk.Button(window, text="打开模拟网页", command=openMoNiWeb).place(x=50)
tk.Button(window, text="打开国拍网页", command=openGuoPaiWeb).place(x=200)
tk.Button(window, text="刷新网页", command=refreshWeb).place(x=50, y=40)
tk.Button(window, text="关闭网页", command=closeWeb).place(x=200, y=40)


def creatPoint(text, point, separatorChar=','):
    x = point[0]
    y = point[1]
    tk.Label(window, text=text).place(x=x, y=y)
    var_iuput_x = tk.IntVar()
    var_iuput_y = tk.IntVar()
    tk.Entry(window, textvariable=var_iuput_x).place(x=x + 140, y=y, w=50, h=25)
    tk.Label(window, text=separatorChar).place(x=x + 190, y=y, w=10)
    tk.Entry(window, textvariable=var_iuput_y).place(x=x + 200, y=y, w=50, h=25)
    return var_iuput_x, var_iuput_y

def creatTime(text, point, separatorChar=','):
    x = point[0]
    y = point[1]
    tk.Label(window, text=text).place(x=x, y=y)
    var_iuput_x = tk.StringVar()
    var_iuput_y = tk.StringVar()
    tk.Entry(window, textvariable=var_iuput_x).place(x=x + 140, y=y, w=50, h=25)
    tk.Label(window, text=separatorChar).place(x=x + 190, y=y, w=10)
    tk.Entry(window, textvariable=var_iuput_y).place(x=x + 200, y=y, w=50, h=25)
    return var_iuput_x, var_iuput_y

def creatImage(text, point):
    x = point[0]
    y = point[1]
    tk.Label(window, text=text).place(x=x, y=y)
    var_iuput_x1 = tk.IntVar()
    var_iuput_y1 = tk.IntVar()
    var_iuput_x2 = tk.IntVar()
    var_iuput_y2 = tk.IntVar()
    tk.Entry(window, textvariable=var_iuput_x1).place(x=x + 140, y=y, w=50, h=25)
    tk.Label(window, text=',').place(x=x + 190, y=y, w=10)
    tk.Entry(window, textvariable=var_iuput_y1).place(x=x + 200, y=y, w=50, h=25)
    tk.Label(window, text=',').place(x=x + 250, y=y, w=10)
    tk.Entry(window, textvariable=var_iuput_x2).place(x=x + 260, y=y, w=50, h=25)
    tk.Label(window, text=',').place(x=x + 310, y=y, w=10)
    tk.Entry(window, textvariable=var_iuput_y2).place(x=x + 320, y=y, w=50, h=25)
    return var_iuput_x1, var_iuput_y1, var_iuput_x2, var_iuput_y2

def creatOneEntry(text, point):
    x = point[0]
    y = point[1]
    tk.Label(window, text=text).place(x=x, y=y)
    var_iuput = tk.StringVar()
    tk.Entry(window, textvariable=var_iuput).place(x=x + 140, y=y, w=60, h=25)
    return var_iuput

def creatTwoEntry(text, point):
    x = point[0]
    y = point[1]
    tk.Label(window, text=text).place(x=x, y=y)
    var_iuput_1 = tk.StringVar()
    var_iuput_2 = tk.StringVar()
    tk.Label(window, text='快版').place(x=x + 140, y=y, w=25)
    tk.Entry(window, textvariable=var_iuput_1).place(x=x + 170, y=y, w=50, h=25)
    tk.Label(window, text='慢版').place(x=x + 230, y=y, w=25)
    tk.Entry(window, textvariable=var_iuput_2).place(x=x + 260, y=y, w=50, h=25)
    return var_iuput_1, var_iuput_2




tk.Label(window, text='元素定位', font=("Arial", 16), ).place(y=70)
x1, y1 = 50, 100
var_customUpPriceIuput_x, var_customUpPriceIuput_y = creatPoint('自定义加价输入框', (x1, y1 + 40 * 0))
var_customUpPriceButton_x, var_customUpPriceButton_y = creatPoint('自定义加价按钮', (x1, y1 + 40 * 1))
var_offerButton_x, var_offerButton_y = creatPoint('出价按钮', (x1, y1 + 40 * 2))
var_currentPriceImage_x1, var_currentPriceImage_y1, var_currentPriceImage_x2, var_currentPriceImage_y2 = \
    creatImage('当前出价图片', (x1, y1 + 40 * 3))
var_rightPriceImage_x1, var_rightPriceImage_y1, var_rightPriceImage_x2, var_rightPriceImage_y2 = \
    creatImage('最低成交价图片', (x1, y1 + 40 * 4))
var_biggestPriceImage_x1, var_biggestPriceImage_y1, var_biggestPriceImage_x2, var_biggestPriceImage_y2 = \
    creatImage('最高可接受价图片', (x1, y1 + 40 * 5))
var_YZMSureButton_x, var_YZMSureButton_y = creatPoint('验证码确定按钮', (x1, y1 + 40 * 6))

x2, y2 = x1, y1 + 40 * 6 + 30
tk.Label(window, text='出价策略', font=("Arial", 16), ).place(y=y2)
var_basetime_h, var_basetime_m = creatTime('基础时间', (x2, y2 + 30 * 1), ':')
var_startTime = creatOneEntry('开始检测时间', (x2, y2 + 30 * 2))
var_upTime_fast, var_upTime_slow = creatTwoEntry('出价时间', (x2, y2 + 30 * 3))
var_upPrice_fast, var_upPrice_slow = creatTwoEntry('出价加价', (x2, y2 + 30 * 4))
var_checkPrice = creatOneEntry('验证差价', (x2, y2 + 30 * 5))
var_sureOfferTime_fast, var_sureOfferTime_slow = creatTwoEntry('最早提交出价时间', (x2, y2 + 30 * 6))
var_latestSureOfferTime_fast, var_latestSureOfferTime_slow = creatTwoEntry('最晚提交出价时间', (x2, y2 + 30 * 7))

def setVarValuesFromConfigFile():
    configFilePath = os.path.join(os.getcwd(), 'guopaiConfig.json')
    if os.path.exists(configFilePath):
        with open(configFilePath, 'r') as f:
            configParamers = json.loads(f.read())
        points = configParamers.get('points')
        policys = configParamers.get('policys')
        points_moni = configParamers.get('points_moni')
        policys_moni = configParamers.get('policys_moni')
        consoleRes('读取配置文件成功')
    else:
        points = {
            'customUpPriceIuput': (650, 375),            # 自定义加价输入框
            'customUpPriceButton': (800, 375),           # 自定义加价按钮
            'offerButton': (800, 485),                   # 出价按钮
            'currentPriceImage': (650, 469, 700, 486),   # 当前出价图片      moneyshot1.png  #retina屏分辨率高 截图需要 x2
            'lowestPriceImage': (151, 474, 193, 489),    # 最低可成交价图片   moneyshot2.png  #retina屏分辨率高 截图需要 x2
            'biggestPriceImage': (273, 522, 316, 538),   # 最高可接受价图片   moneyshot3.png  #retina屏分辨率高 截图需要 x2
            'YZMSureButton': (550, 564),                 # 验证码确定按钮
        }
        policys = {
            'basetimestr': '11:29:',  # 基础时间
            'startTime': '45.0',  # 检测最低成交价格 ，判断快还是慢
            'upTime':  # 第一次出价时间
                {'slow': '48.0',
                 'fast': '45.0'},
            'upPrice':  # 第一次出价加价
                {'slow': '800',
                 'fast': '500'},
            'checkPrice': '100',  # 验证差价
            'sureOfferTime':  # 验证码确定按钮点击最早时间
                {'slow': '53.0',
                 'fast': '55.0'},
            'latestSureOfferTime':  # 验证码确定按钮点击最晚时间
                {'slow': '55.0',
                 'fast': '57.0'},
        }
        points_moni = {
            'customUpPriceIuput': (650, 375),  # 自定义加价输入框
            'customUpPriceButton': (800, 375),  # 自定义加价按钮
            'offerButton': (800, 485),  # 出价按钮
            'currentPriceImage': (650, 469, 700, 486),  # 当前出价图片      moneyshot1.png  #retina屏分辨率高 截图需要 x2
            'rightPriceImage': (650, 469, 700, 486),  # 最低成交价图片     moneyshot2.png  #retina屏分辨率高 截图需要 x2
            'biggestPriceImage': (273, 522, 316, 538),  # 最高可接受价图片   moneyshot3.png  #retina屏分辨率高 截图需要 x2
            'YZMSureButton': (550, 564),  # 验证码确定按钮
        }
        policys_moni = {
            'basetimestr': '11:29:',  # 基础时间
            'startTime': '45.0',  # 检测最低成交价格 ，判断快还是慢
            'upTime':  # 第一次出价时间
                {'slow': '48.0',
                 'fast': '45.0'},
            'upPrice':  # 第一次出价加价
                {'slow': '800',
                 'fast': '500'},
            'checkPrice': '100',  # 验证差价
            'sureOfferTime':  # 验证码确定按钮点击最早时间
                {'slow': '53.0',
                 'fast': '55.0'},
            'latestSureOfferTime':  # 验证码确定按钮点击最晚时间
                {'slow': '55.0',
                 'fast': '57.0'},
        }
        consoleRes('配置文件不存在，采用预设参数')
    if isMoni:
        pointsDict = points_moni
        policysDict = policys_moni
    else:
        pointsDict = points
        policysDict = policys
    if pointsDict:
        var_customUpPriceIuput_x.set(pointsDict['customUpPriceIuput'][0])
        var_customUpPriceIuput_y.set(pointsDict['customUpPriceIuput'][1])
        var_customUpPriceButton_x.set(pointsDict['customUpPriceButton'][0])
        var_customUpPriceButton_y.set(pointsDict['customUpPriceButton'][1])
        var_offerButton_x.set(pointsDict['offerButton'][0])
        var_offerButton_y.set(pointsDict['offerButton'][1])
        var_currentPriceImage_x1.set(pointsDict['currentPriceImage'][0])
        var_currentPriceImage_y1.set(pointsDict['currentPriceImage'][1])
        var_currentPriceImage_x2.set(pointsDict['currentPriceImage'][2])
        var_currentPriceImage_y2.set(pointsDict['currentPriceImage'][3])
        var_rightPriceImage_x1.set(pointsDict['rightPriceImage'][0])
        var_rightPriceImage_y1.set(pointsDict['rightPriceImage'][1])
        var_rightPriceImage_x2.set(pointsDict['rightPriceImage'][2])
        var_rightPriceImage_y2.set(pointsDict['rightPriceImage'][3])
        var_biggestPriceImage_x1.set(pointsDict['biggestPriceImage'][0])
        var_biggestPriceImage_y1.set(pointsDict['biggestPriceImage'][1])
        var_biggestPriceImage_x2.set(pointsDict['biggestPriceImage'][2])
        var_biggestPriceImage_y2.set(pointsDict['biggestPriceImage'][3])
        var_YZMSureButton_x.set(pointsDict['YZMSureButton'][0])
        var_YZMSureButton_y.set(pointsDict['YZMSureButton'][1])
    if policysDict:
        var_basetime_h.set(policysDict['basetimestr'].split(':')[0])
        var_basetime_m.set(policysDict['basetimestr'].split(':')[1])
        var_startTime.set(policysDict['startTime'])
        var_upTime_fast.set(policysDict['upTime']['fast'])
        var_upTime_slow.set(policysDict['upTime']['slow'])
        var_upPrice_fast.set(policysDict['upPrice']['fast'])
        var_upPrice_slow.set(policysDict['upPrice']['slow'])
        var_checkPrice.set(policysDict['checkPrice'])
        var_sureOfferTime_fast.set(policysDict['sureOfferTime']['fast'])
        var_sureOfferTime_slow.set(policysDict['sureOfferTime']['slow'])
        var_latestSureOfferTime_fast.set(policysDict['latestSureOfferTime']['fast'])
        var_latestSureOfferTime_slow.set(policysDict['latestSureOfferTime']['slow'])
    consoleRes('参数设置完毕--%s' % ('模拟程序' if isMoni else '真实程序'))


def checkParamers():
    consoleRes('检查参数格式')
    checkRirgt = True
    if var_currentPriceImage_y2.get() - var_currentPriceImage_y1.get() < 15:
        checkRirgt = False
        consoleRes('当前出价图片尺寸有误，最短边应不小于15')
    if var_rightPriceImage_y2.get() - var_rightPriceImage_y1.get() < 15:
        checkRirgt = False
        consoleRes('最低可成交价图片尺寸有误，最短边应不小于1')
    if var_biggestPriceImage_y2.get() - var_biggestPriceImage_y1.get() < 15:
        checkRirgt = False
        consoleRes('最高可接受价格图片尺寸有误，最短边应不小于1')
    if len(var_basetime_h.get()) != 2 or len(var_basetime_m.get()) != 2:
        checkRirgt = False
        consoleRes('基础时间格式有误，正确格式如上午8点八分\"08:08\"')
    if len(var_upTime_fast.get().split('.')) != 2 or len(var_upTime_slow.get().split('.')) != 2:
        checkRirgt = False
        consoleRes('出价时间格式有误，正确格式如\"45.0\"')
    if len(var_sureOfferTime_fast.get().split('.')) != 2 or len(var_sureOfferTime_slow.get().split('.')) != 2:
        checkRirgt = False
        consoleRes('最早提交出价时间格式有误，正确格式如\"45.0\"')
    if len(var_latestSureOfferTime_fast.get().split('.')) != 2 or len(
            var_latestSureOfferTime_slow.get().split('.')) != 2:
        checkRirgt = False
        consoleRes('最晚提交出价时间格式有误，正确格式如\"45.0\"')
    return checkRirgt


def saveParamersToConfigFile():
    paramersRight = checkParamers()
    if paramersRight:
        configFilePath = os.path.join(os.getcwd(), 'guopaiConfig.json')
        if os.path.exists(configFilePath):
            with open(configFilePath, 'r') as f:
                configParamers = json.loads(f.read())
            points = configParamers.get('points')
            policys = configParamers.get('policys')
            points_moni = configParamers.get('points_moni')
            policys_moni = configParamers.get('policys_moni')
        else:
            points = {
                'customUpPriceIuput': (650, 375),  # 自定义加价输入框
                'customUpPriceButton': (800, 375),  # 自定义加价按钮
                'offerButton': (800, 485),  # 出价按钮
                'currentPriceImage': (650, 469, 700, 486),  # 当前出价图片      moneyshot1.png  #retina屏分辨率高 截图需要 x2
                'rightPriceImage': (650, 469, 700, 486),  # 最低成交价图片     moneyshot2.png  #retina屏分辨率高 截图需要 x2
                'biggestPriceImage': (273, 522, 316, 538),  # 最高可接受价图片   moneyshot3.png  #retina屏分辨率高 截图需要 x2
                'YZMSureButton': (550, 564),  # 验证码确定按钮
            }
            policys = {
                'basetimestr': '11:29:',  # 基础时间
                'startTime': '45.0',  # 检测最低成交价格 ，判断快还是慢
                'upTime':  # 第一次出价时间
                    {'slow': '48.0',
                     'fast': '45.0'},
                'upPrice':  # 第一次出价加价
                    {'slow': '800',
                     'fast': '500'},
                'checkPrice': '100',  # 验证差价
                'sureOfferTime':  # 验证码确定按钮点击最早时间
                    {'slow': '53.0',
                     'fast': '55.0'},
                'latestSureOfferTime':  # 验证码确定按钮点击最晚时间
                    {'slow': '55.0',
                     'fast': '57.0'},
            }
            points_moni = {
                'customUpPriceIuput': (650, 375),  # 自定义加价输入框
                'customUpPriceButton': (800, 375),  # 自定义加价按钮
                'offerButton': (800, 485),  # 出价按钮
                'currentPriceImage': (650, 469, 700, 486),  # 当前出价图片      moneyshot1.png  #retina屏分辨率高 截图需要 x2
                'rightPriceImage': (650, 469, 700, 486),  # 最低成交价图片     moneyshot2.png  #retina屏分辨率高 截图需要 x2
                'biggestPriceImage': (273, 522, 316, 538),  # 最高可接受价图片   moneyshot3.png  #retina屏分辨率高 截图需要 x2
                'YZMSureButton': (550, 564),  # 验证码确定按钮
            }
            policys_moni = {
                'basetimestr': '11:29:',  # 基础时间
                'startTime': '45.0',  # 检测最低成交价格 ，判断快还是慢
                'upTime':  # 第一次出价时间
                    {'slow': '48.0',
                     'fast': '45.0'},
                'upPrice':  # 第一次出价加价
                    {'slow': '800',
                     'fast': '500'},
                'checkPrice': '100',  # 验证差价
                'sureOfferTime':  # 验证码确定按钮点击最早时间
                    {'slow': '53.0',
                     'fast': '55.0'},
                'latestSureOfferTime':  # 验证码确定按钮点击最晚时间
                    {'slow': '55.0',
                     'fast': '57.0'},
            }
        newPoints = {
            'customUpPriceIuput': (var_customUpPriceIuput_x.get(), var_customUpPriceIuput_y.get()),
            'customUpPriceButton': (var_customUpPriceButton_x.get(), var_customUpPriceButton_y.get()),
            'offerButton': (var_offerButton_x.get(), var_offerButton_y.get()),
            'currentPriceImage': (
            var_currentPriceImage_x1.get(), var_currentPriceImage_y1.get(), var_currentPriceImage_x2.get(),
            var_currentPriceImage_y2.get()),
            'rightPriceImage': (
            var_rightPriceImage_x1.get(), var_rightPriceImage_y1.get(), var_rightPriceImage_x2.get(),
            var_rightPriceImage_y2.get()),
            'biggestPriceImage': (
            var_biggestPriceImage_x1.get(), var_biggestPriceImage_y1.get(), var_biggestPriceImage_x2.get(),
            var_biggestPriceImage_y2.get()),
            'YZMSureButton': (var_YZMSureButton_x.get(), var_YZMSureButton_y.get()),
        }
        newPolicys = {
            'basetimestr': var_basetime_h.get() + ':' + var_basetime_m.get() + ':',
            'startTime': var_startTime.get(),
            'upTime':
                {'slow': var_upTime_slow.get(),
                 'fast': var_upTime_fast.get()},
            'upPrice':
                {'slow': var_upPrice_slow.get(),
                 'fast': var_upPrice_fast.get()},
            'checkPrice': var_checkPrice.get(),
            'sureOfferTime':
                {'slow': var_sureOfferTime_slow.get(),
                 'fast': var_sureOfferTime_fast.get()},
            'latestSureOfferTime':
                {'slow': var_latestSureOfferTime_slow.get(),
                 'fast': var_latestSureOfferTime_fast.get()},
        }
        if isMoni:
            paramers = {
                'points': points,
                'policys': policys,
                'points_moni': newPoints,
                'policys_moni': newPolicys,
            }
        else:
            paramers = {
                'points': newPoints,
                'policys': newPolicys,
                'points_moni': points_moni,
                'policys_moni': policys_moni,
            }
        with open(configFilePath, 'w') as f_w:
            f_w.write(json.dumps(paramers))
        consoleRes('配置保存成功--%s' % ('模拟程序' if isMoni else '真实程序'))


def consoleRes(res):
    global consoleText
    consoleText.insert(tk.END, res + '\n')
    consoleText.update()


def checkTimeRight(time):  # 到达指定时间跳出循环往下执行，否则一直等待
    checktime = datetime.datetime.strptime(var_basetime_h.get() + ':' + var_basetime_m.get() + ':' + time.split('.')[0],
                                           "%H:%M:%S").time()
    while True:
        now = datetime.datetime.now().time()
        if now >= checktime:
            break


def checkSecondBiggerThan(second):  # 到达指定秒跳出循环往下执行，否则一直等待
    while True:
        now = datetime.datetime.now()
        if float(str(now)[17:21]) >= float(second):
            break


def checkTimeLessThan(time):
    now = datetime.datetime.now()
    if float(str(now)[17:21]) < float(time):
        return True
    return False


def get_file_content(filePath):  # 读取图片
    with open(filePath, 'rb') as fp:
        return fp.read()

isRun = False

def run():
    global isRun
    if not isRun:
        isRun = True
        t = threading.Thread(target=startPolicy)
        t.setDaemon(True)
        t.start()



def startPolicy():
    global isRun
    paramersRight = checkParamers()
    if paramersRight:
        consoleRes('开始-- %s' % ('模拟程序' if isMoni else '真实程序'))
        newPoints = {
            'customUpPriceIuput': (var_customUpPriceIuput_x.get(), var_customUpPriceIuput_y.get()),
            'customUpPriceButton': (var_customUpPriceButton_x.get(), var_customUpPriceButton_y.get()),
            'offerButton': (var_offerButton_x.get(), var_offerButton_y.get()),
            'currentPriceImage': (
                var_currentPriceImage_x1.get(), var_currentPriceImage_y1.get(), var_currentPriceImage_x2.get(),
                var_currentPriceImage_y2.get()),
            'rightPriceImage': (
                var_rightPriceImage_x1.get(), var_rightPriceImage_y1.get(), var_rightPriceImage_x2.get(),
                var_rightPriceImage_y2.get()),
            'biggestPriceImage': (
                var_biggestPriceImage_x1.get(), var_biggestPriceImage_y1.get(), var_biggestPriceImage_x2.get(),
                var_biggestPriceImage_y2.get()),
            'YZMSureButton': (var_YZMSureButton_x.get(), var_YZMSureButton_y.get()),
        }
        newPolicys = {
            'basetimestr': var_basetime_h.get() + ':' + var_basetime_m.get() + ':',
            'startTime': var_startTime.get(),
            'upTime':
                {'slow': var_upTime_slow.get(),
                 'fast': var_upTime_fast.get()},
            'upPrice':
                {'slow': var_upPrice_slow.get(),
                 'fast': var_upPrice_fast.get()},
            'checkPrice': var_checkPrice.get(),
            'sureOfferTime':
                {'slow': var_sureOfferTime_slow.get(),
                 'fast': var_sureOfferTime_fast.get()},
            'latestSureOfferTime':
                {'slow': var_latestSureOfferTime_slow.get(),
                 'fast': var_latestSureOfferTime_fast.get()},
        }
        try:
            consoleRes(str(datetime.datetime.now().second))
            checkTimeRight(newPolicys['startTime'])
            consoleRes(str(datetime.datetime.now().second))
            moneyshot2 = ImageGrab.grab(newPoints['rightPriceImage'])  # 最低可成交价图片
            moneyshot2.save('moneyshot2.png')
            consoleRes(str(datetime.datetime.now().second))
            moneyshot2 = get_file_content('moneyshot2.png')
            moneyress2 = client.basicGeneral(moneyshot2)
            consoleRes('最低可成交价识别结果--%s' % moneyress2)
            moneystr2 = moneyress2['words_result'][0]['words']  # 最低可成交价
            consoleRes('%s秒--最低可成交价--%s' % (newPolicys['startTime'], moneystr2))

            isSlow = True
            if int(moneystr2) < 87000:
                isSlow = False

            if isSlow:
                upPrice = newPolicys['upPrice']['slow']
                upTime = newPolicys['upTime']['slow']
                sureOfferTime = newPolicys['sureOfferTime']['slow']
                latestSureOfferTime = newPolicys['latestSureOfferTime']['slow']
            else:
                upPrice = newPolicys['upPrice']['fast']
                upTime = newPolicys['upTime']['fast']
                sureOfferTime = newPolicys['sureOfferTime']['fast']
                latestSureOfferTime = newPolicys['latestSureOfferTime']['fast']

            checkSecondBiggerThan(upTime)

            pg.moveTo(newPoints['customUpPriceIuput'])  # 自定义加价输入框
            time.sleep(sleeptime)
            pg.click()
            pg.click()
            pg.typewrite(upPrice)  # 输入自定义加价

            pg.moveTo(newPoints['customUpPriceButton'])  # 自定义加价按钮 # 点击效果等同于输入出价
            time.sleep(sleeptime)
            pg.click()

            moneyshot1 = ImageGrab.grab(newPoints['currentPriceImage'])  # 当前出价框
            moneyshot1.save('moneyshot1.png')
            moneyshot1 = get_file_content('moneyshot1.png')
            moneyress1 = client.basicGeneral(moneyshot1)
            consoleRes('出价识别结果--%s' % moneyress1)
            moneystr1 = moneyress1['words_result'][0]['words']  # 当前出价
            consoleRes('%s秒--出价--%s' % (datetime.datetime.now().second, moneystr1))

            pg.moveTo(newPoints['offerButton'])  # 出价按钮
            time.sleep(sleeptime)
            pg.click()

            # 现在手动输入验证码

            checkSecondBiggerThan(sureOfferTime)  # 开始检测 价格差

            while checkTimeLessThan(latestSureOfferTime):  # 到达出价时间 或者 到达检测价格 强制出价
                moneyshot3 = ImageGrab.grab(newPoints['biggestPriceImage'])  # 最大可接受出价图片
                moneyshot3.save('moneyshot3.png')
                moneyshot3 = get_file_content('moneyshot3.png')
                moneyress3 = client.basicGeneral(moneyshot3)
                consoleRes('%s秒--最大可接受出价--%s' %(datetime.datetime.now().second, moneyress3))
                moneystr3 = moneyress3['words_result'][0]['words']  # 最大可接受出价
                if int(moneystr1) - int(moneystr3) <= int(newPolicys['checkPrice']):
                    consoleRes('出价到达检查点:  %s' % datetime.datetime.now().second)
                    break
            consoleRes('提交出价时间：%s' % str(datetime.datetime.now())[17:21])

            pg.moveTo(newPoints['YZMSureButton'])  # 验证码确定按钮
            time.sleep(sleeptime)
            pg.click()
            isRun = False
        except Exception:
            consoleRes('运行失败--%s' % traceback.format_exc())
            isRun = False

tk.Button(window, text="从配置文件读取参数", command=setVarValuesFromConfigFile).place(x=50, y=620, w=150)
tk.Button(window, text="保存参数到配置文件", command=saveParamersToConfigFile).place(x=220, y=620, w=150)
tk.Button(window, text="开始", font=("Arial", 20), command=run).place(x=500, y=20, w=150, h=50)
tk.Label(window, text='程序输出', font=("Arial", 16)).place(x=400, y=70)
consoleText = tk.Text(window, bg='gray')
consoleText.place(x=430, y=100, w=300, h=500)





window.mainloop()