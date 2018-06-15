#coding=utf-8
import json

import requests


# base_url = 'http://192.168.1.251:8080/'
base_url = 'http://192.168.1.201:8000/'
token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'


headers = {
    'Content-Type': 'application/json',
    'token': token,
    'source': '1',
}


def getevents(page):
    event = None
    res = requests.get(base_url + 'user/event/?page_index=%s' % page, headers=headers).content
    res = json.loads(res)
    if res['code'] == 1000:
        event = res['result']['data']
    return event

def getAndSaveUserCom_cat(userid, com_id, event_id, round):
    com_data = getCom_Data(com_id)
    if com_data:
        data = {
            'user': int(userid),
            'round': round,
            'Pindustrytype': com_data['com_cat_name'],
            'industrytype': com_data['com_sub_cat_name'],
        }
        saveUserEventTag(event_id, data)


def getCom_Data(com_id):
    com_data = None
    res = requests.get(base_url + 'mongolog/proj?com_id=%s' % com_id,
                       headers=headers).content
    res = json.loads(res)
    if res['code'] == 1000:
        com_list = res['result']['data']
        if len(com_list) > 0:
            com_data = com_list[0]
    return com_data




def saveUserEventTag(event_id, data):
    res = requests.put(base_url + 'user/event/%s/'% event_id, data=json.dumps(data), headers=headers).content
    res = json.loads(res)
    if res['code'] != 1000:
        print res['errormsg']


i = 0
while i < 1000:
    i += 1
    events = getevents(i)
    for event in events:
        useid = event['user']
        com_id = event['com_id']
        event_id = event['id']
        round = event['round']
        if com_id:
            getAndSaveUserCom_cat(useid, com_id, event_id, round)