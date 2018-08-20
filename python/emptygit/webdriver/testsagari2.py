#coding=utf-8
import os

import time
from PIL import ImageGrab
import pyautogui as pg
# pip install baidu-aip
from aip import AipOcr
import datetime

# policy = 'a'
# policy = 'b'
policy = 'c'

basetimestr = '10:33:'

isRetina = False

sleeptime = 0.02  #鼠标反应时间

#rect : (x1, y1, x2, y2)  retina显示屏截图坐标转换
def transRect(rect):
    if isRetina:
        return (x * 2 for x in rect)
    return rect

# 浏览器多页面时出现的头部高度   safari为22
browser_header = 0

points = {
    'customUpPriceIuput': (645, 340 - browser_header),            # 自定义加价输入框
    'customUpPriceButton': (800, 340 - browser_header),           # 自定义加价按钮
    'offerButton': (800, 505 - browser_header),                   # 出价按钮
    'currentPriceImage': transRect((640, 490 - browser_header, 710, 511 - browser_header)),   # 当前出价图片      moneyshot1.png
    'lowestPriceImage': transRect((150, 495 - browser_header, 195, 511 - browser_header)),    # 最低可成交价图片   moneyshot2.png
    'biggestPriceImage': transRect((275, 526 - browser_header, 318, 542 - browser_header)),   # 最高可接受价图片   moneyshot3.png
    'YZMquestion': (),                                # 验证码问题
    'YZMImage': (),                                   # 验证码图片
    'YZMCancelButton': (750, 590 - browser_header),               # 验证码取消按钮
    'YZMSureButton': (550, 590 - browser_header),                 # 验证码确定按钮
}
APP_ID = '11546435'
API_KEY = 'w9646O4Ug0H2XNwXQX0WLcen'
SECRET_KEY = '4kPgOiOsSGH35asD1ifi3SzBgniLY00u'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def checkTimeRight(time):  # 到达指定时间跳出循环往下执行，否则一直等待
    while 1:
        now = datetime.datetime.now()
        if str(now)[11:21] == basetimestr + time:
            break

def checkTimeLessThan(time):
    now = datetime.datetime.now()
    if float(str(now)[17:21]) < float(time):
        return True
    return False

def get_file_content(filePath): # 读取图片
    with open(filePath, 'rb') as fp:
        return fp.read()

def policyA():

    policys = {
            'startTime': '44.0',   # 第一次出价时间
            'upPrice': '1000',           # 第一次出价加价
            'sureOfferTime': '56.0',   # 验证码确定按钮点击时间
    }

    checkTimeRight(policys['startTime'])

    pg.moveTo(points['customUpPriceIuput'])  # 自定义加价输入框
    time.sleep(sleeptime)
    pg.click()
    pg.click()
    pg.typewrite(policys['upPrice'])            # 输入自定义加价

    pg.moveTo(points['customUpPriceButton'])    # 自定义加价按钮 # 点击效果等同于输入出价
    time.sleep(sleeptime)
    pg.click()
    pg.moveTo(points['offerButton'])     # 出价按钮
    time.sleep(sleeptime)
    pg.click()

    checkTimeRight(policys['sureOfferTime'])

    pg.moveTo(points['YZMSureButton'])  # 验证码确定按钮
    time.sleep(sleeptime)
    pg.click()



def policyB():
    policys = {
        'startTime': '45.0',          # 第一次出价时间
        'firstUpPrice': '1000',                     # 第一次出价加价
        'checkPriceTime': '51.0',     # 验证差价时间
        'checkPrice': '800',                        # 验证差价
        'secondUpPrice': '600',                     # 第二次出价加价
        'sureOfferTime': '55.5',      # 验证码确定按钮点击时间
    }

    checkTimeRight(policys['startTime'])      # 验证时间开始出价

    pg.moveTo(points['customUpPriceIuput'])   # 自定义加价输入框
    time.sleep(sleeptime)
    pg.click()
    pg.click()
    pg.typewrite(policys['firstUpPrice'])      # 输入自定义加价
    pg.moveTo(points['customUpPriceButton'])   # 自定义加价按钮 # 点击效果等同于输入出价
    time.sleep(sleeptime)
    pg.click()

    moneyshot1 = ImageGrab.grab(points['currentPriceImage'])  # 当前出价框
    moneyshot1.save('moneyshot1.png')
    moneyshot1 = get_file_content('moneyshot1.png')
    moneyress1 = client.basicGeneral(moneyshot1)
    moneystr1 = moneyress1['words_result'][0]['words']        # 当前出价

    pg.moveTo(points['offerButton'])                  # 出价按钮
    time.sleep(sleeptime)
    pg.click()

    checkTimeRight(policys['checkPriceTime'])             # 监测最低可成交价

    moneyshot2 = ImageGrab.grab(points['lowestPriceImage'])    # 最低可成交价图片
    moneyshot2.save('moneyshot2.png')

    moneyshot2 = get_file_content('moneyshot2.png')
    moneyress2 = client.basicGeneral(moneyshot2)
    moneystr2 = moneyress2['words_result'][0]['words']   # 最低可成交价

    if int(moneystr1) - int(moneystr2) >= int(policys['checkPrice']):
        pg.moveTo(points['YZMCancelButton'])        # 验证码页面取消按钮
        time.sleep(sleeptime)
        pg.click()
        time.sleep(sleeptime)
        pg.moveTo(points['customUpPriceIuput'])     # 自定义加价输入框
        time.sleep(sleeptime)
        pg.click()
        pg.press(['delete', 'delete', 'delete', 'delete'])
        pg.typewrite(policys['secondUpPrice'])
        pg.moveTo(points['customUpPriceButton'])      # 自定义加价按钮
        time.sleep(sleeptime)
        pg.click()
        pg.moveTo(points['offerButton'])     #出价按钮
        time.sleep(sleeptime)
        pg.click()

    checkTimeRight(policys['sureOfferTime'])

    pg.moveTo(points['YZMSureButton'])  # 验证码确定按钮   #确定出价
    time.sleep(sleeptime)
    pg.click()


def policyC():
    policys = {
            'startTime': '49.0',        # 第一次出价时间
            'upPrice': '700',           # 第一次出价加价
            'checkPrice': '100',          # 验证差价
            'sureOfferTime': '53.0',    # 验证码确定按钮点击最早时间
            'latestSureOfferTime': '55.0',    # 验证码确定按钮点击最晚时间
    }
    checkTimeRight(policys['startTime'])

    pg.moveTo(points['customUpPriceIuput'])  # 自定义加价输入框
    time.sleep(sleeptime)
    pg.click()
    pg.click()
    pg.typewrite(policys['upPrice'])            # 输入自定义加价

    pg.moveTo(points['customUpPriceButton'])    # 自定义加价按钮 # 点击效果等同于输入出价
    time.sleep(sleeptime)
    pg.click()

    moneyshot1 = ImageGrab.grab(points['currentPriceImage'])  # 当前出价框
    moneyshot1.save('moneyshot1.png')
    moneyshot1 = get_file_content('moneyshot1.png')
    moneyress1 = client.basicGeneral(moneyshot1)
    moneystr1 = moneyress1['words_result'][0]['words']  # 当前出价

    pg.moveTo(points['offerButton'])     # 出价按钮
    time.sleep(sleeptime)
    pg.click()

    # 现在手动输入验证码

    checkTimeRight(policys['sureOfferTime'])

    while checkTimeLessThan(policys['latestSureOfferTime']):
        moneyshot3 = ImageGrab.grab(points['biggestPriceImage'])  # 最大可接受出价图片
        moneyshot3.save('moneyshot3.png')
        moneyshot3 = get_file_content('moneyshot3.png')
        moneyress3 = client.basicGeneral(moneyshot3)
        print(moneyress3, str(datetime.datetime.now())[17:21])
        moneystr3 = moneyress3['words_result'][0]['words']  # 最大可接受出价
        if int(moneystr1) - int(moneystr3) <= int(policys['checkPrice']):
            break

    pg.moveTo(points['YZMSureButton'])  # 验证码确定按钮
    time.sleep(sleeptime)
    pg.click()





if policy == 'a':
    policyA()
elif policy == 'b':
    policyB()
elif policy == 'c':
    policyC()