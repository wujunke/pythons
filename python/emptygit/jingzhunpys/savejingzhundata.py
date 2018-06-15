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

headers = {
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',

}
base_url = 'http://192.168.1.251:8080/'
token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'

iplist = [
          # '119.28.194.66:8888',
          # '113.200.214.164:9999',
          # '123.161.16.48:9797',
          # '27.44.161.252:9999',
          # '14.117.208.19:9797',
          # '114.239.201.237:61234',
          # '121.234.245.182:61234',
          # '183.56.177.130:808',
          '115.229.112.82:9000',
          # '183.158.162.189:1246'
          ]

projlist = []
with open("/Users/investarget/pythons/python/emptygit/jingzhun/jingzhun2","r") as f:
    lines = f.readlines()
    for line in lines:
        projlist.append(json.loads(line.replace('\n','')))

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
    'X-Tingyun-Id':'Dio1ZtdC5G4;r=50173626',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'rong.36kr.com',
    'Referer': 'https://rong.36kr.com/list/detail&?sortField=HOT_SCORE',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'kr_plus_utype=4; MEIQIA_EXTRA_TRACK_ID=152CCejE5FvZOExdNT5VaiQnC2S; Z-XSRF-TOKEN=eyJpdiI6Ik8yaUlvYitpMUo5d05oaEVcLzZzSk9RPT0iLCJ2YWx1ZSI6ImZWdXNcL0k4b2J4bURHMFwvYXRiT00rM2piYzBvSVpocWRLQW9EQ0dSUkZpTVpoZlpUMzM0dE13RFcxaUVPaURWVUlONjJ5NjRoQVFPU2RTZEZoNkdXd1E9PSIsIm1hYyI6IjVmYzA2Njk5NWQ4NzczOTgyZWU3YjA4ODc5ZGQ0MWNkZmI4NGNkMmJjOWVhMTRjZDdjMmMwMjE2NTEyNmM0MDQifQ%3D%3D; krchoasss=eyJpdiI6IjdBRzhaRTZDXC9ybFlmUGpBQUI4b0JnPT0iLCJ2YWx1ZSI6IndWTG5Ka2ttYVYrVWc4VFJwZUREN0l4NlBwTG9yeVNVMUZSY2VVVHFVUURLSHJYSW9JamJYa1BQSGdYSDdZbDByK0F3d2ZvQlFWVE5lR29Ca2tGQlZnPT0iLCJtYWMiOiJmY2NmY2M2ZDVmOTcxNDBiOWUwODhkNGIxYWMxMTJmMjY5Y2UyNDgwZTQwMjM1ZTNiNjFkYTgxN2RiODFmYjNlIn0%3D; acw_tc=AQAAALwWlDy19gkAX3iptAh3cJ/alBmi; Hm_lvt_713123c60a0e86982326bae1a51083e1=1527132817,1527488045; device-uid=521c7050-623e-11e8-8f0c-2924338a5d11; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22163a561dce51f1-0393c36168cee8-3f616c4d-2073600-163a561dce72d0%22%2C%22%24device_id%22%3A%22163a561dce51f1-0393c36168cee8-3f616c4d-2073600-163a561dce72d0%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; kr_plus_id=1326029038; kr_plus_token=LIlxDt2eao_UXwzMdTu82hFkMJuMi673525_1___; krid_user_id=1326029038; krid_user_version=6; Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3=1527132687; _kr_p_se=390fca41-fd0c-4e85-ac33-af8289407412; download_animation=1; kr_stat_uuid=5NMfw25453793'
}



def getFinance(jingzhun_id, kw):
    finances = []
    url = url_base + str(jingzhun_id) + '/finance'
    jingzhun_headers['Referer'] = referer + kw
    res = requests.get(url, headers=jingzhun_headers).content
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
                    'currency': finance.get('financeAmountUnit'),    #货币类型
                    'date': str(datetime.datetime.fromtimestamp(finance['financeDate']/1000))[:10]  if finance.get('financeDate') else None,
                    'money': finance.get('financeAmount'),
                    'investormerge': 1,
                    'round': phrase_round.get(finance.get('phase','')),
                }
                finances.append(data)
    return finances


def getCombase(jingzhun_id, kw):
    combase = None
    url = url_base + str(jingzhun_id)
    jingzhun_headers['Referer'] = referer + kw
    res = requests.get(url, headers=jingzhun_headers).content
    res = json.loads(res)
    if res['code'] == 0:
        combase = res['data']
    return combase

def getMembers(jingzhun_id, kw):
    members = None
    url = url_base + str(jingzhun_id) + '/member'
    jingzhun_headers['Referer'] = referer + kw
    res = requests.get(url, headers=jingzhun_headers).content
    res = json.loads(res)
    if res['code'] == 0:
        if len(res['data']['members']) > 0:
            members = res['data']['members']
    return members

def getNews(jingzhun_id, kw):
    news = []
    url = url_base + str(jingzhun_id) + '/news'
    jingzhun_headers['Referer'] = referer + kw
    res = requests.get(url, headers=jingzhun_headers).content
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
                                headers={'Content-Type': 'application/json', 'token': token}).content
            res = json.loads(res)
            if res['code'] == 1000:
                print '新增comnews--' + str(res['result'].get('com_id', None))
                pass
            elif res['code'] == 8001:
                pass
            else:
                print res
                break


def saveInvestInfoToMongo(event_list):
    for event_data in event_list:
        res = requests.post(base_url + 'mongolog/event', data=json.dumps(event_data),
                            headers={'Content-Type': 'application/json', 'token': token}).content
        res = json.loads(res)
        if res['code'] == 1000:
            print '新增invse--' + str(res['result'].get('invse_id', None))
        elif res['code'] == 8001:
            print '重复invest'
        else:
            print res

def saveCompanyToMongo(com_data):
    res = requests.post(base_url + 'mongolog/proj', data=json.dumps(com_data),
                                    headers={'Content-Type': 'application/json', 'token': token}).content
    res = json.loads(res)
    if res['code'] == 1000:
        print '新增com--' + str(res['result'].get('com_id', None))
    elif res['code'] == 8001:
        print '重复company'
    else:
        print res

for proj in projlist:
    kw = urllib.quote(proj['name'].decode(sys.stdin.encoding).encode('utf8'))
    jingzhun_id = proj['id']
    tags = proj.get('tags',[])
    if "36氪报道" in tags:
        tags.remove("36氪报道")
    if "媒体报道" in tags:
        tags.remove("媒体报道")
    data = {
        'com_id': int(jingzhun_id) + saltfactor,
        'com_name': proj['name'],
        'com_status': '运营中',
        'com_scale':'',   #公司规模
        'com_web': '',     #公司网站
        # 'invse_round_id': phrase_round.get(proj.get('phase'),' '),    #公司获投状态
        'com_cat_name': proj.get('industryStr'),     #行业
        'com_sub_cat_name': '',    #子行业
        'com_born_date': str(datetime.datetime.fromtimestamp(proj['startDate']/1000))[:10] if proj.get('startDate') else None,   #成立日期
        'invse_detail_money': '',     #最新融资金额
        'guzhi': '',                 #估值
        'invse_date': '',        #最新融资日期
        'com_logo_archive': '',   #公司logo
        'com_fund_needs_name': '',     #融资需求
        'com_des': '',         #公司介绍
        'invse_total_money': '',    #融资总额
        'com_addr': proj.get('cityStr').replace('省', '').replace('市', '').replace('自治区', '') if proj.get('cityStr') else None,     #公司所在地
        'mobile': '',     # 公司联系方式
        'email': '',       # 公司邮箱
        'detailaddress': '',  # 公司地址
        'tags': tags,       #公司标签
        'source':2,  #用2来表示鲸准 ，空或者1表示it桔子
    }

    search_url = 'https://api.investarget.com/mongolog/proj?com_name=' + kw
    res = requests.get(search_url).content
    res = json.loads(res)
    if res['code'] == 1000:
        if len(res['result']['data']) == 0:
            print '不存在--%s' % proj['name']
            time.sleep(30)
            combase = getCombase(jingzhun_id, kw)
            data['com_scale'] = combase.get('scale')
            data['com_des'] = combase.get('intro')
            data['com_logo_archive'] = combase.get('logo')
            data['detailaddress'] = combase.get('address2Desc', None)
            data['com_web'] = combase.get('website')
            saveCompanyToMongo(data)
            # time.sleep(3)
            investlist = getFinance(jingzhun_id, kw)
            saveInvestInfoToMongo(investlist)
            # time.sleep(3)
            news = getNews(jingzhun_id, kw)
            saveCompanyNewsToMongo(news, proj['name'])
        else:
            print '存在--%s' % res['result']['data'][0]['com_name']

