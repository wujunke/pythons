# -*- coding:utf-8 -*-
# !/usr/bin/python
from bs4 import BeautifulSoup
import requests



headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'radar.itjuzi.com',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}

r1 = requests.get(url='https://www.itjuzi.com/user/login?flag=radar',headers=headers, proxies=proxie)
r1_cookies_dict = r1.cookies.get_dict()

r2 = requests.post(
    url='https://www.itjuzi.com/user/login?redirect=%2F%2Fmycom%3FphpSessId%3D20635173d733c34d52c10f0a4d41df66b05e2830&flag=radar&radar_coupon=',
    data={
        'identity': '18616837957',
        'password': 'x81y0122',
        'remember': 1,
        'submit':None,
        'page': None,
        'url': None,
    },
    cookies=r1_cookies_dict,
    headers=headers,
    proxies=proxie
)
r2_cookies_dict = r2.cookies.get_dict()

# print(r1_cookies_dict)
# print(r2_cookies_dict)

all_cookies = {}

all_cookies.update(r1_cookies_dict)
all_cookies.update(r2_cookies_dict)
heders = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'radar.itjuzi.com',
            'Referer':'http://radar.itjuzi.com///company?phpSessId=e65ca8471446469d5e68b8885ff06f67fc0d31db?phpSessId=d87230bfa03a3885aa4471da7ab09491948fff74',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',}
r3 = requests.post('http://radar.itjuzi.com/company/infonew?page=1', cookies=all_cookies, headers=headers, proxies=proxie)
print(r3.content)
