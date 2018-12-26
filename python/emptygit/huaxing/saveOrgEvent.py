#coding=utf-8
import json
import random

import requests
import time

from huaxing.huaxing_url import url_eventList,   replaceRes, writrFileLines


def getEventList(INST_ID, page, start):
    try:
        data = {
            'INST_ID': INST_ID,
            'useCondition': True,
            'YEAR': 2018,
            'page': page,
            'start': start,
            'limit': 100,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Pragma': 'no-cache',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Host': '10.101.11.2:8080',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Origin': 'http://10.101.11.2:8080',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
            'Referer': 'http://10.101.11.2:8080/ck/home',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=BAD741AA22DD7BE0B14F385B2DE5C893',
            'X-Requested-With': 'XMLHttpRequest'
        }
        res = requests.post(url_eventList, data=data, headers=headers).content
        res = replaceRes(res)
        res = json.loads(res)
        if res['success']:
            return res
    except Exception:
        print('request error')
    return None


# getEventList('535f5c36-e7b5-4037-8338-edbc55a2f5dc', 1, 0)

def getEvents(INST_ID, page, start, events=None):
    if not events:
        events = []
    response = getEventList(INST_ID, page, start)
    if response:
        events.extend(response['rows'])
        if response['total'] > 100*page:
            page += 1
            start += 100
            return getEvents(INST_ID, page, start, events)
        else:
            return events

orglist = []

with open('orglist', 'r') as f:
    lines = f.readlines()
    for line in lines:
        orglist.append(json.loads(line))

i = 1
for org in orglist:
    time.sleep(random.randint(10, 20))
    events = getEvents(org['INST_ID'], 1, 1)
    writrFileLines(events, 'events', 'a')
    print(i)
    i += 1




