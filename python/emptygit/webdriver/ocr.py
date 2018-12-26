#coding=utf-8

import json

import requests
import xlwt, sys
from future.backports.urllib import parse

reload(sys)
sys.setdefaultencoding('utf-8')

# 机构全称、标签、描述、投资事件（简介、网址、联系方式以及历史融资情况）、合伙人/投委会成员
def saveToFile(org_qs):
    wb = xlwt.Workbook(encoding='utf-8')
    style = xlwt.XFStyle()  # 初始化样式
    alignment = xlwt.Formatting.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 垂直对齐
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 水平对齐
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT  # 自动换行
    style.alignment = alignment
    ws_org = wb.add_sheet('IT桔子海外机构列表')
    ws_org.write(0, 0, '名称')
    ws_org.write(0, 1, 'url')
    ws_org.write(0, 2, 'haituo_id')


    ws_org_hang = 1
    for org in org_qs:

        ws_org.write(ws_org_hang, 0, str(org['org_name']))
        ws_org.write(ws_org_hang, 1, str(org['url']))
        ws_org.write(ws_org_hang, 2, str(org['haituo_id']))
        ws_org_hang += 1

    wb.save('outorg.xls')






orgNameIdlist = []
with open("/Users/investarget/pythons/python/emptygit/addInvestEvent/name_id_comparetable","r") as f:
    lines = f.readlines()
    for line in lines:
        orgNameIdlist.append(json.loads(line.replace('\n','')))


def checkIdExist(orgid):
    isExist = True
    url = 'https://api.investarget.com/org/?ids=%s' % orgid
    orglist = json.loads(requests.get(url).content).get('result', {}).get('data', [])
    if len(orglist) > 1:
        print('有多个搜索结果--%s' % orgid)
    elif len(orglist) == 1:
        print(orglist[0]['id'])
    else:
        isExist = False
    return isExist


def getOrgIdByOrgname(orgname):
    orgid = None
    for org in orgNameIdlist:
        if org['itjuzi_name'] == orgname:
            orgid = org['haituo_id']
    if orgid:
        isExist = checkIdExist(orgid)
        if not isExist:
            orgid = None
    return orgid


orglist = []

with open('org.json', 'r') as f:
    lines = f.readlines()
    for line in lines:
        org = json.loads(line)
        orgid = getOrgIdByOrgname(org['org_name'])
        if not orgid:
            orgid = ''
        org['haituo_id'] = orgid
        orglist.append(org)


saveToFile(orglist)