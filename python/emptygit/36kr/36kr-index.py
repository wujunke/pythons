#coding=utf-8
import json
import random
import traceback

import requests

from datetime import datetime
import time
import xlwt
from requests.exceptions import ConnectionError



import sys
reload(sys)
sys.setdefaultencoding('utf-8')



iplist = ['101.201.115.184:8080']

def rand_proxie():
    return {'http':'http://%s' % iplist[random.randint(0, len(iplist)) - 1],}

class InvestError(Exception):
    def __init__(self, msg):
        self.msg = msg

headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Host':'36kr.com',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
}
def getHtml(url):
    s = requests.Session()
    num = 3  # 重试次数
    while num > 0:
        try:
            s = requests.Session()
            print datetime.now()
            html = s.get(url, headers=headers, proxies=rand_proxie()).content
            print datetime.now()
        except ConnectionError:
            print 'Timeout, try again'
            # proxie =
            num -= 1
        else:
            # 成功获取
            print 'ok'
            break
    else:
        # 3次都失败
        print 'Try 3 times, But all failed'
        raise InvestError('连接失败，Try 3 times, But all failed')
    return html


def saveToExcel(path):
    res = open(path,'r').readlines()
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('A Test Sheet')
    ws.write(0, 0, 0)
    ws.write(0, 1, 'title')
    ws.write(0, 2, 'summary')
    ws.write(0, 3, 'published_at')
    ws.write(0, 4, 'extraction_tags')
    ws.write(0, 5, 'favorite')
    ws.write(0, 6, 'comment')
    hang = 1
    for row in res:
        row = json.loads(row)
        lie = 1
        ws.write(hang, 0, hang)
        ws.write(hang, lie + 0, row['title'])
        ws.write(hang, lie + 1, row['summary'])
        ws.write(hang, lie + 2, row['published_at'])
        ws.write(hang, lie + 3, row['extraction_tags'])
        ws.write(hang, lie + 4, row['favorite'])
        ws.write(hang, lie + 5, row['comment'])
        hang = hang + 1
    wb.save(path + '.xls')

def saveInfo(info,path):
    f = open(path, 'a+')
    f.writelines(info)
    f.writelines('\n')
    f.close()



b_id = ''

def getStart(b_id):
    try:
        url = 'http://36kr.com/api/info-flow/main_site/posts?column_id=&b_id=%s&per_page=20'%b_id
        print url
        res = getHtml(url)
        resdic = json.loads(res)
        if resdic['code'] == 0:
            data = resdic['data']['items']
            if isinstance(data,list) and len(data) > 0:
                print len(data)
                for dic in data:
                    res = {}
                    res['id'] = dic['id']
                    res['title'] = dic['title']
                    res['summary'] = dic['summary']
                    res['published_at'] = dic['published_at']
                    res['extraction_tags'] = dic['extraction_tags']
                    res['favorite'] = dic['counters']['favorite']
                    res['comment'] = dic['counters']['comment']
                    res['type'] = dic['column']['name']
                    info = json.dumps(res,ensure_ascii=False)
                    saveInfo(info, path='36kr2.txt')
                    b_id = dic['id']
        else:
            print res
        return b_id

    except Exception:
        print traceback.format_exc()
        return None
repeat = True
count = 1
while repeat:
    print count
    new_bid = getStart(b_id=b_id)
    if new_bid and new_bid != b_id:
        b_id = new_bid
    else:
        repeat = False
    count += 1
# saveToExcel('36kr')


# http://36kr.com/api/post?column_id=67&b_id=&per_page=20&_=1513069170263
# http://36kr.com/api/post?column_id=23&b_id=&per_page=20&_=1513069183847
# http://36kr.com/api/post?column_id=102&b_id=&per_page=20&_=1513069196334
# http://36kr.com/api/post?column_id=185&b_id=&per_page=20&_=1513069210598