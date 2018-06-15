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


headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'www.itjuzi.com',
            'Referer':'https://www.itjuzi.com/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie':'Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1528867742; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1528171396,1528447998,1528448117,1528859974; _ga=GA1.2.731013236.1525919505; _gid=GA1.2.1446903901.1528859974; gr_session_id_eee5a46c52000d401f969f4535bdaa78=bb18ff64-3a63-4185-857f-2609dbb5b410_true; session=aae6a2abaae7540c327bbdafc2bc27fb0a8ee6fb; _gat=1; identity=18616837957%40test.com; paidtype=vip; remember_code=5ep8EkW3iv; unique_token=439977; MEIQIA_EXTRA_TRACK_ID=14OXH2v2gWQV2XMgAOGoHy4ttSx; acw_tc=AQAAANRgqTkn4QwAXniptFMN8D7Ssis9; gr_user_id=6fbe0ddf-3ae7-42c2-a691-9d922ba5ab99'
}
iplist1 = ['140.205.222.3:80']
def rand_proxie_http():
    return {'http':'http://%s' % iplist1[random.randint(0, len(iplist1)) - 1],}
url_company_detail_https = 'https://www.itjuzi.com/company/'

res = requests.get(url_company_detail_https + '28554595', headers=headers , proxies=rand_proxie_http()).content

# print res


def parse(html):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    com_name = soup.find('h1', class_='seo-important-title').text.replace('\n', '').replace('\t', '')
    com_web = None
    a_s = soup.find('i', class_='fa fa-link t-small', )
    if a_s:
        com_web = a_s.parent['href']

    # 联系方式
    response = {}
    # response['com_id'] = int(com_id)
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

    # 融资信息
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
    return response

print res
info = parse(res)
print info