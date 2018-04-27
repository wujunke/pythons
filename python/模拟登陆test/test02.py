#coding=utf-8

import re
import requests
import cookielib
import urllib
import time
filename = 'linkedIncookie'
# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent,
    'Host':'www.linkedin.com',
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename)

# 访问 初始页面带上 cookie
index_url = "https://www.linkedin.com/hp"
try:
    session.cookies.load(filename=filename, ignore_discard=True)
except:
    session.get(index_url, headers=headers)
    session.cookies.save()

# for item in session.cookies:
#     print 'Cookie：Name = '+item.name
#     print 'Cookie：Value = '+item.value
time.sleep(3)

def getcookiestr(cookie):
    cookiestr = ''
    infopattern = re.compile(r'<Cookie (.*?) for')
    info = re.findall(infopattern, cookie)
    for item in info:
        cookiestr = cookiestr + str(item) + ';'
    # print 'cookiestr = %s'% cookiestr
    return cookiestr

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
           'Host':'www.linkedin.com',
           'X-LinkenIn-tranceDataContext':'X-LI-ORIGIN-UUID=Wc5ON8mtdRRgE5ISmCsAAA==',
           'Referer':'https://www.linkedin.com/?trk=baidubrand-mainlink',
           'Upgrade-Insecure-Requests': '1',
           'Connection':'keep-alive',
           'Cookie':getcookiestr(str(session.cookies)),
           'Origin':'https://www.linkedin.com'
          }
# print str(session.cookies)
def loginWeb(url, user, pwd):
    cookies = str(session.cookies)
    loginCsrfParam_pattern = re.compile(r'<Cookie bcookie="v=2&(.*?)" for .linkedin.com/>*')
    loginCsrfParam = re.findall(loginCsrfParam_pattern, cookies)[0]
    formValue = {'session_key': user,
                 'session_password': pwd,
                 'submit': '登录',
                 'isJsEnabled': 'false',
                 'loginCsrfParam': loginCsrfParam,
                 'trk': 'baidubrand-mainlink',
                 'sourceAlias': '0_7r5yezRXCiA_H0CRD8sf6DhOjTKUNps5xGTqeX8EEoi',
                }
    session.post(url, data=urllib.urlencode(formValue), headers=headers)
    print session.cookies
    session.get('http://www.linkedin.com/nhome')
    session.cookies.save()
    print session.cookies


if __name__ == '__main__':
    submit = 'https://www.linkedin.com/uas/login-submit'
    user = 'wjk1397@163.com'
    password = '123921013le'
    loginWeb(submit,user,password)
    # get_url = 'http://www.linkedin.com/vsearch/f?type=all&keywords=li+ning&orig=GLHD&rsid=&pageKey=nprofile_view_nonself&trkInfo=tarId%3A1474433924565&trk=global_header&search=%E6%90%9C%E7%B4%A2'
    # allow_redirects=False 禁止重定向
    # resp = session.get(get_url, headers=headers, allow_redirects=False)
    # print (resp.status_code) , resp.text
