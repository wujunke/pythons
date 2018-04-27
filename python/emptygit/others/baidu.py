#coding:utf-8
import urllib
import cookielib
import requests
import re
import sys
import HTMLParser
from bs4 import BeautifulSoup
parser = HTMLParser.HTMLParser()
s = requests.session()
s.cookies = cookielib.LWPCookieJar('baiducookies')
heders = {
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Host':'www.baidu.com',
    'Cookie':'BAIDUID=0BC59FA7F2039E19470869C930CD0815:FG=1; BIDUPSID=0BC59FA7F2039E19470869C930CD0815; PSTM=1480386798; BDRCVFR[AjWLOTlvo0C]=mk3SLVN4HKm; BD_CK_SAM=1; PSINO=5; H_PS_PSSID=; B64_BOT=1'
}
url= 'http://www.baidu.com/s?ie=utf-8' \
     '&wd=烯牛数据' \
     '&rqlang=cn'
url = url.decode(sys.stdin.encoding).encode("utf-8")
result = s.get(url)

s.cookies.save()
# print s.cookies
html = result.text
print html
# print html
# req = r'(<h4 itemprop="name">.*?</h4>)'
# try:
#     tes = re.findall(re.compile(req), html)
#     for item in tes:
#         print item
# except:
#     print '这页没抓到东西'
soup = BeautifulSoup(html, 'html.parser')
# print soup
# des = soup.find_all('h4' , itemprop='name' )
asd = soup.find_all('a', itemprop='url', class_=re.compile(r"eventlist-link"))
# for item in des:
#     print item.get_text()
