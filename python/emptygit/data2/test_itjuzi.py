#coding=utf-8
import json
import random
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

from data2.itjuzi_config import Cookie, base_url, token, insert_rate, find_rate, judgerepeat, temp_path_base, iplist, iplist2


import datetime
import requests
import time
from bs4 import BeautifulSoup



def rand_proxie():
    return {'http':'http://%s' % iplist[random.randint(0, len(iplist)) - 1],}

def rand_proxie2():
    return {'https':'https://%s' % iplist2[random.randint(0, len(iplist2)) - 1],}
class InvestError(Exception):
    def __init__(self, msg):
        self.msg = msg
# 公司详情
url_company_detail_http = 'http://radar.itjuzi.com/company/'
url_company_detail_https = 'https://www.itjuzi.com/company/'


heders = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'radar.itjuzi.com',
            'Referer':'http://radar.itjuzi.com///company?phpSessId=e65ca8471446469d5e68b8885ff06f67fc0d31db?phpSessId=d87230bfa03a3885aa4471da7ab09491948fff74',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie':Cookie,
}

def getCompanyDetail(com_id):
    num = 3  # 重试次数
    com_name = ''
    while num > 0:
        try:
            pox = rand_proxie2()
            html = requests.get(url_company_detail_https + '%s' % com_id, headers=heders, proxies=pox).content
        except ConnectionError:
            print 'Timeout, try again'
            num -= 1
        else:
            print 'com_ok'
            break
    else:
        # 3次都失败
        print 'Try 3 times, But all failed'
        raise InvestError('连接失败，Try 3 times, But all failed')
    print html


html1 = getCompanyDetail(2)
print html1