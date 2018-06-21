#coding=utf-8
import json
import threading
import traceback
import requests
import time
import random
from datetime import datetime
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import sys



reload(sys)
sys.setdefaultencoding('utf8')


# 存储地址
base_url = 'https://api.investarget.com/'

#it桔子Cookie
Cookie =  'acw_tc=AQAAAAcaelkdyggAXQ2or++LwDKVoGo9; gr_user_id=a64916ec-575e-4962-a58c-f1e27b27b457; _gat=1; MEIQIA_EXTRA_TRACK_ID=162hb7jpnp3GiecPKB5GJJ8lACe; identity=18616837957%40test.com; remember_code=dmjJwbKdFS; unique_token=439977; paidtype=vip; _ga=GA1.2.1545006483.1529044671; _gid=GA1.2.419480130.1529044671; gr_session_id_eee5a46c52000d401f969f4535bdaa78=123d9b67-738a-431a-8699-75f1af66a76a_true; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1529044671; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1529044685; session=49b5143893120232d53a614b60ec911b8322092b'
#API新增token
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
#线程sleep间隔
find_rate = 36000
#http代理
iplist1 = ['140.205.222.3:80']




def rand_proxie_http():
    ip_port = iplist1[random.randint(0, len(iplist1)) - 1]
    return {
            # 'http':'http://%s' % ip_port,
            'https': 'https://%s' % '123.152.37.195:2682',
            }

def rand_sleeptime():
    return random.randint(0, 5)

headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'radar.itjuzi.com',
            'Referer':'http://radar.itjuzi.com///company?phpSessId=e65ca8471446469d5e68b8885ff06f67fc0d31db?phpSessId=d87230bfa03a3885aa4471da7ab09491948fff74',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',

}


headers2__company = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.itjuzi.com',
            'Referer':'https://www.itjuzi.com/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
}



#国内融资
url_invest_in = 'http://radar.itjuzi.com/investevent/info?location=in&orderby=def&page='
#国内并购
url_merge_in = 'http://radar.itjuzi.com/investevent/merg?location=in&orderby=merger_id&page='
#国外融资
url_invest_out = 'http://radar.itjuzi.com/investevent/info?location=out&orderby=def&page='
#国外并购
url_merge_out = 'http://radar.itjuzi.com/investevent/merg?location=out&orderby=def&page='
#公司信息
url_com = 'http://radar.itjuzi.com/company/infonew?page='
#国外公司
url_com_out = 'http://radar.itjuzi.com/company/infonew?prov%5B%5D=%E5%9B%BD%E5%A4%96&page='

# 公司详情
url_company_detail = 'https://www.itjuzi.com/company/'


class InvestError(Exception):
    def __init__(self, msg):
        self.msg = msg


def getHtml(url, cookie):
    num = 3  # 重试次数
    while num > 0:
        try:
            headers['Cookie'] = cookie
            s = requests.Session()
            print datetime.now()
            proxy = rand_proxie_http()
            html = s.get(url, headers=headers, proxies=proxy).content
            print datetime.now()
        except ConnectionError:
            print 'Timeout, try again'
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


def getInfo(url, cookie):
    try:
        result = json.loads(getHtml(url, cookie))
        status = result['status']
        if status == 1:
            return result['data']['rows']
        elif status == 2:
            return None
        else:
            print '请求失败'
            time.sleep(5)
            return getInfo(url, cookie)
    except Exception as err:
        print 'error------%s' % err.message
        time.sleep(5)
        return getInfo(url, cookie)

class insetManager():

    def __init__(self, token, cookie):
        self.token = token
        self.cookie = cookie

    def saveCompanyInfoToMongo(self, com_list):
        for dic in com_list:
            com_detail, com_fullname = self.getCompanyDetail(dic['com_id'])
            if com_fullname:
                if (u'未找到' in com_fullname or u'403' in com_fullname or u'www.itjuzi.com' in com_fullname):
                    pass
                else:
                    dic['com_name'] = com_fullname.split('(')[0]
            if com_detail:
                dic['tags'] = com_detail.get('tags', [])
                dic['com_web'] = com_detail.get('com_web', None)
                dic['mobile'] = com_detail.get('mobile', None)
                dic['email'] = com_detail.get('email', None)
                dic['detailaddress'] = com_detail.get('detailaddress', None)
                news = com_detail['news']
                self.saveEventToMongo(com_detail['events'], dic['com_id'])
                self.saveCompanyNewsToMongo(news, dic['com_id'], dic.get('com_name'))
                self.saveCompanyIndustyInfoToMongo(com_detail)
            dic['com_name'] = dic['com_name'] + '...'
            dic['com_id'] = int(dic['com_id'])
            res = requests.post(base_url + 'mongolog/proj', data=json.dumps(dic),
                                headers={'Content-Type': 'application/json', 'token': self.token}).content
            res = json.loads(res)
            if res['code'] == 1000:
                print '新增com--' + str(res['result'].get('com_id', None))
                pass
            elif res['code'] == 8001:
                pass
            else:
                print '错误event数据--%s' % repr(dic)
                print res

    def saveEventToMongo(self, events, com_id):
        for event in events:
            event['com_id'] = com_id
            res = requests.post(base_url + 'mongolog/event', data=json.dumps(event),
                               headers={'Content-Type': 'application/json', 'token': self.token}).content
            res = json.loads(res)
            if res['code'] == 1000:
                print '新增invse--' + str(res['result'].get('invse_id', None))
            elif res['code'] == 8001:
                print '重复invest'
            else:
                print '错误event数据--%s' % repr(event)
                print res


    def saveCompanyNewsToMongo(self,newslist,com_id=None,com_name=None):
        for news in newslist:
            if news.get('linkurl'):
                news['com_id'] = com_id if isinstance(com_id,int) else int(com_id)
                news['com_name'] = com_name
                res = requests.post(base_url + 'mongolog/projnews', data=json.dumps(news),
                                    headers={'Content-Type': 'application/json', 'token': self.token}).content
                res = json.loads(res)
                if res['code'] == 1000:
                    print '新增comnews--' + str(res['result'].get('com_id', None))
                    pass
                elif res['code'] == 8001:
                    pass
                else:
                    print '错误数据news----' + 'com_id=%s' % news['com_id']
                    print res
                   
    def saveCompanyIndustyInfoToMongo(self,info):
        res = requests.post(base_url + 'mongolog/projinfo', data=json.dumps(info),
                            headers={'Content-Type': 'application/json', 'token': self.token}).content
        res = json.loads(res)
        if res['code'] == 1000:
            print '新增indus_info--' + str(res['result'].get('com_id', None))
        else:
            print '错误数据indus_info----' + 'com_id=%s' % info['com_id']
            print res



    def getCompanyDetail(self, com_id):
        num = 3  # 重试次数
        com_name = ''
        while num > 0:
            try:
                pox = rand_proxie_http()
                headers2__company['Cookie'] = self.cookie
                s = requests.Session()
                r = s.get(url_company_detail + '%s' % com_id, headers=headers2__company, proxies=pox)
                html = r.content
            except ConnectionError:
                print 'Com_detail timeout, try again'
                num -= 1
            else:
                print 'com_ok'
                print r.elapsed.microseconds
                break
        else:
            # 3次都失败
            print 'Com_detail try 3 times, But all failed'
            raise InvestError('连接失败，Try 3 times, But all failed')
        try:
            # print html
            soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
            com_name = soup.find('h1', class_='seo-important-title').text.replace('\n', '').replace('\t', '')
            com_web = None
            a_s = soup.find('i', class_='fa fa-link t-small', )
            if a_s:
                com_web = a_s.parent['href']

            # 联系方式
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
            else:
                pass

            #融资信息
            investents = soup.find(id='invest-portfolio')
            eventtable = investents.find('table')
            eventtrlist = eventtable.find_all('tr')
            eventlist = []
            for eventtr in eventtrlist:
                if eventtr.find(class_='date'):
                    date = eventtr.find(class_='date').text
                    round = eventtr.find(class_='round').text
                    money = eventtr.find(class_='finades').text

                    link = eventtr.find(class_='finades').a['href']
                    type = link.split('/')[-2]
                    event_id = link.split('/')[-1]
                    data = {
                        'date': date,
                        'round': round,
                        'money': money,
                    }
                    if type == 'merger':
                        data['investormerge'] = 2
                        data['merger_id'] = event_id
                        data['merger_with'] = eventtr.find('a', class_='line1 c-gray').text if eventtr.find('a',
                                                                                                            class_='line1 c-gray') else ''
                    else:
                        data['investormerge'] = 1
                        data['invse_id'] = event_id
                        line1s = eventtr.find_all('a', class_='line1')
                        invsest_with = []
                        for line1 in line1s:
                            url = line1.get('href', None)
                            invst_name = line1.text
                            invsest_with.append({'url': url, 'invst_name': invst_name})
                        data['invsest_with'] = invsest_with
                    eventlist.append(data)
            response['events'] = eventlist

            # 团队信息
            members = []
            membersul = soup.find('ul', class_='list-unstyled team-list limited-itemnum')
            if membersul:
                lilist = membersul.find_all('li')
                for li in lilist:
                    dic = {}
                    dic['姓名'] = li.find('a', class_='person-name').text.replace('\n', '').replace('\t', '') if li.find('a',
                                                                                                                       class_='person-name') else None
                    dic['职位'] = li.find('div', class_='per-position').text.replace('\n', '').replace('\t', '') if li.find(
                        'div', class_='per-position') else None
                    dic['简介'] = li.find('div', class_='per-des').text.replace('\n', '').replace('\t', '') if li.find('div',
                                                                                                                     class_='per-des') else None
                    members.append(dic)
            response['indus_member'] = members


            # 新闻
            res = soup.find_all('ul', class_='list-unstyled news-list')
            news = []
            for ss in res:
                lilist = ss.find_all('li')
                for li in lilist:
                    dic = {}
                    dic['newsdate'] = li.find('span', class_='news-date').text.replace('\n', '').replace('\t',
                                                                                                         '') if li.find(
                        'span', class_='news-date') else None
                    a = li.find('a', class_='line1')
                    dic['title'] = a.text.replace('\n', '').replace('\t', '')
                    dic['linkurl'] = a['href']
                    dic['newstag'] = li.find('span', class_='news-tag').text.replace('\n', '').replace('\t', '') if li.find(
                        'span', class_='news-tag') else None
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

                    if tabhref in ['indus_shareholder', u'indus_shareholder', 'indus_foreign_invest',
                                   u'indus_foreign_invest',
                                   'indus_busi_info', u'indus_busi_info']:  # 股东信息、企业对外投资信息、工商变更信息
                        indus_shareholder = recruit_info.find('div', id=tabhref)
                        thead = indus_shareholder.find('thead')
                        theadlist = []
                        infolist = []
                        if thead:
                            theadthlist = thead.find_all('th')
                            for theaditem in theadthlist:
                                theadlist.append(theaditem.text)
                            tbody = indus_shareholder.find('tbody')
                            if tbody:
                                trlist = tbody.find_all('tr')
                                for tr in trlist:
                                    infodic = {}
                                    tdlist = tr.find_all('td')
                                    for i in range(0, len(theadlist) - 1):
                                        infodic[theadlist[i]] = tdlist[i].text if tdlist[i].text else None
                                    infolist.append(infodic)
                        response[tabhref] = infolist
            return response, com_name
        except Exception:
            print 'xxxxxx'
            print traceback.format_exc()
            return None,   com_name



class Catch_Thread(threading.Thread):
        def __init__(self, cookie, token,  url, content, utype , startpage, endpage):
            self.url = url
            self.cookie = cookie
            self.content = content
            self.type = utype
            self.token = token
            self.startpage = startpage
            self.endpage = endpage
            threading.Thread.__init__(self)

        def run(self):
            manager = insetManager(token=self.token, cookie=self.cookie)
            while True:
                aa = True
                page = self.startpage
                while aa:
                    try:
                        info = getInfo(self.url + str(page), self.cookie)
                        if info:
                            manager.saveCompanyInfoToMongo(info)
                        print self.content + 'page = %d' % page
                        page += 1
                        if page > self.endpage:
                            aa = False
                            print datetime.now()
                            print self.content + '请求结束，终止page = %d' % page
                    except Exception as err:
                        print err
                        print '*****'
                time.sleep(find_rate)



# Catch_Thread(Cookie, token, url_com, '国内公司', 3 , startpage=104 , endpage=110).start()
Catch_Thread(Cookie, token, url_com_out, '国外公司', 3, startpage=7 ,endpage=10).start()





