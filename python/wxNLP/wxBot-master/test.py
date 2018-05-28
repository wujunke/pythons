#!/usr/bin/env python
# coding: utf-8
#

# from wxbot import *
# import sys
# reload(sys)
# sys.setdefaultencoding('gb2312')
#
# fpath = '/Users/investarget/Desktop/django_server/pdffile/中文.pdf'
#
# path1 =  os.path.basename(fpath)
# path2 =  str(os.path.getsize(fpath))
# path3 =  fpath.split('.')[-1]
# print path1,path2,path3
import json
import os

import datetime
import shutil

import requests


def deleteExpireDir(rootpath):
    #删除过期的文件夹/文件
    if (os.path.exists(rootpath)):
        files = os.listdir(rootpath)
        for file in files:
            m = os.path.join(rootpath, file)
            if (os.path.isdir(m)) and checkDirCtimeExpire(m,0):
                #过期的文件夹
                if os.path.exists(m):
                    shutil.rmtree(m)
            if (os.path.isfile(m)) and checkDirCtimeExpire(m,0):
                #过期的文件
                if os.path.exists(m):
                    os.remove(m)

def checkDirCtimeExpire(path, expire=1):
    filePath = unicode(path, 'utf8')
    timeStamp = os.path.getctime(filePath)
    datetimeStruct = datetime.datetime.fromtimestamp(timeStamp)
    if datetimeStruct < (datetime.datetime.now() - datetime.timedelta(hours=24 * expire)):
        return True
    else:
        return False


line = '{"智店项目": "本周项目自动推送：全国首家智能便利店技术/运营提供商，拟交易规模：$10000000 USD"}'



# ds = json.loads(line)
# print ds[unicode("智店项目", "utf-8")]
#
# groupnames = [u'特工', u'多维海拓投资人交流11群·大健康', u'多维海拓投资人交流1群', u'多维海拓投资人交流10群', u'多维海拓投资人交流9群',
#                                 u'多维海拓投资人交流3群', u'多维海拓投资人交流4群', u'多维海拓投资人交流12群·AR·VR', u'多维海拓投资人交流5群']
# deleteExpireDir('/Users/investarget/Desktop/django_server/pdffile')

aa = 'aaa        d        sss'
vv = aa.split()
print vv