#coding=utf-8
import json
import random
import threading
import traceback

import requests
import time

from datetime import datetime

from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

from itjuzi_config import Cookie, base_url, token, insert_rate, find_rate, judgerepeat, temp_path_base, iplist2 ,iplist

import sys
reload(sys)
sys.setdefaultencoding('utf8')



def rand_proxie2():
    return {'http':'https://%s' % iplist2[random.randint(0, len(iplist)) - 1],
            'https':'https://%s' % iplist2[random.randint(0, len(iplist2)) - 1],}


headers2 = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Host':'www.itjuzi.com',
            'Referer':'http://radar.itjuzi.com/company',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Upgrade-Insecure-Requests':'1',
            'Cookie':Cookie,
}



# 公司详情
# url_company_detail_http = 'http://radar.itjuzi.com/company/'
url_company_detail_https = 'https://www.itjuzi.com/company/'

class InvestError(Exception):
    def __init__(self, msg):
        self.msg = msg



def timersleep():
    print datetime.now()
    time.sleep(find_rate)


class insetManager():
    def saveCompanyInfoToMongo(self, com_detail, com_fullname):
        dic = {}
        update = False
        if com_fullname:
            dic['com_name'] = com_fullname
            update = True
        if com_detail:
            dic['tags'] = com_detail.get('tags', [])
            dic['com_web'] = com_detail.get('com_web', None)
            dic['mobile'] = com_detail.get('mobile', None)
            dic['email'] = com_detail.get('email', None)
            dic['detailaddress'] = com_detail.get('detailaddress', None)
            news = com_detail['news']
            update = True
            self.saveCompanyNewsToMongo(news, dic['com_id'], dic.get('com_name'))
            self.saveCompanyIndustyInfoToMongo(com_detail)
        if update:
            dic['com_id'] = int(dic['com_id'])
            print  'com_id = %s ' % dic['com_id']
            res = requests.post(base_url + 'mongolog/proj', data=json.dumps(dic),
                                headers={'Content-Type': 'application/json', 'token': token}).content
            res = json.loads(res)
            if res['code'] == 1000:
                print '新增com--' + str(res['result'].get('com_id', None))
                pass
            elif res['code'] == 8001:

                print '重复company'
            else:
                print res


    def saveCompanyNewsToMongo(self,newslist,com_id=None,com_name=None):
        for news in newslist:
            if news.get('linkurl'):
                news['com_id'] = com_id if isinstance(com_id,int) else int(com_id)
                news['com_name'] = com_name
                res = requests.post(base_url + 'mongolog/projnews', data=json.dumps(news),
                                    headers={'Content-Type': 'application/json', 'token': token}).content
                res = json.loads(res)
                if res['code'] == 1000:
                    print '新增comnews--' + str(res['result'].get('com_id', None))
                    pass
                elif res['code'] == 8001:
                    pass
                    # repeat_count = repeat_count + 1
                    # brea
                    # print '重复company_news'
                else:
                    # print filepath
                    print '错误数据news----' + 'com_id=%s' % news['com_id']
                    print res
                    break

    def saveCompanyIndustyInfoToMongo(self,info):
        res = requests.post(base_url + 'mongolog/projinfo', data=json.dumps(info),
                            headers={'Content-Type': 'application/json', 'token': token}).content
        res = json.loads(res)
        if res['code'] == 1000:
            print '新增indus_info--' + str(res['result'].get('com_id', None))
            pass
        elif res['code'] == 8001:
            pass
        else:
            # print filepath
            print '错误数据indus_info----' + 'com_id=%s' % info['com_id']
            print res



def getCompanyDetail(com_id):
    num = 3  # 重试次数
    com_name = ''
    while num > 0:
        try:
            res = requests.get(url_company_detail_https + '%s' % com_id, headers=headers2, )
            html = res.content
        except ConnectionError:
            print '%s--Timeout, try again'%pox
            num -= 1
        else:
            print 'com_ok'
            break
    else:
        # 3次都失败
        print 'Try 3 times, But all failed'
        raise InvestError('连接失败，Try 3 times, But all failed')
    try:
        print html
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        titletag = soup.find('h1',class_='seo-important-title')
        if titletag:

            com_name = titletag.text.replace('\n', '').replace('\t', '')
            com_web = None
            a_s = soup.find('i', class_='fa fa-link t-small', )
            if a_s:
                com_web = a_s.parent['href']

            # 联系方式
            ll = ['mobile', 'email', 'detailaddress']
            response = {}
            response['com_id'] = int(com_id)
            contact_ul = soup.find('ul', class_='list-block aboutus')
            if contact_ul:
                for info in contact_ul.find_all('li'):
                    if info.find('i', class_='fa icon icon-phone-o'):
                        response['mobile'] = info.text.replace('\n', '').replace('\t', '')
                    if info.find('i', class_='fa icon icon-email-o'):
                        response['email'] = info.text.replace('\n', '').replace('\t', '')
                    if info.find('i', class_='fa icon icon-address-o'):
                        response['detailaddress'] = info.text.replace('\n', '').replace('\t', '')

            # 新闻
            res = soup.find_all('ul', class_='list-unstyled news-list')
            news = []
            for ss in res:
                lilist = ss.find_all('li')
                for li in lilist:
                    dic = {}
                    dic['newsdate'] = li.find('span', class_='news-date').text.replace('\n', '').replace('\t', '')
                    a = li.find('a', class_='line1')
                    dic['title'] = a.text.replace('\n', '').replace('\t', '')
                    dic['linkurl'] = a['href']
                    dic['newstag'] = li.find('span', class_='news-tag').text.replace('\n', '').replace('\t', '')
                    news.append(dic)
            response['news'] = news
            response['com_web'] = com_web

            # 竞品
            taglist = []
            compititoridlist = soup.find('div', class_='sub-titlebar detail-compete-info').find_all('a')
            for compititorid in compititoridlist:
                if compititorid:
                    if len(compititorid.text):
                        taglist.append(compititorid.text)
            response['tags'] = taglist
            # 工商信息
            # recruit-info
            recruit_info = soup.find('div', id='recruit-info')
            if recruit_info:
                tablistul = recruit_info.find('ul', class_='nav-tabs list-inline stock_titlebar')
                tablistli = tablistul.find_all('li')
                for tabli in tablistli:
                    tabhref = tabli.a['href'].replace('#', '')
                    if tabhref in ['indus_base', u'indus_base']:  # 基本信息
                        indus_base = recruit_info.find('div', id=tabhref)
                        company_name = indus_base.find('th').text
                        infolisttd = indus_base.find_all('td')
                        infodic = {}
                        for info in infolisttd:
                            if info:
                                if info.find('span', class_='tab_title') and info.find('span', class_='tab_main'):
                                    if info.find('span', class_='tab_title').text:
                                        infodic[info.find('span', class_='tab_title').text] = info.find('span',
                                                                                                        class_='tab_main').text.replace(
                                            '\n', '').replace('\t', '')
                        infodic[u'公司名称:'] = company_name.replace('\n', '').replace('\t', '')
                        response[tabhref] = infodic

                    if tabhref in ['indus_shareholder', u'indus_shareholder', 'indus_foreign_invest', u'indus_foreign_invest',
                                   'indus_busi_info', u'indus_busi_info']:  # 股东信息、企业对外投资信息、工商变更信息
                        indus_shareholder = recruit_info.find('div', id=tabhref)
                        thead = indus_shareholder.find('thead')
                        theadthlist = thead.find_all('th')
                        theadlist = []
                        for theaditem in theadthlist:
                            theadlist.append(theaditem.text)
                        tbody = indus_shareholder.find('tbody')
                        infolist = []
                        if tbody:
                            trlist = tbody.find_all('tr')
                            for tr in trlist:
                                infodic = {}
                                tdlist = tr.find_all('td')
                                for i in range(0, len(theadlist) - 1):
                                    infodic[theadlist[i]] = tdlist[i].text if tdlist[i].text else None
                                infolist.append(infodic)
                        response[tabhref] = infolist
        else:
            response = None
        return response, com_name
    except Exception:
        print 'xxxxxx'
        print traceback.format_exc()
        return None,   com_name





class Catch_Thread(threading.Thread):
        def __init__(self, url, startpage, endpage):
            self.url = url
            self.startpage = startpage
            self.endpage = endpage
            threading.Thread.__init__(self)
        def run(self):
            manager = insetManager()
            while True:
                aa = True
                page = self.startpage
                while aa:
                    try:
                        res = requests.get(base_url + 'mongolog/proj?page_index=%s'%page, headers={'Content-Type': 'application/json', 'token': token}).content
                        page += 1
                        if res:
                            data = json.loads(res)
                            if data['code'] in [1000, '1000', u'1000']:
                                projlist = data['result']['data']
                                if len(projlist) < 10:
                                    aa = False
                                for proj in projlist:
                                    com_id = proj['com_id']
                                    com_name = proj['com_name']
                                    com_detail, com_fullname = getCompanyDetail(com_id=com_id)
                                    if com_name == com_fullname:
                                        com_fullname = None
                                    manager.saveCompanyInfoToMongo(com_detail=com_detail,com_fullname=com_fullname)
                        if page > self.endpage:
                            aa = False
                    except Exception as err:
                        print err
                        print '*****'
                time.sleep(find_rate)

Catch_Thread(url_company_detail_https,startpage=1 ,endpage=9000).start()



