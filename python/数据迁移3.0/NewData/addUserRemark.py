# -*- coding: utf-8 -*-
import traceback
import  xdrlib ,sys

import _mssql

import pymysql
import xlrd
from datetime import datetime
from pypinyin import slug as hanzizhuanpinpin
import requests
from xlrd import xldate_as_tuple
import json

reload(sys)
sys.setdefaultencoding('utf-8')

token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'

# base_url = 'http://192.168.1.201:8000/'
# base_url = 'http://192.168.1.251:8080/'
base_url = 'https://api.investarget.com/'
headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }


