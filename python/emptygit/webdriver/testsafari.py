#coding=utf-8
import os

import time
from PIL import ImageGrab
import pyautogui as pg
# pip install baidu-aip
from aip import AipOcr
import datetime

# policy = 'a'
policy = 'b'

basetimestr = '12:59:'

sleeptime = 0.05  #鼠标反应时间

points = {
    'customUpPriceIuput': (650, 400 - 22),            # 自定义加价输入框
    'customUpPriceButton': (800, 400 - 22),           # 自定义加价按钮
    'offerButton': (800, 505 - 22),                   # 出价按钮
    'currentPriceImage': (640, 490 - 22, 710, 511 - 22),   # 当前出价图片
    'lowestPriceImage': (150, 495 - 22, 195, 511 - 22),    # 最低可成交价图片
    'YZMquestion': (),                           # 验证码问题
    'YZMImage': (),                              # 验证码图片
    'YZMCancelButton': (750, 590 - 22),               # 验证码取消按钮
    'YZMSureButton': (550, 590 - 22),                 # 验证码确定按钮
}


def checkTimeRight(time):  # 到达指定时间跳出循环往下执行，否则一直等待
    while 1:
        now = datetime.datetime.now()
        if str(now)[11:21] == time:
            break

def get_file_content(filePath): # 读取图片
    with open(filePath, 'rb') as fp:
        return fp.read()

def policyA():

    policys = {
            'startTime': basetimestr + '44.0',   # 第一次出价时间
            'upPrice': '1000',           # 第一次出价加价
            'sureOfferTime': basetimestr + '56.0',   # 验证码确定按钮点击时间
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
    APP_ID = '11546435'
    API_KEY = 'w9646O4Ug0H2XNwXQX0WLcen'
    SECRET_KEY = '4kPgOiOsSGH35asD1ifi3SzBgniLY00u'

    policys = {
        'startTime': basetimestr + '44.0',          # 第一次出价时间
        'firstUpPrice': '1000',                     # 第一次出价加价
        'checkPriceTime': basetimestr + '51.0',     # 验证差价时间
        'checkPrice': '800',                        # 验证差价
        'secondUpPrice': '600',                     # 第二次出价加价
        'sureOfferTime': basetimestr + '56.0',      # 验证码确定按钮点击时间
    }

    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

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




if policy == 'a':
    policyA()
else:
    policyB()