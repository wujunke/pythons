#coding=utf-8
import cookielib
import requests
import re
import sys
import HTMLParser
parser = HTMLParser.HTMLParser()
s = requests.session()
s.cookies = cookielib.LWPCookieJar('领英')
heders = {
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Upgrade-Insecure-Requests':'1',
    'Referer':'http://www.linkedin.com/',
    'Host':'www.linkedin.com',
    'Cookie':'JSESSIONID="ajax:4639553405520871651"; bcookie="v=2&938c404b-bed0-40cb-8839-4bf9bf3d6d33"; visit="v=1&M"; _ga=GA1.2.1644338019.1474364419; VID=V_2016_09_20_02_1423; lidc="b=SGST04:g=1:u=1:i=1474509301:t=1474595701:s=AQEiKZkPmpR9Xxs1gU9MvMZQ3wBLmNpR"; lang="v=2&lang=zh-cn"; oz_props_fetch_size1_undefined=undefined; wutan=7ybiorCxReMqB3Wmwu2zQepjaIEsNTwNtkoPtneUsvc=; share_setting=PUBLIC; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; RT=s=1474509305880&r=http%3A%2F%2Fwww.linkedin.com%2Fuas%2Flogout%3Fsession_full_logout%3D%26csrfToken%3Dajax%253A7644466845550059404%26trk%3Dnav_account_sub_nav_signout; _gat=1; liap=true; li_at=AQEDAR-K07sFAhR7AAABV0-akXUAAAFXUAhudVEAsbgvAfX6MOVQgUEGoOSMEyabzZK_XZv6-0afhlEqWtOl5mz5E--6gMGhbzRP3_wDRgoYrBMwr3D1sgXFCiPQc0LT9aDhqP_EjN7wUAWzy5QVJqcn',
}


def getName(html):
    req = r'"fmt_canonicalName":"(.*?)",'
    try:
        name = re.findall(re.compile(req), html)[0]
        return name.replace('\u002d','-').replace('\u003cB\u003e','').replace('\u003c/B\u003e','').replace('&quot;','"')
    except:
        return 'no name'
def getdescription(html):
    req = r'"fmt_body":"(.*?)"}],'
    try:
        description = re.findall(re.compile(req),html)[0]
        return description.replace('\u002d','-').replace('\u003cB\u003e','').replace('\u003c/B\u003e','').replace('&quot;','"')
    except:
        return 'no description'
def getcount(html):
    req = r'"fmt_size":"(.*?)",'
    try:
        count = re.findall(re.compile(req),html)[0]
        return count.replace('\u002d','-')
    except:
        return 'no count'
def getindustry(html):
    req = r'"fmt_industry":"(.*?)",'
    try:
        industay = re.findall(re.compile(req),html)[0]
        return industay
    except:
        return 'no industay'
def getlocation(html):
    req = r'"fmt_location":"(.*?)",'
    try:
        location = re.findall(re.compile(req),html)[0]
        return location
    except:
        return 'no location'


#  f：全站   C:公司     P:会员
# url= 'https://www.linkedin.com/vsearch/f?keywords=夏艳&page_num=1'
# url= 'https://www.linkedin.com/vsearch/c?keywords=汽车之家&page_num=1'
# url= 'https://www.linkedin.com/vsearch/p?keywords=夏艳&page_num=1'
# 职位搜索
url= 'https://www.linkedin.com/jobs/search?keywords=工程师&page_num=1'
url = url.decode(sys.stdin.encoding).encode("utf-8")
result = s.get(url,headers=heders)
s.cookies.save()
# print s.cookies
html = result.text
print html
# req = r'({"company":.*?,"logoMediaId":.*?})'
req = r'{"company":(.*?)}},'
try:
    tes = re.findall(re.compile(req), html)
    for item in tes:
        name = getName(item)
        description = getdescription(item)
        location = getlocation(item)
        count = getcount(item)
        industry = getindustry(item)

        # print item
        print parser.unescape(name)
        # print description
        print location
        print count
        print industry + '\n'
except:
    print '这页没抓到东西'
