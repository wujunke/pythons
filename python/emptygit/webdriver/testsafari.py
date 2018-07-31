#coding=utf-8
import os

import time
from PIL import ImageGrab
import pyautogui as pg
# pip install baidu-aip
from aip import AipOcr
import datetime


# starttime = '11:29:45'
# checktime = '11:29:52'
starttime = '21:29:45'
checktime = '21:29:56'

def checktimetrue(time):
    #time = '11:29:00'
    while 1:
        now = datetime.datetime.now()
        if str(now)[11:19] == time:
            # print str(now)[11:19]
            break

checktimetrue(starttime)


APP_ID = '11546435'
API_KEY = 'w9646O4Ug0H2XNwXQX0WLcen'
SECRET_KEY = '4kPgOiOsSGH35asD1ifi3SzBgniLY00u'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

pg.moveTo(690, 400) #自定义加价输入框
time.sleep(0.1)
pg.click()
pg.click()
pg.typewrite('1000')
pg.moveTo(800, 400) #自定义加价按钮
time.sleep(0.1)
pg.click()

moneyshot1 = ImageGrab.grab((653, 491, 705, 511))    #出价框
moneyshot1.save('moneyshot1.png')
moneyshot1 = get_file_content('moneyshot1.png')
moneyress1 = client.basicGeneral(moneyshot1)
moneystr1 = moneyress1['words_result'][0]['words']

print moneystr1   #当前出价

pg.moveTo(800, 505)     #出价按钮
time.sleep(0.1)
pg.click()


# screenshot1 = ImageGrab.grab((450, 430, 700, 470))   #验证码题目图片
# screenshot1.save('shot1.png')
# screenshot2 = ImageGrab.grab((470, 475, 660, 560))   #验证码图片
# screenshot2.save('shot2.png')

checktimetrue(checktime)

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
pg.moveTo(550, 590)    #验证码确定按钮
time.sleep(0.1)
pg.click()
# pg.moveTo(665, 575)
# time.sleep(0.1)
# pg.click()



# driver.quit()