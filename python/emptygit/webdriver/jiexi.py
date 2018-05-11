#coding=utf-8
import json

from bs4 import BeautifulSoup

html = open('itjuzi2.html','r').read()

def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    com_name = soup.title.text
    com_web = None
    a_s = soup.find('i', class_='fa fa-link t-small', )
    if a_s:
        com_web = a_s.parent['href']
    name = soup.find('h1', class_='seo-important-title', )
    if name:
        com_name = name.text.replace(u'\t', u'')
        com_name = com_name.split('\n')[1]

    industryType = soup.find('a', class_='one-level-tag').text if soup.find('a', class_='one-level-tag') else ''

    # 联系方式
    ll = ['mobile', 'email', 'detailaddress']
    response = {}
    contact_ul = soup.find('ul',class_='list-block aboutus')
    if contact_ul:
        for info in contact_ul.find_all('li'):
            if info.find('i',class_='fa icon icon-phone-o'):
                response['mobile'] = info.text.replace('\n','').replace('\t','')
            if info.find('i',class_='fa icon icon-email-o'):
                response['email'] = info.text.replace('\n','').replace('\t','')
            if info.find('i',class_='fa icon icon-address-o'):
                response['detailaddress'] = info.text.replace('\n','').replace('\t','')
    # 团队信息
    members = []
    membersul = soup.find('ul', class_='list-unstyled team-list limited-itemnum')
    if membersul:
        lilist = membersul.find_all('li')
        for li in lilist:
            dic = {}
            dic['姓名'] = li.find('a', class_='person-name').text.replace('\n','').replace('\t','') if li.find('a', class_='person-name') else None
            dic['职位'] = li.find('div', class_='per-position').text.replace('\n','').replace('\t','') if li.find('div', class_='per-position') else None
            dic['简介'] = li.find('div', class_='per-des').text.replace('\n','').replace('\t','') if li.find('div', class_='per-des') else None
            members.append(dic)
    response['indus_member'] = members

    # 新闻
    res = soup.find_all('ul', class_='list-unstyled news-list')
    news = []
    for ss in res:
            # print ss.name
            lilist = ss.find_all('li')
            for li in lilist:
                dic = {}
                dic['newsdate'] = li.find('span', class_='news-date').text.replace('\n','').replace('\t','') if li.find('span', class_='news-date') else None
                a = li.find('a', class_='line1')
                dic['title'] = a.text.replace('\n','').replace('\t','')
                dic['linkurl'] = a['href']
                dic['newstag'] = li.find('span', class_='news-tag').text.replace('\n','').replace('\t','') if li.find('span', class_='news-tag') else None
                news.append(dic)
    response['news'] = news
    response['com_web'] = com_web

    # 工商信息
    # recruit-info
    recruit_info = soup.find('div',id='recruit-info')
    if recruit_info:
        tablistul = recruit_info.find('ul',class_='nav-tabs list-inline stock_titlebar')
        tablistli = tablistul.find_all('li')
        for tabli in tablistli:
            tabhref = tabli.a['href'].replace('#','')
            if tabhref in ['indus_base',u'indus_base']:   # 基本信息
                indus_base = recruit_info.find('div', id=tabhref)
                com_name = indus_base.find('th').text
                infolisttd = indus_base.find_all('td')
                infodic = {}
                for info in infolisttd:
                    if info:
                        if info.find('span', class_='tab_title') and info.find('span', class_='tab_main'):
                            if info.find('span', class_='tab_title').text:
                                infodic[info.find('span', class_='tab_title').text] = info.find('span', class_='tab_main').text.replace('\n','').replace('\t','')
                infodic[u'公司名称:'] = com_name.replace('\n','').replace('\t','')
                response[tabhref] = infodic

            if tabhref in ['indus_shareholder', u'indus_shareholder','indus_foreign_invest', u'indus_foreign_invest', 'indus_busi_info', u'indus_busi_info']:   #  股东信息、企业对外投资信息、工商变更信息
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
                        for i in range(0, len(theadlist)):
                            infodic[theadlist[i]] = tdlist[i].text.replace('\n','').replace('\t','') if tdlist[i].text else None
                        infolist.append(infodic)
                response[tabhref] = infolist


    # 投资信息


    # 融资信息
    investents = soup.find(id='invest-portfolio')
    eventtable = investents.find('table')
    eventtrlist = eventtable.find_all('tr')
    eventlist = []
    for eventtr in eventtrlist:
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
            data['merger_with'] = eventtr.find('a', class_='line1 c-gray').text if eventtr.find('a', class_='line1 c-gray') else ''
        else:
            data['investormerge'] = 1
            data['invse_id'] = event_id
            line1s = eventtr.find_all('a', class_='line1')
            invsest_with = []
            for line1 in line1s:
                url = line1['href']
                invst_name = line1.text
                invsest_with.append({'url':url, 'invst_name':invst_name})
            data['invsest_with'] = invsest_with
        eventlist.append(data)
    response['events'] = eventlist

    response['industryType'] = industryType

    return response, com_name

res = parseHtml(html)
# print res


