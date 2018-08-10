#coding=utf-8
import os

import time
# from PIL import ImageGrab
import pyautogui as pg
# pip install baidu-aip
# from aip import AipOcr
import datetime

policy = 'a'

policys = {
    'a':{
        'startTime': '11:39:44.0',   # 第一次出价时间
        'upPrice': '1000',           # 第一次出价加价
        'checkTime': '11:39:56.0',   # 验证码确定按钮点击时间
    },
}

points = {
    'customUpPriceIuput': (690, 378),   # 自定义加价输入框
    'customUpPriceButton': (800, 378),  # 自定义加价按钮
    'offerButton': (800, 505 - 22),          # 出价按钮
    'lowestPriceImage': (151, 495 - 22, 195, 511 - 22),     # 最低可成交价图片
    'YZMquestion': (),          # 验证码问题
    'YZMImage': (),             # 验证码图片
    'YZMSureButton': (550, 590 - 22)         # 验证码确定按钮
}


def startTime():   # 第一次出价时间
    return policys[policy]['startTime']

def upPrice():     # 第一次出价加价
    return policys[policy]['upPrice']

def checkTime():   # 验证码确定按钮点击时间
    return policys[policy]['checkTime']


def checkTimeRight(time):   # 到达指定时间跳出循环往下执行，否则一直等待
    while 1:
        now = datetime.datetime.now()
        if str(now)[11:21] == time:
            break


def get_file_content(filePath): # 读取图片
    with open(filePath, 'rb') as fp:
        return fp.read()


checkTimeRight(startTime())

pg.moveTo(points['customUpPriceIuput']) #自定义加价输入框
time.sleep(0.1)
pg.click()
pg.click()
pg.typewrite(upPrice())
pg.moveTo(points['customUpPriceButton']) #自定义加价按钮
time.sleep(0.1)
pg.click()


pg.moveTo(points['offerButton'])     #出价按钮
time.sleep(0.1)
pg.click()


checkTimeRight(checkTime())

# moneyshot2 = ImageGrab.grab((151, 495, 195, 511))    #最低可成交价图片
# moneyshot2.save('moneyshot2.png')
#
# moneyshot2 = get_file_content('moneyshot2.png')
# moneyress2 = client.basicGeneral(moneyshot2)
# moneystr2 = moneyress2['words_result'][0]['words']
#
# print moneystr2  #最低可成交价
#
# if int(moneystr1) - int(moneystr2) >= 800:
#     pg.moveTo(740, 590)    #验证码页面取消按钮
#     time.sleep(0.05)
#     pg.click()
#     time.sleep(0.05)
#     pg.moveTo(650, 400)     #自定义加价输入框
#     time.sleep(0.05)
#     pg.click()
#     pg.press(['delete', 'delete', 'delete', 'delete'])
#     pg.typewrite('600')
#     pg.moveTo(800, 400)      #自定义加价按钮
#     time.sleep(0.05)
#     pg.click()
#     pg.moveTo(800, 505)     #出价按钮
#     time.sleep(0.05)
#     pg.click()


# image = get_file_content('shot1.png')     #验证码问题
# ress = client.basicGeneral(image)
# resultstr = ress['words_result'][0]['words']
# print(resultstr)



# pg.moveTo(704, 508)
# time.sleep(0.1)
# pg.click()
# # pg.typewrite('123')
# time.sleep(3)
pg.moveTo(points['YZMSureButton'])    #验证码确定按钮
time.sleep(0.1)
pg.click()
# pg.moveTo(665, 575)
# time.sleep(0.1)
# pg.click()



# driver.quit()



706