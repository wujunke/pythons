#coding=utf-8


import json
import random
import requests

from data2.itjuzi_config import base_url, token


def getEvent(page):
    events = []
    headers = {
        'token': token,
        'source': '1',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    response = requests.get(base_url + 'mongolog/event?page_index=%s'%page, headers=headers).content
    response = json.loads(response)
    if response['code'] != 1000:
        print '获取失败--%s' % str(response)
    else:
        events = events + response['data']
    return events



def update(event_id, event):
    headers = {
        'token': token,
        'source': '1',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    newinvest_with = []
    for invest_with in event['invsest_with']:
        orgid = getOrgIdByOrgname(invest_with.get('invst_name', None))
        newinvest_with.append({
                                'url':invest_with['url'],
                                'invst_name':invest_with['invst_name'],
                                'org_id':orgid
                               })
    data = {
        'invsest_with':newinvest_with
    }
    response = requests.put(base_url + 'mongolog/event?id=%s'%event_id, data=data, headers=headers).content
    response = json.loads(response)
    if response['code'] != 1000:
        print '获取失败--%s' % str(response)




orglist = []

def getOrgIdByOrgname(orgname):
    orgid = None
    if orgname and orgname != '未透露':
        for org in orglist:
            if org['com_name'] == orgname:
                orgid = org['com_id']
    return orgid
