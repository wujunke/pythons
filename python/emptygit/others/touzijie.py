#coding=utf-8
import re
import urllib2
from bs4 import BeautifulSoup
import time
from random import choice



f = open('URLtext2','r')
urllist = f.readlines()
iplist=['118.1899.69.34','124.193.144.238','211.144.76.58','58.248.137.228']

def getInfo(url):
    def getHtml(url):
        ip = choice(iplist)
        proxy_support = urllib2.ProxyHandler({'https': 'https://' + ip})
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)

        page = urllib2.urlopen(url)
        html = page.read()
        return html

    html = getHtml(url)
    # print html

    def getTel(html):
        req = r'(<tr>\s*([\s\S]*?)\s*</tr>)'
        telre = re.compile(req)
        tel = re.findall(telre, html)
        return tel
    info = getTel(html)

    def getth1(detailinfo):
        req = r'<a target="_blank" href="http://zdb.pedaily.cn/enterprise/.*?>(.*?)</a>'
        telre = re.compile(req)
        tel = re.findall(telre, detailinfo)
        info = ''
        for item in tel:
            item = str(item) + ' / '
            info = info + item
        return '受资方 > ' + info + ';  '
    def getth2(detailinfo):
        req = r'<a target="_blank" href="http://zdb.pedaily.cn/company/.*?">(.*?)</a>'
        telre = re.compile(req)
        tel = re.findall(telre, detailinfo)
        info = ''
        for item in tel:
            item = str(item)+ ' / '
            info = info + item
        return '投资方 > ' + info + ';  '
    def getth3(detailinfo):
        req = r'<td class="td3">.*?>(.*?)</a></td>*'
        telre = re.compile(req)
        tel = re.findall(telre, detailinfo)
        info = ''
        for item in tel:
            item = str(item)+ ' / '
            info = info + item
        return '所属行业 > ' + info + ';  '

    def getth4(detailinfo):
        req = r'<td class="td4">(.*?)</td>*'
        telre = re.compile(req)
        tel = re.findall(telre, detailinfo)
        info = ''
        for item in tel:
            item = str(item) + ' '
            info = info + item
        return '投资金额 > ' + info + ';  '
    def getth5(detailinfo):
        req = r'<td class="td5">(.*?)</td>*'
        telre = re.compile(req)
        tel = re.findall(telre, detailinfo)
        info = ''
        for item in tel:
            item = str(item) + ' '
            info = info + item
        return '投资时间 > ' + info + ';  '

    def saveInfo(info):
        f = open('touzijie-inv22data', 'a')
        f.writelines(info)
        f.writelines('\n')
        f.close()

    for item in info:
        detailinfo = item[0]
        th1 = getth1(detailinfo)
        th2 = getth2(detailinfo)
        th3 = getth3(detailinfo)
        th4 = getth4(detailinfo)
        th5 = getth5(detailinfo)
        thinfo = th1 + th2 + th3 + th4 + th5
        saveInfo(thinfo)


for item in range(1,9,1):
    url = "http://zdb.pedaily.cn/inv/h2861/%d" % item
    getInfo(url)
    print 'page = %d' % item
    time.sleep(3)


