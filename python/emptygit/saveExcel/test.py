#coding=utf-8
# import json
#
# import requests
#
# url = 'https://api.investarget.com/mongolog/cat'
# res = requests.get(url, headers={'token':'a7305831f4903690feb349c16ab37f9b4962197305ba32c7'}).content
# res = json.loads(res)
#
# datas = res['result']['data']
#
#
# p_cat_list = []
# for data in datas:
#     if not data['p_cat_id']:
#         print data['cat_name']
#         p_cat_list.append(data['cat_name'])
#
# print p_cat_list
#! /usr/bin/python
#-* coding: utf-8 -*
# __author__ ="tyomcat"
import time
import sys
# 生产者
def produce(l):
    i=0
    while 1:
        if i < 10:
            l.append(i)
            yield 9
            i=i+1
            # yield i
            # i=i+2
            time.sleep(1)
        else:
            return
# 消费者
def consume(l):
    p = produce(l)
    while 1:
        try:
            p.next()
            while len(l) > 0:
                print l.pop()
        except StopIteration:
            sys.exit(0)
if __name__ == "__main__":
    l = []
    consume(l)
