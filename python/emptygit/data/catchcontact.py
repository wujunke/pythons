#coding=utf-8
import json
import os
import random
import re
import traceback

import requests
from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

Cookie = 'gr_user_id=3e9524a2-4693-416b-8c3c-dc8432051a65; acw_tc=AQAAAHqI7j5POQAARonnZWVgg0YNhC9s; MEIQIA_EXTRA_TRACK_ID=0vqN2YLRaP4z6UN9O4TzPsgXpYC; pgv_pvi=1923164160; pgv_si=s8890313728; _gat=1; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1509688884,1509702469; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1509704826; identity=18616837957%40test.com; remember_code=.aXHurL2KA; unique_token=439977; gr_session_id_eee5a46c52000d401f969f4535bdaa78=fb030942-37f1-43c1-ad9e-1e5bcaa62c11; gr_cs1_fb030942-37f1-43c1-ad9e-1e5bcaa62c11=user_id%3A439977; _ga=GA1.2.713347647.1509688885; _gid=GA1.2.1398237094.1509688885; Hm_lvt_80ec13defd46fe15d2c2dcf90450d14b=1509704830; Hm_lpvt_80ec13defd46fe15d2c2dcf90450d14b=1509704830; session=67dc0b9e908962b169ace06d194f82713e7c0c34; user-radar.itjuzi.com=%7B%22n%22%3A%22%5Cu6854%5Cu53cb9ef285e61d740%22%2C%22v%22%3A3%7D'

headers = {
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'radar.itjuzi.com',
            'Referer':'http://radar.itjuzi.com///company?phpSessId=e65ca8471446469d5e68b8885ff06f67fc0d31db?phpSessId=d87230bfa03a3885aa4471da7ab09491948fff74',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie':Cookie,
}


iplist=['124.115.157.54','114.215.102.168:8081','111.56.5.42','180.153.58.154:8088','58.210.218.106:80']

proxie = {
    'http' : 'http://%s' % iplist[3] ,
    # 'https': 'https://103.240.10.29:53281'
}

url_company_detail = 'http://radar.itjuzi.com/company/'

base_url = 'http://192.168.1.201:8000/'

token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'


# def getCompanyName(com_id):
#     html = requests.get(url_company_detail + '%s' % com_id, headers=headers, proxies=proxie).content
#     soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
#     com_name = str(soup.title.text).replace(' | 桔子雷达', '')
#     return com_name
#
#
# def updateCompanyName(com_id,com_name):
#     dic = {}
#     dic['com_id'] = com_id
#     dic['com_name'] = com_name
#     res = requests.put(base_url + 'mongolog/proj', data=json.dumps(dic),
#                         headers={'Content-Type': 'application/json', 'token': token}).content
#     res = json.loads(res)
#     if res['code'] == 1000:
#         print '修改com--' + str(res['result'].get('com_id', None))
#         pass
#     elif res['code'] == 8001:
#         # break
#         pass
#         # print '重复company'
#     else:
#         print '错误数据'
#         print res
#
#
# def getCompany(page_index):
#     res = requests.get(base_url + 'mongolog/proj?com_name=...&page_index=%s'%page_index,
#                        headers={'Content-Type': 'application/json', 'token': token}).content
#     res = json.loads(res)
#     if res['code'] == 1000:
#         projlist = res['result']['data']
#         if len(projlist) == 10:
#             return True,projlist
#         else:
#             return False,projlist
#
# def getEvent(page_index):
#     res = requests.get(base_url + 'mongolog/event?page_index=%s'%page_index,
#                        headers={'Content-Type': 'application/json', 'token': token}).content
#     res = json.loads(res)
#     if res['code'] == 1000:
#         projlist = res['result']['data']
#         if len(projlist) == 10:
#             return True,projlist
#         else:
#             return False,projlist
#
#
#
# def updateEvent(event_id):
#     res = requests.put(base_url + 'mongolog/event?id=%s' % event_id,
#                        headers={'Content-Type': 'application/json', 'token': token}).content
#     res = json.loads(res)
#     if res['code'] == 1000:
#         print 'event'
#         pass
#     elif res['code'] == 8001:
#         # break
#         pass
#         # print '重复company'
#     else:
#         print '错误数据'
#         print res
#
#
#
#
# page = 1
# isRepeat = True
# while isRepeat:
#     isRepeat,projlist = getEvent(page)
#     for proj in projlist:
#         try:
#             updateEvent(proj['id'])
#         except Exception as err:
#             print traceback.format_exc()
#     page+=1
# os.system("poweroff")



    # res = soup.find_all('span', class_='text-main')
# # res.find
# ll = ['mobile','email','address']
# i = 0
#
# response = {}
#
# for ss in res:
#     response[ll[i]] = ss.text
#     i = i + 1
# res = soup.find('div', class_='company-title')
# # print res.text
#
# # res = soup.find_all('ul', class_='cont-news-list')
# # news = []
# # for ss in res:
# #     # print ss.name
# #     lilist = ss.find_all('li')
# #     for li in lilist:
# #         plist = li.find_all('p')
# #         dic = {}
# #         for p in plist:
# #             a = p.find('a')
# #             if a:
# #                 dic['title'] = a.text
# #                 dic['link'] = a['href']
# #             else:
# #                 dic['time'] = p.text.split(' ')[0]
# #         news.append(dic)
# #
# # response['news'] = news
#
# # print response
# #
# # html = requests.get(url_company_detail,headers=headers,proxies=proxie).content
# # # print html
# #
# #
# # soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
# # res = soup.find_all('span', class_='text-main')
# # # res.find
# # ll = ['mobile','email','address']
# # i = 0
# #
# # response = {}
# #
# # for ss in res:
# #     response[ll[i]] = ss.text
# #     i = i + 1
# #
# # res = soup.find_all('ul', class_='cont-news-list')
# # news = []
# # for ss in res:
# #     # print ss.name
# #     lilist = ss.find_all('li')
# #     for li in lilist:
# #         isnews = False
# #         plist = li.find_all('p')
# #         dic = {}
# #         for p in plist:
# #             a = p.find('a')
# #             if a:
# #                 isnews = True
# #                 dic['title'] = a.text
# #                 dic['link'] = a['href']
# #             else:
# #                 dic['time'] = p.text.split(' ')[0]
# #         if isnews:
# #             news.append(dic)
# #
# # response['news'] = news
# #
# # print response



'''
获取公司网站链接
'''
file_object = open('contact.html')
try:
    html = file_object.read( )
finally:
    file_object.close( )
# html = requests.get(url_company_detail,headers=headers,proxies=proxie).content
# print html
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
# a_s = soup.find_all('a',target='_blank',)
# for div in a_s:
#     if div.i:
#         i = div.i
#         if i['class']:
#             if ' '.join(i['class']) == u'fa fa-link t-small':
#                 print div['href']
# print res['href']


a_s = soup.find('a',class_='title-url',)
div = a_s['href']
print div