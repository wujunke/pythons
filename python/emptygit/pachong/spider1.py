#coding=utf-8

# 模拟登陆爬取
from bs4 import BeautifulSoup
import requests

# 1. 获取token和cookie
r1 = requests.get(url='https://github.com/login')
s1 = BeautifulSoup(r1.text, 'html.parser')
val = s1.find(attrs={'name': 'authenticity_token'}).get('value')
# cookie返回给你
r1_cookie_dict = r1.cookies.get_dict()

# 发送用户认证
r2 = requests.post(
    url='https://github.com/session',
    data={
        'commit': 'Sign in',
        'utf8': '✓',
        'authenticity_token': val,
        'login': '',
        'password': ''
    },
    cookies=r1_cookie_dict
)

r2_cookie_dict = r2.cookies.get_dict()

print(r1_cookie_dict)
print(r2_cookie_dict)

all_cookies = {}

all_cookies.update(r1_cookie_dict)
all_cookies.update(r2_cookie_dict)

# 3.github直接用带token之后的cookies就行
print all_cookies
r3 = requests.get('https://github.com/settings/emails', cookies=all_cookies)
print(r3.text)