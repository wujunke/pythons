#!/usr/bin/env python
# coding: utf-8
#

from wxbot import *
import sys
reload(sys)
sys.setdefaultencoding('gb2312')

fpath = '/Users/investarget/Desktop/django_server/pdffile/中文.pdf'

path1 =  os.path.basename(fpath)
path2 =  str(os.path.getsize(fpath))
path3 =  fpath.split('.')[-1]
print path1,path2,path3