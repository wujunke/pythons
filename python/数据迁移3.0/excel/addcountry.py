#coding=utf-8
import csv
import json

from pypinyin import slug as hanzizhuanpinpin
import requests

csvfile = csv.reader(open('/Users/investarget/Desktop/python/数据迁移3.0/excel/exceldata/China.csv','r'))


chinadic = {

}

for stu in csvfile:
    province  = str(stu[1]).replace('市','').replace('省','').replace('自治区','').replace('特别行政区','')\
        .replace('壮族','').replace('维吾尔','').replace('回族','')
    city = str(stu[2])
    # print province,citylevel


    if city == '':
        # print province
        chinadic[province] = []
    else:
        # print province,city
        citylist = chinadic[province]
        if city not in citylist:
            chinadic[province].append(city)
headers = {
        'source':'2',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }



for province, citylist in chinadic.items():
    data = {
        'countryC':province,
        'countryE':hanzizhuanpinpin(unicode(province, "utf-8"),separator=''),
        'areaCode':86,
        'parent':219,
        'level':3,

    }
    response = requests.post('http://192.168.1.201:8000/source/country',data=json.dumps(data),headers=headers).content
    response = json.loads(response)
    if response['code'] == 1000:
        parentId = response['result']['id']
        for city in citylist:
            city = str(city)
            if '市' in city:
                countryE = str(hanzizhuanpinpin(unicode(city.replace('市',''), "utf-8"), separator=' ')).capitalize().replace(' ','') + ' City'
            elif '自治州' in city:
                countryE = str(hanzizhuanpinpin(unicode(city.replace('自治州',''), "utf-8"), separator=' ')).capitalize().replace(' ','') + ' Autonomous Prefecture'
            else:
                countryE = hanzizhuanpinpin(unicode(city, "utf-8"), separator=' ')
            data = {
                'countryC': city,
                'countryE': countryE,
                'areaCode': 86,
                'parent': parentId,
                'level': 4,
            }
            response = requests.post('http://192.168.1.201:8000/source/country', data=json.dumps(data),headers=headers).content
            response = json.loads(response)
            if response['code'] == 1000:
                pass
            else:
                print '新增城市失败：（%s）-》（%s）'%(province,city)

    else:
        print '新增省失败：（%s）' % (province)
