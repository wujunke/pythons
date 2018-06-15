#coding=utf-8
import json
import random

import requests
import time

url = ' https://rong.36kr.com/n/api/column/0/company?sortField=HOT_SCORE'

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'br, gzip, deflate',
    'Accept-Language': 'zh-cn',
    'X-Tingyun-Id':'Dio1ZtdC5G4;r=78204299',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'rong.36kr.com',
    'Referer': 'https://rong.36kr.com/list/detail&?sortField=HOT_SCORE',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'Z-XSRF-TOKEN=eyJpdiI6ImhQa0k1XC9XWlpOd3VRNFlFUlJ3SGtnPT0iLCJ2YWx1ZSI6Illxc3phM2M4b2s2NmZUZnZmVFRGMlB5REdkb1wvZHRkdWk4ZDJONENZcHRiXC9SUWVPRUd6cGgzamNIeWN6RlNVV1N5dTloSDl3UE5YK2greFRROEdSUnc9PSIsIm1hYyI6IjYzZmIzNTkwMDAxYTI0MmFlZDEzOWFiODNiNzQwMjBiNzRiNjE5NDBhZDhlMmNiYTkyMjk0ZjgyYmRiNWJkMTgifQ%3D%3D; krchoasss=eyJpdiI6Ilg5bmdGSVwva2F5SGJHd1VrQWxPTll3PT0iLCJ2YWx1ZSI6IkNWRWJSbkpGaU50NllMTVVGK2RsaTU5dTdLb1FFTnVCZjJSbWM1bXVzOVlxNEtqN3pXaEZSd2Z3aTk0SGJvRHBLRElYNTd4bmtxaGRDRTJJaUp6UVdRPT0iLCJtYWMiOiI2MDdkYmNhZTNjMTE1ZTA3ZWRmOGZiY2MwMGUzYTY5ODIzOTg4NmU2MjYxNzc0ZjhhOTczOTc0MzA3NWU4N2Q5In0%3D; MEIQIA_EXTRA_TRACK_ID=152CCejE5FvZOExdNT5VaiQnC2S; kr_plus_utype=4; acw_tc=AQAAAI35LAcApg0AX3iptKae7wQyH0hR; kr_plus_id=1326029038; kr_plus_token=LIlxDt2eao_UXwzMdTu82hFkMJuMi673525_1___; krid_user_id=1326029038; krid_user_version=6; Hm_lvt_e8ec47088ed7458ec32cde3617b23ee3=1527132687; _kr_p_se=390fca41-fd0c-4e85-ac33-af8289407412; download_animation=1; kr_stat_uuid=5NMfw25453793'
}
iplist = [
          # '119.28.194.66:8888',
          # '113.200.214.164:9999',
          # '123.161.16.48:9797',
          # '27.44.161.252:9999',
          # '14.117.208.19:9797',
          # '114.239.201.237:61234',
          # '121.234.245.182:61234',
          # '183.56.177.130:808',
          '115.229.112.82:9000',
          # '183.158.162.189:1246'
          ]

def rand_proxie():
    return {'http':'http://%s' % iplist[random.randint(0, len(iplist)) - 1],}

def getPage(page):
    proxy = rand_proxie()
    res = requests.get(url + '&p=%s' % page, headers=headers, proxies=proxy).content
    res = json.loads(res)

    data = res['data']['pageData']['data']
    return data

def savedata(datalist):
    for data in datalist:
        f = open('jingzhun2', 'a')
        content = json.dumps(data, ensure_ascii=False).encode('utf-8')
        f.writelines(content)
        f.writelines('\n')
        f.close()


def getandsavepage(i):
    data = getPage(i)
    if len(data) > 0:
        savedata(data)
        print 'succeed， page = %s '% i
    else:
        print 'failed，retry，page = %s '% i
        time.sleep(3)
        getandsavepage(i)


for i in range(1, 6292):
    time.sleep(5)
    getandsavepage(i)
