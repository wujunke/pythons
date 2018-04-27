#coding=utf-8
import json

import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def saveInfo(info,name):
    f = open(name, 'a+')
    for key,values in info.items():
        f.writelines(json.dumps(key).decode('unicode_escape'))
        f.writelines(':')
        f.writelines(json.dumps(values).decode('unicode_escape'))
        f.writelines(';')
    f.writelines('\n')
    f.close()

catlist = [ {'cat':'金融','sub_cat' :'保险'},
            {'cat':'金融','sub_cat' :'理财'},
            {'cat':'金融','sub_cat' :'信用及征信'},
            {'cat':'房产服务','sub_cat' :'房产金融'},
            {'cat':'房产服务','sub_cat' :'租房'},
            # {'cat':'房产服务','sub_cat' :'理财'},
            # {'cat':'金融','sub_cat' :'理财'},
           ]


token = '46b9a5c726b9f3a85fcd35374e008396309d79154f169277'
aa = 1
for cat in catlist:
    name = 'cat%s'%aa
    aa = aa + 1
    x = 1
    while x < 7000:
        res = requests.get('http://192.168.1.201:8000/mongolog/proj?sub_cat=%s&cat=%s&page_index=%s'%(cat['sub_cat'],cat['cat'],x)).content
        res = json.loads(res)
        companylist = []
        x = x + 1
        if res['code'] == 1000:
            companylist = res['result']['data']
            for com in companylist:
                ress = requests.get('http://192.168.1.201:8000/mongolog/event?com_id=%s' % com['com_id']).content
                ress = json.loads(ress)
                if ress['code'] == 1000:
                    eventlist = ress['result']['data']
                else:
                    eventlist = []
                    print ress + com
                com['event'] = eventlist
                saveInfo(com,name)
            if len(companylist) < 10:
                x = 7000
        else:
            print res