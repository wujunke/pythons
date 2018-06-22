#coding=utf-8
import json
import random
import urllib

import datetime
import requests
import time
import sys



reload(sys)
sys.setdefaultencoding('utf-8')
url = ' https://rong.36kr.com/n/api/column/0/company?sortField=HOT_SCORE'




# base_url = 'http://192.168.1.251:8080/'
# token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'
base_url = 'https://api.investarget.com/'
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
headers = {'Content-Type': 'application/json', 'token': token}

iplist = [
          '115.229.112.82:9000',
          ]


# &createtime=2018-06-12T11:51:00
def getSearchCompany(page):
    com_list = []
    res = requests.get(base_url + 'mongolog/proj/search?page_index=%s&createtime=2018-06-12T00:00:00' % page , headers=headers).content
    res = json.loads(res)
    if res['code'] == 1000:
        data = res['result']['data']
        if len(data) > 0:
            com_list.extend(data)
    return com_list







saltfactor = 111234567890


phrase_round = {
    'NONE': '尚未获投',
    'SEED': '种子轮',
    'ANGEL': '天使轮',
    'PRE_A': 'Pre-A轮',
    'A': 'A轮',
    'A_PLUS': 'A+轮',
    'PRE_B': 'Pre-B轮',
    'B': 'B轮',
    'B_PLUS': 'B+轮',
    'C': 'C轮',
    'C_PLUS': 'C+轮',
    'D': 'D轮',
    'E': 'E轮',
    'INFORMAL':'战略投资',
    'ACQUIRED':'并购',
    'AFTER_IPO':'上市后',
    'IPO': '上市',
}



url_base = 'https://rong.36kr.com/n/api/company/'
referer = 'https://rong.36kr.com/landing/detail?type=company&sortField=MATCH_RATE&kw='



url_finance = 'https://rong.36kr.com/n/api/company/%s/finance'   #融资历史
url_combase = 'https://rong.36kr.com/n/api/company/%s'           #公司基本信息
url_member = 'https://rong.36kr.com/n/api/company/%s/member'     #创始团队
url_news= 'https://rong.36kr.com/n/api/company/%s/news'          #公司新闻



jingzhun_headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'br, gzip, deflate',
    'Accept-Language': 'zh-cn',
    'X-Tingyun-Id':'Dio1ZtdC5G4;r=59479200',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'rong.36kr.com',
    'Referer': 'https://rong.36kr.com/list/detail&?sortField=HOT_SCORE',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'Z-XSRF-TOKEN=eyJpdiI6Im0wU1JnRVdNTWJESCsxUHQ4dGFMYkE9PSIsInZhbHVlIjoiOVdaMDdrNFZyQjcrb29RRjlNSzJvM3l5RFh5cm5wY2ZqSURjYW82ZXN1ZHVFdzVjK2ZNRW5xY3JSbWVNeWo0MmFOYVNQK09XT2ZpMkc2YXc1Z3g1cEE9PSIsIm1hYyI6ImY5ZGY1MTFiYmVlYjY4YWViNDcyMTk3NjAyZDU4MzgzMjBhZWEwMmI4MWFmNGQ4ZDhiYTYzNmMxNGUxYjliNTkifQ%3D%3D; krchoasss=eyJpdiI6IjB3a1MrYm9zcVUwQ1h1aGNJZGNmQmc9PSIsInZhbHVlIjoiSHZZRmwyeGlyUnYzWkJFZ3JKQlg3cjVzUlgrRzM5R0lkR2ZneGRtVGdaVFwvUDUyN0RwcTJ2ekJiTEdvSnlRaWJVaUVaZmlzU3hSUHZzRk1MRnVNTVwvZz09IiwibWFjIjoiMDQ2Y2NmYmM5ZDVmODQ3YzlkY2U3NzFjZTUyMDE2OWYzN2NlMTYwZTgxZDc1MmQ3YTI0MTcxYjk2MTAwNjUxYiJ9; MEIQIA_EXTRA_TRACK_ID=152CCejE5FvZOExdNT5VaiQnC2S; MEIQIA_VISIT_ID=16Mnh89bolXrtOUdsjR2uzf3rud; krid_user_id=817177228; krid_user_version=2; M-XSRF-TOKEN=8809b9570e47a600d14b9019a804da7d20639ecc3c999fea8ebd0445e721df9a; device-uid=086c2c10-75fe-11e8-ad9f-27eb44ae713f; krnewsfrontss=1e785e1cc935aea1c7411de4d1357725; Hm_lpvt_e8ec47088ed7458ec32cde3617b23ee3=1529659455; Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3=1528427129,1528685104,1528855758,1529659455; kr_plus_id=817177228; kr_plus_token=BuoIudOZORDzoAxQdI746P284NH8i2bMb28_____; kr_plus_utype=0; acw_tc=AQAAAEAd6kVxpwkAXXiptOaxTv2wN9vb; _kr_p_se=4fb266ce-d902-4495-892a-a47d8cae28d4; download_animation=1; kr_stat_uuid=y5Rtm25480929'
}



def getFinance(jingzhun_id, kw):
    finances = []
    url = url_base + str(jingzhun_id) + '/finance'
    jingzhun_headers['Referer'] = referer + kw
    res = requests.get(url, headers=jingzhun_headers, proxies=proxy).content
    res = json.loads(res)
    if res['code'] == 0:
        if len(res['data']) > 0:
            for finance in res['data']:
                invsest_with = []
                invse_id = None
                for invsest in finance.get('participantVos', []):
                    invse_id = int(invsest['investmentId']) + saltfactor
                    invsest_with.append({
                        'url':'',
                        'invst_name': invsest.get('entityName'),
                    })
                data = {
                    'com_id': int(jingzhun_id) + saltfactor,
                    'invse_id': invse_id,
                    'invsest_with': invsest_with,
                    'currency': finance.get('financeAmountUnit'),    #货币类型
                    'date': str(datetime.datetime.fromtimestamp(finance['financeDate']/1000))[:10]  if finance.get('financeDate') else None,
                    'money': finance.get('financeAmount'),
                    'investormerge': 1,
                    'round': phrase_round.get(finance.get('phase', '其他')),
                }
                finances.append(data)
    return finances


def getCombase(jingzhun_id, kw):
    combase = None
    url = url_base + str(jingzhun_id)
    jingzhun_headers['Referer'] = referer + kw
    res = requests.get(url, headers=jingzhun_headers, proxies=proxy).content
    res = json.loads(res)
    if res['code'] == 0:
        combase = res['data']
    return combase

def getMembers(jingzhun_id, kw):
    '''
    "intro": 简介
    "name": 姓名
    "position": 职位,
    :return:
    '''
    members = None
    url = url_base + str(jingzhun_id) + '/member'
    jingzhun_headers['Referer'] = referer + kw
    res = requests.get(url, headers=jingzhun_headers, proxies=proxy).content
    res = json.loads(res)
    if res['code'] == 0:
        if len(res['data']['members']) > 0:
            members = res['data']['members']
    return members

def getNews(jingzhun_id, kw):
    news = []
    url = url_base + str(jingzhun_id) + '/news'
    jingzhun_headers['Referer'] = referer + kw
    res = requests.get(url, headers=jingzhun_headers, proxies=proxy).content
    res = json.loads(res)
    if res['code'] == 0:
        if len(res['data']) > 0:
            for new in res['data']:
                data = {
                    'com_id' : int(jingzhun_id) + saltfactor,  # 公司id
                    # 'com_name' : new[''],  # 公司名称
                    'title' : new.get('title'),
                    'linkurl' : new.get('newsUrl'),
                    'newsdate' : new.get('publishDateStr'),
                }
                news.append(data)
    return news

def saveCompanyNewsToMongo(newslist,com_name=None):
    for news in newslist:
        if news.get('linkurl'):
            news['com_id'] = news['com_id'] if isinstance(news['com_id'], int) else int(news['com_id'])
            news['com_name'] = com_name
            res = requests.post(base_url + 'mongolog/projnews', data=json.dumps(news),
                                headers=headers).content
            res = json.loads(res)
            if res['code'] == 1000:
                print '新增comnews--' + str(res['result'].get('com_id', None))
                pass
            elif res['code'] == 8001:
                pass
            else:
                print res
                break


def saveInvestInfoToMongo(event_list, event_id_none_count):
    for event_data in event_list:
        if not event_data['invse_id']:
            event_data['invse_id'] = saltfactor - event_id_none_count
            event_id_none_count += 1
        res = requests.post(base_url + 'mongolog/event', data=json.dumps(event_data),
                            headers=headers).content
        res = json.loads(res)
        if res['code'] == 1000:
            print '新增invse--' + str(res['result'].get('invse_id', None))
        elif res['code'] == 8001:
            print '重复invest'
        else:
            print res
    return event_id_none_count

def saveCompanyToMongo(com_data):
    res = requests.post(base_url + 'mongolog/proj', data=json.dumps(com_data),
                                    headers=headers).content
    res = json.loads(res)
    if res['code'] == 1000:
        print '新增com--' + str(res['result'].get('com_id', None))
    elif res['code'] == 8001:
        print '重复company'
    else:
        print res


jingzhun_search_url = 'https://rong.36kr.com/n/api/search/company?kw='
proxy = {'http':'http://118.212.137.135:31288'}

event_id_none_count = 18    #系数 -  none_count = none_id

for page in range(1, 100):

    projlist = getSearchCompany(page)
    for proj in projlist:
        kw = urllib.quote(proj['com_name'].decode(sys.stdin.encoding).encode('utf8'))
        search_url = 'https://api.investarget.com/mongolog/proj/simple?com_name=' + proj['com_name']
        res = requests.get(search_url, headers=headers).content
        res = json.loads(res)
        print 'page=%s, search_name=%s'%(page, proj['com_name'])
        if res['code'] == 1000:
            if len(res['result']['data']) == 0:
                time.sleep(30)
                res = requests.get(jingzhun_search_url + kw, headers=jingzhun_headers, proxies=proxy).content
                res = json.loads(res)
                pagedata = res['data']
                datalist = pagedata['pageData']['data']
                count = 0
                for com in datalist:
                    count += 1
                    if count > 3:
                        break
                    if com['phase'] not in ['NONE', u'NONE']:
                        time.sleep(8)
                        jingzhun_id = com['id']
                        tagss = com.get('tags',[])
                        tags = []
                        for tag in tagss:
                            if '报道' not in tag and u'报道' not in tag:
                                tags.append(tag)
                        data = {
                            'com_id': int(jingzhun_id) + saltfactor,
                            'com_name': com['name'],
                            'com_status': '运营中',
                            'com_scale':'',   #公司规模
                            'com_web': '',     #公司网站
                            'com_cat_name': com.get('industryStr'),     #行业
                            'com_sub_cat_name': '',    #子行业
                            'com_born_date': str(datetime.datetime.fromtimestamp(com['startDate']/1000))[:10] if com.get('startDate') else None,   #成立日期
                            'invse_detail_money': '',     #最新融资金额
                            'guzhi': '',                 #估值
                            'invse_date': '',        #最新融资日期
                            'com_logo_archive': '',   #公司logo
                            'com_fund_needs_name': '',     #融资需求
                            'com_des': '',         #公司介绍
                            'invse_total_money': '',    #融资总额
                            'com_addr': com.get('cityStr').replace('省', '').replace('市', '').replace('自治区', '') if com.get('cityStr') else None,     #公司所在地
                            'mobile': '',     # 公司联系方式
                            'email': '',       # 公司邮箱
                            'detailaddress': '',  # 公司地址
                            'tags': tags,       #公司标签
                            'source':2,  #用2来表示鲸准 ，空或者1表示it桔子
                        }
                        search_url = 'https://api.investarget.com/mongolog/proj/simple?com_name=' + com['name']
                        res = requests.get(search_url, headers=headers).content
                        res = json.loads(res)
                        if res['code'] == 1000:
                            if len(res['result']['data']) == 0:
                                # print '不存在--%s' % com['name']
                                time.sleep(10)
                                combase = getCombase(jingzhun_id, kw)
                                data['com_scale'] = combase.get('scale')
                                data['com_des'] = combase.get('intro')
                                data['com_logo_archive'] = combase.get('logo')
                                data['detailaddress'] = combase.get('address2Desc', None)
                                data['com_web'] = combase.get('website')
                                saveCompanyToMongo(data)
                                investlist = getFinance(jingzhun_id, kw)
                                event_id_none_count = saveInvestInfoToMongo(investlist, event_id_none_count)
                                print 'event_id_none_count = %s' % event_id_none_count
                                news = getNews(jingzhun_id, kw)
                                saveCompanyNewsToMongo(news, com['name'])
                            else:
                                pass
                                # print '存在--%s' % res['result']['data'][0]['com_name']

