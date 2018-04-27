#coding=utf-8
import json

from bs4 import BeautifulSoup

html = open('itjuzi.html','r').read()

def parseHtml(html):
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    com_name = soup.title.text
    com_web = None
    a_s = soup.find('i', class_='fa fa-link t-small', )
    if a_s:
        com_web = a_s.parent['href']


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

    # 新闻
    res = soup.find_all('ul', class_='list-unstyled news-list')
    news = []
    for ss in res:
            # print ss.name
            lilist = ss.find_all('li')
            for li in lilist:
                dic = {}
                dic['newsdate'] = li.find('span', class_='news-date').text.replace('\n','').replace('\t','')
                a = li.find('a', class_='line1')
                dic['title'] = a.text.replace('\n','').replace('\t','')
                dic['linkurl'] = a['href']
                dic['newstag'] = li.find('span', class_='news-tag').text.replace('\n','').replace('\t','')
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


    # compititor = []
    # compititoridlist = soup.find('div',class_='sub-titlebar detail-compete-info').find_all('a')
    # for compititorid in compititoridlist:
    #     compititordic = {}
    #     compititordic['type'] = compititorid.text
    #     compititoritemlist = []
    #     compititordiv = soup.find('div',id=compititorid['href'].replace('#',''))
    #     compititorul = compititordiv.find('ul', class_='list-main-icnset list-compete-info')
    #     compititorli = compititorul.find_all('li')
    #     for compititoritem in compititorli:
    #         ul = compititoritem.find('ul',class_='list-main-icnset list-compete-info')
    #         image = ''
    #         com = compititoritem.find('p',class_='title').text
    #         com_add = ''
    #         com_date = ''
    #         com_cat = ''
    #         com_round = ''
    #         com_fund = ''



    # list-chart  投资机构排行榜
    # echart  投融资趋势

    # list_chart = soup.find('div', id='list-chart')
    # list_chart_title =  list_chart['chart-title']
    # list_chart_sub_title =  list_chart['chart-sub-title']
    # lilist = list_chart.find_all('li')
    # comlist = []
    # for li in lilist:
    #     com = li.a.text
    #     count = li.span.text
    #     com_id = li.a['href'].split('/')[-1]
    #     comlist.append({'com_name':com,'invest_count':count,'com_id':com_id})
    # response['list_chart'] = {
    #     'title': list_chart_title,
    #     'sub_title': list_chart_sub_title,
    #     'data': comlist
    # }
    #
    # echart = soup.find('div', id='echart')
    # echart_title =  echart['chart-title']
    # echart_sub_title =  echart['chart-sub-title']
    # echart_data = None
    # if len(echart['data-json']) > 2:
    #     echart_data = json.loads(echart['data-json'])
    #
    # response['echart'] = {
    #     'title': echart_title,
    #     'sub_title': echart_sub_title,
    #     'data': echart_data
    # }

    # 工商信息
    # recruit-info
    recruit_info = soup.find('div',id='recruit-info')
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
                    for i in range(0, len(theadlist) - 1):
                        infodic[theadlist[i]] = tdlist[i].text if tdlist[i].text else None
                    infolist.append(infodic)
            response[tabhref] = infolist
    return response, com_name

res = parseHtml(html)
print res


