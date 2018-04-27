#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import requests
from bs4 import BeautifulSoup


headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
# 'Referer':'https://www.zhihu.com/',
# 'X-Requested-With': 'XMLHttpRequest',
# 'Origin':'https://www.zhihu.com'
}

def login(username, password, kill_captcha):
    session = requests.session()
    _xsrf = BeautifulSoup(session.get('https://www.zhihu.com/#signin', headers=headers).content , "lxml").find('input', attrs={'name': '_xsrf'})['value']
    session.headers.update({'_xsrf':str(_xsrf)})
    #加入type=login 否则：ERR_VERIFY_CAPTCHA_SESSION_INVALID
    captcha_content = session.get('http://www.zhihu.com/captcha.gif?r=%d&type=login' % (time.time() * 1000), headers=headers).content
    data = {
        '_xsrf': _xsrf,
        'password': password,
        'captcha': kill_captcha(captcha_content),
        'email': username,
        'remember_me': 'true'
    }
    # print data
    resp = session.post('http://www.zhihu.com/login/email', data=data, headers=headers).content
    # 登录成功
    print 'resp\n',resp
    # assert r'\u767b\u5f55\u6210\u529f' in resp
    return session


def kill_captcha(data):
    with open('1.gif', 'wb') as fp:
        fp.write(data)
    return raw_input('captcha : ')

if __name__ == '__main__':
    session = login('wjk1397@163.com', '123921013le', kill_captcha)
    print BeautifulSoup(session.get("https://www.zhihu.com",headers=headers).content , "lxml").find('span', class_='name').getText()
