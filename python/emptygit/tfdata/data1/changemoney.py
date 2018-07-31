#coding=utf-8
import json
import re

import requests
import xlrd
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)





def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print str(e)

def excel_table_byindex(file,colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows
    colnames =  table.row_values(colnameindex)
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list

def changeTagIndex(tagstr, indexlist, to='1'):
    l = list(tagstr)
    for index in indexlist:
        l[index] = to
    newS = ''.join(l)
    return newS

tagcontrastlist = excel_table_byindex('tagc.xlsx')

base_url = 'https://api.investarget.com/'
# base_url = 'http://192.168.1.201:8000/'

headers = {
    'Content-Type': 'application/json',
    'token': 'a7305831f4903690feb349c16ab37f9b4962197305ba32c7'
}


def getCom_cat_indexlist(com_cat, com_sub_cat):
    indexlist = []
    for tag in tagcontrastlist:
        if tag[u'cat_name'] == com_sub_cat:
            indexlist.append(int(tag[u'index']))
    if len(indexlist) == 0:
        for tag in tagcontrastlist:
            if tag[u'cat_name'] == com_cat:
                indexlist.append(int(tag[u'index']))
    return indexlist

def getCom_Full_name(com_id):
    fullname = None
    url = base_url + 'mongolog/projinfo?com_id=%s' % int(com_id)
    res = requests.get(url, headers=headers).content
    res = json.loads(res)
    if res['code'] == 1000:
        result = res['result']
        if result:
            indus_base = result.get('indus_base', {})
            if indus_base:
                fullname = indus_base.get(u'公司名称:')
    return fullname

orgcontrastlist = []
with open('/Users/investarget/pythons/python/emptygit/addInvestEvent/name_id_comparetable') as f:
    for line in f:
        orgcontrastlist.append(json.loads(line))

def getCom_invest_org(com_id):
    eventlist = []
    url = base_url + 'mongolog/event?com_id=%s' % int(com_id)
    res = requests.get(url, headers=headers).content
    res = json.loads(res)
    if res['code'] == 1000:
        eventlist = res['result']['data']
    orglist = []
    recentlist = []
    l = 0
    for event in eventlist:
        l += 1
        if event['investormerge'] == 2:
            data = {
                'id': None,
                'org_name': event['merger_with']
            }
            orglist.append(data)
            if l == 1:
                recentlist.append(event['merger_with'])
        else:
            if event['invsest_with']:
                for invsest in event['invsest_with']:
                    if invsest['url']:
                        if invsest['url'].split('/')[-2] != u'person':
                            data = {
                                'id': invsest['url'].split('/')[-1],
                                'org_name': invsest['invst_name']
                            }
                            orglist.append(data)
                            if l == 1:
                                recentlist.append(invsest['invst_name'])
    return orglist, recentlist

def searchtoporg(org_id=None, org_name=None):
    if org_id:
        url = base_url + 'org/?ids=%s&lv=1' % int(org_id)
    elif org_name:
        url = base_url + 'org/?orgname=%s&lv=1' % org_name
    else:
        return False
    res = requests.get(url, headers=headers).content
    res = json.loads(res)
    if res['code'] == 1000:
        data = res['result']['data']
        if len(data) > 0:
            return True
    return False


def checktop(orglist):
    for orginfo in orglist:
        try:
            if orginfo['id'] and orginfo['id'].isdigit():
                haituo_id = None
                for org in orgcontrastlist:
                    if org['itjuzi_id'] == int(orginfo['id']):
                        haituo_id = org['haituo_id']
                        break
                if searchtoporg(haituo_id, orginfo['org_name']):
                    return 1
            elif orginfo['org_name']:
                haituo_id = None
                for org in orgcontrastlist:
                    if org['itjuzi_name'] == orginfo['org_name']:
                        haituo_id = org['haituo_id']
                        break
                if searchtoporg(haituo_id, orginfo['org_name']):
                    return 1
        except Exception:
            print json.dumps(orginfo)
    return 0




import csv


def savetocsvfile(data):
    with open("test3.csv","a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            int(data['com_id']),
            data['com_name'],
            data['com_scale'],
            data['invse_round_id'],
            data['com_cat_name'],
            data['com_sub_cat_name'],
            data['com_born_date'],
            data['invse_detail_money'],
            data['guzhi'],
            data['invse_date'],
            data['com_fund_needs_name'],
            data['invse_total_money'],
            data['com_addr'],
            data['tag'],
            data['com_full_name'],
            data['top'],
            data['invest_org'],
            int(data['latest']) if int(data['latest']) < int(data['total']) else int(data['total']),
            int(data['total']),
            0

        ])


def saveorgtocsvfile(orgname):
    with open("org2.csv","a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([orgname])

def moneyToCNY(money, currency):
    if money > 0 and currency != 'CNY':
        rate = moneyrate.get(currency)
        if rate:
            money = money * rate
            return money
    return money

find_float = lambda x: re.search("\d+(\.\d+)?", x).group()

moneyrate = {
    'USD': 6.50,
    'HKD': 0.85,
    'JPY': 0.060,
    'EUR': 7.82,
    'GBP': 8.84,
    'KRW': 0.0059,
    'INR': 0.09741
}

roundcontrast = {
    '尚未获投':1,'种子轮':2,'天使轮':3,'Pre-A轮':4,'A轮':5,'A+轮':6,'Pre-B轮':7,'B轮':8,'B+轮':9,'C轮':10,'C+轮':11,'D轮':12,'D+轮':13,
    'E轮':14,'F轮-上市前':15,'已上市':16,'新三板':0,'战略投资':17,'已被收购':17,'不明确':0,'并购':17
}

def handleMoney(moneystr):
    if isinstance(moneystr, unicode):
        moneystr = str(moneystr)
    if moneystr in ['',  '-'] or '未透露' in moneystr or '未披露' in moneystr:
        moneystr = '0.00'
    if '数' in moneystr:
        moneystr = moneystr.replace('数', '5')
    if '及以上' in moneystr:
        moneystr = moneystr.replace('及以上', '1.0')
    if '级' in moneystr:
        moneystr = moneystr.replace('级', '1.0')
    if '$' in moneystr or '美元' in moneystr:
        currency = 'USD'
    elif '￥' in moneystr or '人民币' in moneystr:
        currency = 'CNY'
    elif '€' in moneystr or '欧元' in moneystr:
        currency = 'EUR'
    elif '£' in moneystr or '英镑' in moneystr:
        currency = 'GBP'
    elif '￥' in moneystr or '日元' in moneystr:
        currency = 'JPY'
    elif '₩' in moneystr or '韩元' in moneystr:
        currency = 'KRW'
    elif '₹' in moneystr or '卢比' in moneystr:
        currency = 'INR'
    elif '￥' in moneystr or '港元' in moneystr:
        currency = 'HKD'
    else:
        currency = 'CNY'

    floatstr = find_float(moneystr)
    if len(floatstr) > 0:
        money = float(floatstr)
        if '十' in moneystr:
            money = money * 10
        if '百' in moneystr:
            money = money * 100
        if '千' in moneystr:
            money = money * 1000
        if '万' in moneystr:
            money = money * 10000
        if '亿' in moneystr:
            money = money * 100000000
        return money, currency
    return 0,currency

def getRoundId(roundstr):
    roundid = 0
    if roundstr:
        roundid = roundcontrast.get(str(roundstr), 0)
    return roundid

tables = excel_table_byindex('proj.xlsx')


for row in tables:
    tagstr = '000000000000000000000000000000000000000000'
    indexlist = getCom_cat_indexlist(row['com_cat_name'], row['com_sub_cat_name'])
    newtagstr = changeTagIndex(tagstr, indexlist)
    row['tag'] = int(newtagstr,2)
    com_full_name = getCom_Full_name(row['com_id'])
    if com_full_name and com_full_name not in ['未透露','未披露',u'未透露',u'未披露', u' ', ' ']:
        row['com_full_name'] = com_full_name
        orglist, recentlist = getCom_invest_org(row['com_id'])
        for org in orglist:
            if org.get('org_name'):
                saveorgtocsvfile(org['org_name'])
        row['top'] = checktop(orglist)
        roundstr = row['invse_round_id']
        row['invse_round_id'] = getRoundId(roundstr)
        latest = row['invse_detail_money']
        total = row['invse_total_money']
        money, currency = handleMoney(latest)
        newlatest = moneyToCNY(money, currency)
        row['latest'] = newlatest
        totalmoney, totalcurrency = handleMoney(total)
        row['total'] = totalmoney
        for recentorg in recentlist:
            row['invest_org'] = recentorg
            savetocsvfile(row)

