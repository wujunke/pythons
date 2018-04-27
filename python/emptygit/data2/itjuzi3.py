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

from itjuzi_config import Cookie, base_url, token, insert_rate, find_rate, page_size, iplist, judgerepeat, \
    temp_path_base, iplist2

import sys
reload(sys)
sys.setdefaultencoding('utf8')


def rand_proxie():
    return {'http':'http://%s' % iplist[random.randint(0, len(iplist)) - 1],}

def rand_proxie2():
    return {'https':'https://%s' % iplist2[random.randint(0, len(iplist2)) - 1],}

def rand_sleeptime():
    return random.randint(0, 5)

heders = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'radar.itjuzi.com',
            'Referer':'http://radar.itjuzi.com///company?phpSessId=e65ca8471446469d5e68b8885ff06f67fc0d31db?phpSessId=d87230bfa03a3885aa4471da7ab09491948fff74',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie':Cookie,
}


headers2 = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.itjuzi.com',
            'Referer':'http://radar.itjuzi.com/company',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie':Cookie,
}



#国内融资
url_invest_in = 'http://radar.itjuzi.com/investevent/info?location=in&orderby=def&page='
#国内并购
url_merge_in = 'http://radar.itjuzi.com/investevent/merg?location=in&orderby=def&page='
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


def getHtml(url):
    num = 3  # 重试次数
    while num > 0:
        try:
            s = requests.Session()
            print datetime.now()
            html = s.get(url, headers=heders, proxies=rand_proxie() ).content
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


def clearfile(path):
    f = open(path, 'r+')
    f.truncate()
    f.close()
    print '清理一次'

def saveInfo(info,path):
    f = open(path, 'a+')
    f.writelines(info)
    f.writelines('\n')
    f.close()
    print info

def getInfo(url,path):
    try:
        result = json.loads(getHtml(url))
        status = result['status']
        total = None
        if status == 1:
            total = result['data']['total']
	    print total
            total = int(total)
            for item in result['data']['rows']:
                thinfo = json.dumps(item)
		print item['invse_id']
                saveInfo(thinfo,path)
                # print thinfo
        elif status == 2:
            print '没有了，暂无数据'
        else:
            print '请求失败'
            print result
        return total
    except Exception as err:
        print err
	time.sleep(10)
        print '------'
        return None



def timersleep():
    print datetime.now()
    time.sleep(find_rate)


class insetManager():
    def saveMergeInfoToMongo(self,filepath):
        repeat_count = 0
        with open(filepath) as file:
            aaaa = 0
            for line in file:
                time.sleep(rand_sleeptime())
		dic = json.loads(line)
                dic['investormerge'] = 2
                dic['com_id'] = int(dic['com_id'])
                dic['merger_id'] = int(dic['merger_id'])
                aaaa = aaaa + 1
                print '开始新增'
		res = requests.post(base_url + 'mongolog/event', data=json.dumps(dic),
                                    headers={'Content-Type': 'application/json','token':token}).content
                res = json.loads(res)
		print '新增完成'
                if res['code'] == 1000:
                    print '新增merge--' + str(res['result'].get('merger_id', None))
                    pass
                elif res['code'] == 8001:
                    repeat_count = repeat_count + 1
                    # print '重复merge'
                    # break
                    # pass
                else:
                    print filepath
                    print '错误数据' + '第%s行' % aaaa 
		    print line
                    print res
                    # break
        return repeat_count


    def saveInvestInfoToMongo(self,filepath):
        repeat_count = 0
        with open(filepath) as file:
            aaaa = 0
            for line in file:
                time.sleep(rand_sleeptime())
                dic = json.loads(line)
                dic['investormerge'] = 1
                dic['com_id'] = int(dic['com_id'])
                dic['invse_id'] = int(dic['invse_id'])
                if isinstance(dic['invsest_with'], dict):
                    values = []
                    for key, value in dic['invsest_with'].items():
                        values.append(value)
                    dic['invsest_with'] = values
                aaaa = aaaa + 1
                res = requests.post(base_url + 'mongolog/event', data=json.dumps(dic),
                                    headers={'Content-Type': 'application/json','token':token}).content
                res = json.loads(res)
                if res['code'] == 1000:
                    print '新增invse--'+ str(res['result'].get('invse_id', None))
                    pass
                elif res['code'] == 8001:
                    repeat_count = repeat_count + 1
                    # break
                    # pass
                    # print '重复invest'
                else:
                    print filepath
                    print '错误数据' + '第%s行' % aaaa
            	    print line 
	            print res
            
        return repeat_count

    def saveCompanyInfoToMongo(self, filepath):
        repeat_count = 0
        with open(filepath) as file:
            aaaa = 0
            for line in file:
                time.sleep(rand_sleeptime())
                aaaa = aaaa + 1
                dic = json.loads(line)
          #      com_detail,com_fullname = getCompanyDetail(dic['com_id'])
           #     if com_fullname:
            #        dic['com_name'] = com_fullname
             #   if com_detail:
              #      dic['tags'] = com_detail.get('tags',[])
               #     dic['com_web'] = com_detail.get('com_web',None)
                #    dic['mobile'] = com_detail.get('mobile',None)
                 #   dic['email'] = com_detail.get('email', None)
                  #  dic['detailaddress'] = com_detail.get('detailaddress', None)
                   # news = com_detail['news']
                   # self.saveCompanyNewsToMongo(news, dic['com_id'],dic.get('com_name'))
                   # self.saveCompanyIndustyInfoToMongo(com_detail)
                dic['com_id'] = int(dic['com_id'])
                res = requests.post(base_url + 'mongolog/proj', data=json.dumps(dic),
                                    headers={'Content-Type': 'application/json', 'token': token}).content
                res = json.loads(res)
                if res['code'] == 1000:
                    print '新增com--' + str(res['result'].get('com_id', None))
                    pass
                elif res['code'] == 8001:
                    repeat_count = repeat_count + 1
                    # break
                    # pass
                    # print '重复company'
                else:
                    print filepath
                    print '错误数据' + '第%s行' % aaaa
                    print res
                   
        return repeat_count

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
                    # repeat_count = repeat_count + 1
                    # break
                    pass
                    # print '重复company'
                else:
                    # print filepath
                    print '错误数据news----' + 'com_id=%s' % news['com_id']
                    print res
                   
    def saveCompanyIndustyInfoToMongo(self,info):
        res = requests.post(base_url + 'mongolog/projinfo', data=json.dumps(info),
                            headers={'Content-Type': 'application/json', 'token': token}).content
        res = json.loads(res)
        if res['code'] == 1000:
            print '新增indus_info--' + str(res['result'].get('com_id', None))
        else:
            print '错误数据indus_info----' + 'com_id=%s' % info['com_id']
            print res



def getCompanyDetail(com_id):
    num = 3  # 重试次数
    com_name = ''
    while num > 0:
        try:
            pox = rand_proxie2()
            r = requests.get(url_company_detail + '%s' % com_id, headers=headers2, proxies=pox) 
            html = r.content
        except ConnectionError:
            print 'Com timeout, try again'
            num -= 1
        else:
            print 'com_ok'
	    print r.elapsed.microseconds
            break
    else:
        # 3次都失败
        print 'Com try 3 times, But all failed'
        raise InvestError('连接失败，Try 3 times, But all failed')
    try:
       # print html
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        com_name = soup.find('h1',class_='seo-important-title').text.replace('\n', '').replace('\t', '')
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
        return response, com_name
    except Exception:
        print 'xxxxxx'
        print traceback.format_exc()
        return None,   com_name



class Catch_Thread(threading.Thread):
    def __init__(self, url, path, content, type , startpage, endpage):
        self.url = url
        self.path = path
        self.content = content
        self.type = type
        self.startpage = startpage
        self.endpage = endpage
        threading.Thread.__init__(self)

    def run(self):
        manager = insetManager()
        while True:
            aa = True
            page = 1
            while aa:
                try:
                    clearfile(self.path)
                    getInfo(self.url + str(page), self.path)
                    if self.type == 1:
                        manager.saveInvestInfoToMongo(self.path)
                    elif self.type == 2:
                         manager.saveMergeInfoToMongo(self.path)
                    else:
                        manager.saveCompanyInfoToMongo(self.path)
                    print self.content + 'page = %d' % page
                    page += 1
                    if judgerepeat:
                        if page > 10:
                            aa = False
                            print datetime.now()
                            print self.content + '终止请求page = %d' % page
                        else:
                            repeat_page = 0
                    if page > self.endpage:
                        aa = False
                        print datetime.now()
                        print self.content + '请求结束，终止page = %d' % page
                except Exception as err:
                    print err
                    print '*****'
            time.sleep(find_rate)


Catch_Thread(url_invest_in, temp_path_base + 'invest_in', '国内投资',1, startpage=1 ,endpage=2000).start()
#Catch_Thread(url_invest_out, temp_path_base + 'invest_out', '国外投资', 1, startpage=1 ,endpage=500).start()
#Catch_Thread(url_merge_in, temp_path_base + 'merge_in', '国内并购', 2, startpage=1 ,endpage=70).start()
#Catch_Thread(url_merge_out, temp_path_base + 'merge_out', '国外并购', 2, startpage=1 ,endpage=50).start()
#Catch_Thread(url_com, temp_path_base + 'company_in', '国内公司', 3 , startpage=1 ,endpage=3000).start()
#Catch_Thread(url_com_out, temp_path_base + 'company_out', '国外公司', 3, startpage=1 ,endpage=200).start()



#Catch_Thread(url_invest_in, temp_path_base + 'invest_in', '国内投资',1, startpage=1 ,endpage=200).start()
#Catch_Thread(url_invest_out, temp_path_base + 'invest_out', '国外投资', 1, startpage=1 ,endpage=100).start()
#Catch_Thread(url_merge_in, temp_path_base + 'merge_in', '国内并购', 2, startpage=1 ,endpage=100).start()
#Catch_Thread(url_merge_out, temp_path_base + 'merge_out', '国外并购', 2, startpage=1 ,endpage=100).start()
#Catch_Thread(url_com, temp_path_base + 'company_in', '国内公司', 3 , startpage=1 ,endpage=100).start()
#Catch_Thread(url_com_out, temp_path_base + 'company_out', '国外公司', 3, startpage=1 ,endpage=50).start()


