#coding=utf-8
import os
import sys
import time
from PIL import ImageGrab
import pyautogui as pg
# pip install baidu-aip
from aip import AipOcr
import datetime
reload(sys)
sys.setdefaultencoding('utf8')



basetimestr = '14:04:'

sleeptime = 0.01  #鼠标反应时间

# points = {
#     'customUpPriceIuput': (650, 375),            # 自定义加价输入框
#     'customUpPriceButton': (800, 375),           # 自定义加价按钮
#     'offerButton': (800, 485),                   # 出价按钮
#     'currentPriceImage': (650, 469, 700, 486),   # 当前出价图片      moneyshot1.png  #retina屏分辨率高 截图需要 x2
#     'rightPriceImage': (),                       # 最低成交价图片      moneyshot2.png  #retina屏分辨率高 截图需要 x2
#     'biggestPriceImage': (273, 522, 316, 538),   # 最高可接受价图片   moneyshot3.png  #retina屏分辨率高 截图需要 x2
#     'YZMquestion': (),                           # 验证码问题
#     'YZMImage': (),                              # 验证码图片
#     'YZMCancelButton': (750, 564),               # 验证码取消按钮
#     'YZMSureButton': (550, 564),                 # 验证码确定按钮
# }

points = {
    'customUpPriceIuput': (650, 375),            # 自定义加价输入框
    'customUpPriceButton': (800, 375),           # 自定义加价按钮
    'offerButton': (800, 485),                   # 出价按钮
    'currentPriceImage': (650, 470, 700, 488),   # 当前出价图片      moneyshot1.png  #retina屏分辨率高 截图需要 x2
    'rightPriceImage': (151, 472, 192, 488),     # 最低成交价图片      moneyshot2.png  #retina屏分辨率高 截图需要 x2
    'biggestPriceImage': (275, 505, 318, 522),   # 最高可接受价图片   moneyshot3.png  #retina屏分辨率高 截图需要 x2
    'YZMquestion': (),                           # 验证码问题
    'YZMImage': (),                              # 验证码图片
    'YZMCancelButton': (750, 564),               # 验证码取消按钮
    'YZMSureButton': (550, 564),                 # 验证码确定按钮
}


APP_ID = '11546435'
API_KEY = 'w9646O4Ug0H2XNwXQX0WLcen'
SECRET_KEY = '4kPgOiOsSGH35asD1ifi3SzBgniLY00u'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

def checkTimeRight(time):  # 到达指定时间跳出循环往下执行，否则一直等待
    while True:
        now = datetime.datetime.now()
        if str(now)[11:21] == basetimestr + time:
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

def get_file_content(filePath): # 读取图片
    with open(filePath, 'rb') as fp:
        return fp.read()


def policyC():
    policys = {
        'startTime': '45.0',            # 检测最低成交价格 ，判断快还是慢
        'upTime':                    # 第一次出价时间
            {'slow': '48.0',
            'fast': '45.0'},
        'upPrice':                      # 第一次出价加价
            {'slow': '800',
            'fast': '500'},
        'checkPrice': '100',            # 验证差价
        'sureOfferTime':                # 验证码确定按钮点击最早时间
            {'slow': '53.0',
            'fast': '55.0'},
        'latestSureOfferTime':          # 验证码确定按钮点击最晚时间
            {'slow': '55.0',
            'fast': '57.0'},
    }

    checkTimeRight(policys['startTime'])

    moneyshot2 = ImageGrab.grab(points['rightPriceImage'])  # 最低可成交价图片
    moneyshot2.save('moneyshot2.png')
    moneyshot2 = get_file_content('moneyshot2.png')
    moneyress2 = client.basicGeneral(moneyshot2)
    moneystr2 = moneyress2['words_result'][0]['words']  # 最低可成交价
    print('%s秒--最低可成交价--%s' % (policys['startTime'], moneystr2))

    isSlow = True
    if int(moneystr2) < 87000:
        isSlow = False

    if isSlow:
        upPrice = policys['upPrice']['slow']
        upTime = policys['upTime']['slow']
        sureOfferTime = policys['sureOfferTime']['slow']
        latestSureOfferTime = policys['latestSureOfferTime']['slow']
    else:
        upPrice = policys['upPrice']['fast']
        upTime = policys['upTime']['fast']
        sureOfferTime = policys['sureOfferTime']['fast']
        latestSureOfferTime = policys['latestSureOfferTime']['fast']

    checkSecondBiggerThan(upTime)

    pg.moveTo(points['customUpPriceIuput'])  # 自定义加价输入框
    time.sleep(sleeptime)
    pg.click()
    pg.click()
    pg.typewrite(upPrice)            # 输入自定义加价

    pg.moveTo(points['customUpPriceButton'])    # 自定义加价按钮 # 点击效果等同于输入出价
    time.sleep(sleeptime)
    pg.click()

    moneyshot1 = ImageGrab.grab(points['currentPriceImage'])  # 当前出价框
    moneyshot1.save('moneyshot1.png')
    moneyshot1 = get_file_content('moneyshot1.png')
    moneyress1 = client.basicGeneral(moneyshot1)
    moneystr1 = moneyress1['words_result'][0]['words']  # 当前出价
    print('%s秒--出价--%s' % (upTime, moneystr1))


    pg.moveTo(points['offerButton'])     # 出价按钮
    time.sleep(sleeptime)
    pg.click()

    # 现在手动输入验证码

    checkSecondBiggerThan(sureOfferTime)     # 开始检测 价格差

    while checkTimeLessThan(latestSureOfferTime):               # 到达出价时间 或者 到达检测价格 强制出价
        moneyshot3 = ImageGrab.grab(points['biggestPriceImage'])  # 最大可接受出价图片
        moneyshot3.save('moneyshot3.png')
        moneyshot3 = get_file_content('moneyshot3.png')
        moneyress3 = client.basicGeneral(moneyshot3)
        print(moneyress3, str(datetime.datetime.now())[17:21])
        moneystr3 = moneyress3['words_result'][0]['words']  # 最大可接受出价
        if int(moneystr1) - int(moneystr3) <= int(policys['checkPrice']):
            print('出价到达检查点:  %s' % policys['checkPrice'])
            break
    print('提交出价时间：%s' % str(datetime.datetime.now())[17:21])

    pg.moveTo(points['YZMSureButton'])  # 验证码确定按钮
    time.sleep(sleeptime)
    pg.click()






policyC()