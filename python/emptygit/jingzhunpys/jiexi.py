#coding=utf-8
from bs4 import BeautifulSoup


# html = open('gongshang.html','r').read()

def parseGongShangHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    source = soup.find('div', class_='main')
    base_info_element = source.find('div', class_='base-info')
    partner_info_element = source.find('div', class_='partner-info')
    employ_info_element = source.find('div', class_='employ-info')
    record_info_element = source.find('div', class_='record-info')
    base_info = []
    base_info_divs = base_info_element.find_all('div', class_='group')
    for base_info_div in base_info_divs:
        describe = base_info_div.find('div', class_='describe').text
        content = base_info_div.find('span', class_='ng-binding').text
        base_info.append({describe: content})

    partner_info = []
    partner_info_divs = partner_info_element.find_all('div', class_='group ng-scope')
    for partner_info_div in partner_info_divs:
        describe = partner_info_div.find('div', class_='describe').text
        content = partner_info_div.find('span', class_='ng-binding').text
        partner_info.append({describe: content})

    employ_info = []
    employ_info_divs = employ_info_element.find_all('div', class_='group ng-scope')
    for employ_info_div in employ_info_divs:
        describe = employ_info_div.find('div', class_='describe').text
        content = employ_info_div.find('span', class_='ng-binding').text
        employ_info.append({describe: content})

    record_info = []
    record_info_table = record_info_element.find('table')
    if record_info_table['class'] =='ng-hide':
        pass
    else:
        table_header = []
        table_header_tr = record_info_table.find('tr')
        table_header_tds = table_header_tr.find_all('td')
        for td in table_header_tds:
            table_header.append(td.text)
        table_trs = record_info_table.find_all('tr', class_='ng-scope')
        for table_tr in table_trs:
            tds = table_tr.find_all('td')
            record_one = {}
            record_one[table_header[0]] = tds[0].text + tds[2].text
            # record_one[table_header[1]] = tds[2].text
            record_one[table_header[2]] = tds[4].text
            record_one[table_header[3]] = tds[6].text

            record_info.append(record_one)

    res = {
        'base': base_info,
        'partner': partner_info,
        'employ': employ_info,
        'record': record_info,
    }
    return res



# res = parseGongShangHtml(html)


searchHtml = open('search_result.html','r').read()

def parseSearchResultHtml(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')
    tbody = table.find('tbody')
    return table



res = parseSearchResultHtml(searchHtml)