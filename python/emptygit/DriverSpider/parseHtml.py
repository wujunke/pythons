#coding=utf-8
import json
import requests
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException


def parseComListHtml(html):
    soup = BeautifulSoup(html, 'html.parser')

    comlistbox = soup.find('div', class_='company-list-box')

    leftbox = comlistbox.find('div', class_='company-list-left')

    comlist = {}

    leftlis = leftbox.find_all('li',)
    for li in leftlis:
        if li.get('data-id'):
            comleftdata = {
                'com_id': li.get('data-id', ''),
                'com_logo_archive': li.find('img').get('src', ''),
                'com_name': li.find_all('a')[1].text,
                'com_des': li.find('p', class_='des').text,
            }
            comlist[li.get('data-id')] = comleftdata

    infobox = comlistbox.find('div', class_='company-list-info')
    infolis = infobox.find_all('li', )
    for li in infolis:
        if li.get('data-id'):
            infodivs = li.find_all('div')
            latestround = infodivs[2].find_all('span')
            cominfodata = {
                'com_cat_name': infodivs[0].text,
                'com_sub_cat_name': infodivs[1].text,
                'invse_total_money': infodivs[3].text,
                'guzhi': infodivs[4].text,
                'com_addr': infodivs[5].text,
                'com_born_date': infodivs[6].text,
                'com_status': infodivs[7].text,
                'com_scale': infodivs[8].text,
                'invse_date': latestround[0].text,
                'invse_round_id': latestround[1].text,
                'invse_detail_money': latestround[2].text,
            }
            comlist[li.get('data-id')].update(cominfodata)

    page = soup.find('div', id_='page-selection').find('li', class_='active').text

    return comlist, page



def parseComDetailHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.title:
        response = {}
        com_name = soup.title.text
        if com_name in (u'www.itjuzi.com', u'找不到您访问的页面', u'502 Bad Gateway', u'403', u'IT桔子 | 泛互联网创业投资项目信息数据库及商业信息服务商'):
            return None, com_name, None
        com_name = com_name.replace(u' - IT桔子', u'').split(',')[0]
        com_web = None
        a_s = soup.find('svg', class_='svg-icon link mr-2', )
        if a_s:
            com_web = a_s.parent.get('href')
        response['com_web'] = com_web
        full_name = soup.find('p', class_='seo-second-title margin-right50', )
        if full_name:
            full_name = full_name.text
        # 联系方式
        contact_ul = soup.find('ul', class_='list-block aboutus')
        if contact_ul:
            for info in contact_ul.find_all('li'):
                if info.find('svg', class_='svg-icon phone align-middle'):
                    response['mobile'] = info.text.replace('\n', '').replace('\t', '')
                if info.find('svg', class_='svg-icon email align-middle'):
                    response['email'] = info.text.replace('\n', '').replace('\t', '')
                if info.find('svg', class_='svg-icon home'):
                    response['detailaddress'] = info.text.replace('\n', '').replace('\t', '')

        com_sub_catele = soup.find('a', class_='tag d-inline-block mr-2 mb-2 sub_scope-tag tag-item')
        com_sub_cat = com_sub_catele.text if com_sub_catele else None
        newslist = []
        newsEle = soup.find(id='news')
        if newsEle:
            newsEle = newsEle.find_all('div', class_='list-group-item d-flex align-items-center feedback-btn-parent justify-content-around border-0 juzi-list-item pt-4 pb-4')
            for new in newsEle:
                newdata = {}
                newdata['newsdate'] = new.find('span', class_='news-date d-inline-block').text
                newdata['linkurl'] = new.find('a').get('href')
                newdata['title'] = new.find('a').text
                newslist.append(newdata)

        response['news'] = newslist
        response['com_sub_cat_name'] = com_sub_cat

        '''
        # com_name = soup.title.text
        # if com_name in (u'www.itjuzi.com', u'找不到您访问的页面', u'502 Bad Gateway', u'403'):
        #     return None, com_name
        # com_web = None
        # a_s = soup.find('i', class_='fa fa-link t-small', )
        # if a_s:
        #     com_web = a_s.parent['href']
        # name = soup.find('h1', class_='seo-important-title', )
        # full_name = None
        # if name:
        #     com_name = name.text.replace(u'\t', u'')
        #     com_name = com_name.split('\n')[1]
        #     full_name = name['data-fullname']
        # # 联系方式
        # ll = ['mobile', 'email', 'detailaddress']
        # response = {}
        # contact_ul = soup.find('ul', class_='list-block aboutus')
        # if contact_ul:
        #     for info in contact_ul.find_all('li'):
        #         if info.find('i', class_='fa icon icon-phone-o'):
        #             response['mobile'] = info.text.replace('\n', '').replace('\t', '')
        #         if info.find('i', class_='fa icon icon-email-o'):
        #             response['email'] = info.text.replace('\n', '').replace('\t', '')
        #         if info.find('i', class_='fa icon icon-address-o'):
        #             response['detailaddress'] = info.text.replace('\n', '').replace('\t', '')


        # # 融资信息
        # investents = soup.find(id='financing')
        # eventtable = investents.find('table')
        # eventtrlist = eventtable.find_all('tr')
        # eventlist = []
        # for eventtr in eventtrlist:
        #     if eventtr.find(class_='date'):
        #         date = eventtr.find(class_='date').text
        #         round = eventtr.find(class_='round').text
        #         money = eventtr.find(class_='finades').text
        #
        #         link = eventtr.find(class_='finades').a['href']
        #         type = link.split('/')[-2]
        #         event_id = link.split('/')[-1]
        #         data = {
        #             'date': date,
        #             'round': round,
        #             'money': money,
        #         }
        #         if type == 'merger':
        #             data['investormerge'] = 2
        #             data['merger_id'] = event_id
        #             data['merger_with'] = eventtr.find('a', class_='line1 c-gray').text if eventtr.find('a',
        #                                                                                                 class_='line1 c-gray') else ''
        #         else:
        #             data['investormerge'] = 1
        #             data['invse_id'] = event_id
        #             line1s = eventtr.find_all('a', class_='line1')
        #             invsest_with = []
        #             for line1 in line1s:
        #                 url = line1.get('href', None)
        #                 invst_name = line1.text
        #                 invsest_with.append({'url': url, 'invst_name': invst_name})
        #             data['invsest_with'] = invsest_with
        #         eventlist.append(data)
        # response['events'] = eventlist
        #
        # industryType = soup.find('a', class_='one-level-tag').text if soup.find('a', class_='one-level-tag') else ''
        # response['industryType'] = industryType
        #
        # # 团队信息
        # members = []
        # membersul = soup.find('ul', class_='list-unstyled team-list limited-itemnum')
        # if membersul:
        #     lilist = membersul.find_all('li')
        #     for li in lilist:
        #         dic = {}
        #         dic['姓名'] = li.find('a', class_='person-name').text.replace('\n', '').replace('\t', '') if li.find('a',
        #                                                                                                            class_='person-name') else None
        #         dic['职位'] = li.find('div', class_='per-position').text.replace('\n', '').replace('\t', '') if li.find(
        #             'div', class_='per-position') else None
        #         dic['简介'] = li.find('div', class_='per-des').text.replace('\n', '').replace('\t', '') if li.find('div',
        #                                                                                                          class_='per-des') else None
        #         members.append(dic)
        # response['indus_member'] = members
        #
        # # 新闻
        # res = soup.find_all('ul', class_='list-unstyled news-list')
        # news = []
        # for ss in res:
        #     # print ss.name
        #     lilist = ss.find_all('li')
        #     for li in lilist:
        #         dic = {}
        #         dic['newsdate'] = li.find('span', class_='news-date').text.replace('\n', '').replace('\t',
        #                                                                                              '') if li.find(
        #             'span', class_='news-date') else None
        #         a = li.find('a', class_='line1')
        #         dic['title'] = a.text.replace('\n', '').replace('\t', '')
        #         dic['linkurl'] = a['href']
        #         dic['newstag'] = li.find('span', class_='news-tag').text.replace('\n', '').replace('\t', '') if li.find(
        #             'span', class_='news-tag') else None
        #         news.append(dic)
        # response['news'] = news
        # response['com_web'] = com_web
        #
        # # 工商信息
        # # recruit-info
        # recruit_info = soup.find('div', id='recruit-info')
        # if recruit_info:
        #     tablistul = recruit_info.find('ul', class_='nav-tabs list-inline stock_titlebar')
        #     tablistli = tablistul.find_all('li')
        #     for tabli in tablistli:
        #         tabhref = tabli.a['href'].replace('#', '')
        #         if tabhref in ['indus_base', u'indus_base']:  # 基本信息
        #             indus_base = recruit_info.find('div', id=tabhref)
        #             com_full_name = indus_base.find('th').text
        #             infolisttd = indus_base.find_all('td')
        #             infodic = {}
        #             for info in infolisttd:
        #                 if info:
        #                     if info.find('span', class_='tab_title') and info.find('span', class_='tab_main'):
        #                         if info.find('span', class_='tab_title').text:
        #                             infodic[info.find('span', class_='tab_title').text] = info.find('span',
        #                                                                                             class_='tab_main').text.replace(
        #                                 '\n', '').replace('\t', '')
        #             infodic[u'公司名称:'] = com_full_name.replace('\n', '').replace('\t', '')
        #             response[tabhref] = infodic
        #
        #         if tabhref in ['indus_shareholder', u'indus_shareholder', 'indus_foreign_invest',
        #                        u'indus_foreign_invest', 'indus_busi_info', u'indus_busi_info']:  # 股东信息、企业对外投资信息、工商变更信息
        #             indus_shareholder = recruit_info.find('div', id=tabhref)
        #             thead = indus_shareholder.find('thead')
        #             if thead:
        #                 theadthlist = thead.find_all('th')
        #                 theadlist = []
        #                 for theaditem in theadthlist:
        #                     theadlist.append(theaditem.text)
        #                 tbody = indus_shareholder.find('tbody')
        #                 infolist = []
        #                 if tbody:
        #                     trlist = tbody.find_all('tr')
        #                     for tr in trlist:
        #                         infodic = {}
        #                         tdlist = tr.find_all('td')
        #                         for i in range(0, len(theadlist)):
        #                             try:
        #                                 infodic[theadlist[i]] = tdlist[i].text.replace('\n', '').replace('\t', '') if \
        #                                 tdlist[i].text else None
        #                             except IndexError:
        #                                 print('数组越界', len(theadlist), len(tdlist))
        #                         if infodic != {}:
        #                             infolist.append(infodic)
        #                 response[tabhref] = infolist
        '''
        return response, com_name, full_name
    else:
        return None, None, None

# html = open('itjuzi_gai.html', 'r').read()
# ss = parseComDetailHtml(html)

# driver = webdriver.Chrome('/usr/local/bin/chromedriver')

def parseComFinanceByDriver(driver):

    financeData = []
    try:
        driver.find_element_by_xpath('//*[@id="financing"]/table/tbody')
    except NoSuchElementException:
        return []
    path_id = 0
    while True:
        path_id += 1
        eventdata = {}
        try:
            tr_xpath = '//*[@id="financing"]/table/tbody/tr[%s]' % path_id
            driver.find_element_by_xpath(tr_xpath)
            eventdata['date'] = driver.find_element_by_xpath(tr_xpath + '/td[1]').text
            eventdata['round'] = driver.find_element_by_xpath(tr_xpath + '/td[2]').text
            eventdata['money'] = driver.find_element_by_xpath(tr_xpath + '/td[3]').text

            eventurlele = driver.find_element_by_xpath(tr_xpath + '/td[5]/a')
            eventurl = eventurlele.get_attribute('href')
            if eventurl.split('/')[-2] == 'investevent':
                investormerge = 1
                eventdata['invse_id'] = eventurl.split('/')[-1]
            else:
                investormerge = 2
                eventdata['merger_id'] = eventurl.split('/')[-1]
            eventdata['investormerge'] = investormerge

            if investormerge == 1:
                invsest_with = []
                try:
                    investor = driver.find_element_by_xpath(tr_xpath + '/td[4]/a')
                    invsest_with.append({'url': investor.get_attribute("href"), 'invst_name': investor.text})
                except (NoSuchElementException, Exception):
                    i = 0
                    while i < 10:
                        i += 1
                        try:
                            investor = driver.find_element_by_xpath(tr_xpath + '/td[4]' + '/a[%s]' % i)
                            invsest_with.append({'url': investor.get_attribute("href"), 'invst_name': investor.text})
                        except (NoSuchElementException, Exception):
                            break
                eventdata['invsest_with'] = invsest_with
            else:
                investor = driver.find_element_by_xpath(tr_xpath + '/td[4]/a')
                eventdata['merger_with'] = investor.text

            financeData.append(eventdata)
        except (NoSuchElementException, Exception):
            break

    return financeData







def parseComMemberByDriver(driver):
    try:
        driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[3]/div[1]/div/div[4]/div[1]/div[3]/div[1]/ul')
    except NoSuchElementException:
        return []
    memberlist = []
    path_id = 0
    while True:
        path_id += 1
        memberdata = {}
        try:
            li_xpath = '//*[@id="app"]/div[1]/div/div[3]/div[1]/div/div[4]/div[1]/div[3]/div[1]/ul/li[%s]' % path_id
            driver.find_element_by_xpath(li_xpath)
            memberdata['姓名'] = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[3]/div[1]/div/div[4]/div[1]/div[3]/div[1]/ul/li[1]/a[2]').text
            memberdata['职位'] = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[3]/div[1]/div/div[4]/div[1]/div[3]/div[1]/ul/li[1]/div[1]').text
            memberdata['简介'] = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[3]/div[1]/div/div[4]/div[1]/div[3]/div[1]/ul/li[1]/div[2]').text
            memberlist.append(memberdata)
        except (NoSuchElementException, Exception):
            break
    return memberlist

def getComBasic(driver, com_id):
    driver.get('https://www.itjuzi.com/api/companies/%s?type=basic' % com_id)
    basicpage = driver.page_source.replace(
        '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">',
        '').replace('</pre></body></html>', '')
    basic = json.loads(basicpage)
    basicDic = {}
    if basic.get('data'):
        basicDic.update(basic['data']['basic'])
        basicDic['com_addr'] = basic['data']['basic']['com_prov']
        basicDic['com_sub_cat_name'] = basic['data']['basic']['com_sub_scope'][0]['name']
        basicDic['com_full_name'] = basic['data']['basic']['com_registered_name']
        basicDic['com_web'] = basic['data']['basic']['com_url']
        basicDic['invse_total_money'] = str(basic['data']['basic']['total_money']) + '万'
    return basicDic

def getComIndustryInfo(driver, com_id):
    driver.get('https://www.itjuzi.com/api/companies/%s?type=icp' % com_id)
    industryinfo = driver.page_source.replace(
        '<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">',
        '').replace('</pre></body></html>', '')
    info = json.loads(industryinfo)

    indus_base = {}
    indus_baseData = info['data']['elecredit'].get('elecredit_basic')
    if indus_baseData:
        indus_base.update({ u'地址:': indus_baseData['dom'],
                            u'公司类型:': indus_baseData['enttype'],
                            u'公司名称:': indus_baseData['entname'],
                            u'注册资本:': indus_baseData['regcap'] + '万人民币',
                            u'法人代表:': indus_baseData['frname'],
                            u'成立时间:': indus_baseData['esdate'], })
    indus_shareholderDara = info['data']['elecredit'].get('elecredit_shareholder')
    indus_shareholder = []
    if indus_shareholderDara:
        for userdata in indus_shareholderDara:
            indus_shareholder.append({u'出资比例': userdata['fundedratio'],
                                      u'出资日期': userdata['condate'],
                                      u'股东': userdata['shaname'],
                                      u'出资方式': userdata['conform'],
                                      u'认缴出资额': userdata['subconam'] + '万' + userdata['regcapcur'],})
    indus_busi_info = []
    indus_busi_infoData = info['data']['elecredit'].get('elecredit_alter')
    if indus_busi_infoData:
        for busiData in indus_busi_infoData:
            indus_busi_info.append({
                u'变更日期': busiData['altdate'] + busiData['altitem'],
                u'变更前': busiData['altbe'],
                u'变更后': busiData['altaf'],
            })
    indus_foreign_invest = []
    indus_foreign_investData = info['data']['elecredit'].get('elecredit_entinv')
    if indus_foreign_investData:
        for foreignData in indus_foreign_investData:
            indus_foreign_invest.append({
                u'出资比例': foreignData['fundedratio'],
                u'出资日期': foreignData['esdate'],
                u'出资方式': foreignData['conform'],
                u'认缴出资额': foreignData['subconam'] + '万' + foreignData['regcapcur'],
                u'公司名称': foreignData['entname'],
            })


    return {'com_id': com_id, 'indus_base': indus_base, 'indus_shareholder': indus_shareholder, 'indus_busi_info': indus_busi_info, 'indus_foreign_invest': indus_foreign_invest}


def parseComIndustryInfoByDriver(driver, com_id, proxy):
    cookies = driver.get_cookies()
    coostrlist = []
    for coo in cookies:
        coostrlist.append('%s=%s' % (coo['name'], coo['value']))
    cookie = ';'.join(coostrlist)
    acc_token = driver.execute_script("return localStorage.getItem('accessToken')")
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Authorization': acc_token,
        'Connection': '',
        'Cookie': cookie,
        'Host': 'www.itjuzi.com',
        'Referer': 'https://www.itjuzi.com/company/%s' % com_id,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    }
    if proxy and len(proxy) > 0:
        proxies = {
            "https": "http://%s" % proxy,
        }
    else:
        proxies = None
    def getRequestRes():
        try:
            res = requests.get('https://www.itjuzi.com/api/companies/%s?type=icp' % com_id, headers=headers,
                               proxies=proxies, timeout=20).content
            infores = json.loads(res)['data']['elecredit']
            return infores
        except Exception:
            print('获取icp失败--com_id:%s'%com_id)
            time.sleep(3)
            return getRequestRes()

    info = getRequestRes()

    indus_base = {}
    indus_baseData = info.get('elecredit_basic')
    if indus_baseData:
        indus_base.update({ u'地址:': indus_baseData['dom'],
                            u'公司类型:': indus_baseData['enttype'],
                            u'公司名称:': indus_baseData['entname'],
                            u'注册资本:': str(indus_baseData['regcap']) + '万人民币' if indus_baseData['regcap'] else '',
                            u'法人代表:': indus_baseData['frname'],
                            u'成立时间:': indus_baseData['esdate'], })
    indus_shareholderDara = info.get('elecredit_shareholder')
    indus_shareholder = []
    if indus_shareholderDara:
        for userdata in indus_shareholderDara:
            indus_shareholder.append({u'出资比例': (str(userdata['fundedratio']) + '%') if userdata['fundedratio'] and userdata['fundedratio'] != 0 else None,
                                      u'出资日期': userdata['condate'],
                                      u'股东': userdata['shaname'],
                                      u'出资方式': userdata['conform'],
                                      u'认缴出资额': (str(userdata['subconam']) + '万' if userdata['subconam'] else '' ) + (userdata['regcapcur'] if userdata['regcapcur'] else ''),})
    indus_busi_info = []
    indus_busi_infoData = info.get('elecredit_alter')
    if indus_busi_infoData:
        for busiData in indus_busi_infoData:
            indus_busi_info.append({
                u'变更日期': busiData['altdate'] + busiData['altitem'],
                u'变更前': busiData['altbe'],
                u'变更后': busiData['altaf'],
            })
    indus_foreign_invest = []
    indus_foreign_investData = info.get('elecredit_entinv')
    if indus_foreign_investData:
        for foreignData in indus_foreign_investData:
            indus_foreign_invest.append({
                u'出资比例': (str(foreignData['fundedratio']) + '%') if foreignData['fundedratio'] and foreignData['fundedratio'] != 0 else None,
                u'出资日期': foreignData['esdate'],
                u'出资方式': foreignData['conform'],
                u'认缴出资额': (str(foreignData['subconam']) + '万') if foreignData['subconam'] else '' + foreignData['regcapcur'] if foreignData['regcapcur'] else '',
                u'公司名称': foreignData['entname'],
            })


    return {'com_id': com_id, 'indus_base': indus_base, 'indus_shareholder': indus_shareholder, 'indus_busi_info': indus_busi_info, 'indus_foreign_invest': indus_foreign_invest}

