#coding=utf-8
import urllib
import cookielib
import requests
import re
import sys
import HTMLParser
from bs4 import BeautifulSoup
parser = HTMLParser.HTMLParser()
s = requests.session()
s.cookies = cookielib.LWPCookieJar('Hannovermesse')
heders = {
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Origin':'http://www.hannovermesse.de',
    'Referer':'http://www.hannovermesse.de/search',
    'Host':'www.hannovermesse.de',
    'Upgrade-Insecure-Requests':'1',
    'Cookie':'FILES=f01; ns_session=true; JSESSIONID=DFE1CCF412DAC23733228D7A41B39025; _gat=1; SRV=b08|V/oKQ; ns_cookietest=true; _ga=GA1.2.919461279.1474867052'
}
form_data = {
    'search':'medical',
    'typ':'',
    'searchSource':'sb'
}


url= 'http://www.hannovermesse.de/search'
url = url.decode(sys.stdin.encoding).encode("utf-8")
result = s.post(url,headers=heders,data=urllib.urlencode(form_data))
s.cookies.save()
# print s.cookies
html = result.text
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
a = 0
for itema in asd:
    a+=1
    print a
    print itema
    des = itema.find_all('h4', itemprop='name')
    print des[0].get_text()