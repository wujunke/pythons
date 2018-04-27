#coding=utf-8
import json

import requests

allline = 0
for item in range(1,3,1):

    filepath = "data2/itjuzi-data%s" % item
    with open(filepath) as file:
        aaaa = 0
        for line in file:
            dic = json.loads(line)
            dic['investormerge'] = 1
            if isinstance(dic['invsest_with'],dict):
                values = []
                for key,value in dic['invsest_with'].items():
                    values.append(value)
                dic['invsest_with'] = values
            aaaa = aaaa + 1
            res = requests.post('http://192.168.1.201:8000/mongolog/event',data=json.dumps(dic),headers={'Content-Type':'application/json'}).content
            res = json.loads(res)
            if res['code'] == 1000:
                allline = allline + 1
                if allline % 1000 == 0:
                    print allline
            elif res['code'] == 8001:
                pass
            else:
                print '错误数据' + str(item) + '第%s行' % aaaa
                print res

filepath = 'data2/itjuzi-inmerge-data1'
with open(filepath) as file:
    aaaa = 0
    for line in file:
        dic = json.loads(line)
        dic['investormerge'] = 2
        aaaa = aaaa + 1
        res = requests.post('http://192.168.1.201:8000/mongolog/event', data=json.dumps(dic),
                            headers={'Content-Type': 'application/json'}).content
        res = json.loads(res)
        if res['code'] == 1000:
            allline = allline + 1
            if allline % 1000 == 0:
                print allline
        elif res['code'] == 8001:
            pass
        else:
            print '错误数据' + '第%s行' % aaaa
            print res

filepath = 'data2/itjuzi-out-data1'
with open(filepath) as file:
    aaaa = 0
    for line in file:
        dic = json.loads(line)
        dic['investormerge'] = 1
        if isinstance(dic['invsest_with'], dict):
            values = []
            for key, value in dic['invsest_with'].items():
                values.append(value)
            dic['invsest_with'] = values
        aaaa = aaaa + 1
        res = requests.post('http://192.168.1.201:8000/mongolog/event', data=json.dumps(dic),
                            headers={'Content-Type': 'application/json'}).content
        res = json.loads(res)
        if res['code'] == 1000:
            allline = allline + 1
            if allline % 1000 == 0:
                print allline
        elif res['code'] == 8001:
            pass
        else:
            print '错误数据' + '第%s行' % aaaa
            print res

filepath = 'data2/itjuzi-outmerge-data1'
with open(filepath) as file:
    aaaa = 0
    for line in file:
        dic = json.loads(line)
        dic['investormerge'] = 2
        aaaa = aaaa + 1
        res = requests.post('http://192.168.1.201:8000/mongolog/event', data=json.dumps(dic),
                            headers={'Content-Type': 'application/json'}).content
        res = json.loads(res)
        if res['code'] == 1000:
            allline = allline + 1
            if allline % 1000 == 0:
                print allline
        elif res['code'] == 8001:
            pass
        else:
            print '错误数据' + '第%s行' % aaaa
            print res



# filepath = 'itjuzi-cat'
# with open(filepath) as file:
#     aaaa = 0
#     for line in file:
#         dic = json.loads(line)
#         aaaa = aaaa + 1
#         res = requests.post('http://192.168.1.201:8000/mongolog/cat', data=json.dumps(dic),
#                             headers={'Content-Type': 'application/json'}).content
#         res = json.loads(res)
#         if res['code'] == 1000:
#             allline = allline + 1
#             if allline % 1000 == 0:
#                 print allline
#         elif res['code'] == 8001:
#             pass
#         else:
#             print '错误数据' + '第%s行' % aaaa
#             print res

filepath = '2017-09-30-cat/location'
with open(filepath) as file:
    aaaa = 0
    for line in file:
        aaaa = aaaa + 1
        res = requests.post('http://192.168.1.201:8000/mongolog/cat', data=json.dumps(line),
                            headers={'Content-Type': 'application/json'}).content
        res = json.loads(res)
        if res['code'] == 1000:
            allline = allline + 1
            if allline % 1000 == 0:
                print allline
        elif res['code'] == 8001:
            pass
        else:
            print '错误数据' + '第%s行' % aaaa
            print res
