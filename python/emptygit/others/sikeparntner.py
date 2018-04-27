#coding=utf-8
import urllib
import cookielib
import requests
import re
import sys
import HTMLParser
from bs4 import BeautifulSoup

# def encode_multipart_formdata(fields):
#     '''''
#             该函数用于拼接multipart/form-data类型的http请求中body部分的内容
#             返回拼接好的body内容及Content-Type的头定义
#     '''
#     import random
#     import os
#     BOUNDARY = '---------------------------1882514727548445438722663542'
#     CRLF = '\r\n'
#     L = []
#     for (key, value) in fields.items():
#         L.append('--' + BOUNDARY)
#         L.append('Content-Disposition: form-data; name="%s"' % key)
#         L.append('')
#         L.append(value)
#     L.append('--' + BOUNDARY + '--')
#     L.append('')
#     body = CRLF.join(L)
#     # content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
#     return body
#
#
# url= 'https://locatr.cloudapps.cisco.com/WWChannels/LOCATR/performAdvanceSearch.do'
# url = url.decode(sys.stdin.encoding).encode("utf-8")
# s = requests.session()
# heders = {
#     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Connection':'keep-alive',
#     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:53.0) Gecko/20100101 Firefox/53.0',
#     'Origin':'https://locatr.cloudapps.cisco.com',
#     'Referer':'https://locatr.cloudapps.cisco.com/WWChannels/LOCATR/performAdvanceSearch.do',
#     'Host':'locatr.cloudapps.cisco.com',
#     'Upgrade-Insecure-Requests':'1',
#     'Content-Type':'multipart/form-data; boundary=---------------------------1882514727548445438722663542',
#     'Content-Disposition':'form-data; name="latitude"',
#     'Cookie':'JSESSIONID=D44CF99F83E835FA2E395ACD9F58AE80; ts=1493881079908; ObSSOCookie=J2qGMLEUT%2By2Sk8PcAK%2B%2Fv6vl5r8Z9W7xOfdL%2Beism5Oe%2FqOSdArgTFXz%2FeIzWy5%2BnEcc3klYEtSgMzmZfoadeHWfRQVcbokcMRT4255NI%2Fzo3tIHVvwCZxFokMNBWnN%2FfZb1xR3BJr8UVzKaaGOh%2BI9I8mqVeKOna4p2FrIAQ1%2FKfV%2F0dwtv15sJKyF11mQS%2FLP9fkh1xBre%2FanvgPQvfU9tLtvbyVksThMN3TnqnPYpCEuZl6a9axk9pu60qjp12R8%2FDlzx7HjMVQmUvHPZrGQnvFW0ieQuJQWU1LOSnLaattvkgkTBolvAkzjoOQIA5mtb7jFJY53fEJL9qMWkMcFkUJbKoxO%2BOOCcIGuGI7AOs2kyHcol82HsHmloJS0ySqz6Y85L6drAiNFbRDq7IknmqAE8xROCvoKS8D4pgXem1GZVdwWXiVa2Rl5hi2eOfZs9zc1AudJYQu2dJVupUOwUbap%2FB17y3UyktTpOWvtls42eK3VpYipOuiubLV1x1Raed7XHCDR5PWJkRYfwg%3D%3D; CP_GUTC=173.36.126.22.1493881045876252; GEAR=locatrprdlae-un5j6z4xprd-2-locatrprdlae; SERVERID=cookielocatr_2; OPTOUTMULTI=0:0%7Cc2:0%7Cc1:0%7Cfunction%20(iterator)%20%7B%0A%20%20%20%20var%20index%20=%200:1%7Cfunction%20(iterator)%20%7B%0A%20%20%20%20var%20index%20=%200; utag_main=v_id:015bd23fd71c000c9249137c6c5501052004c00f00bd0$_sn:2$_ss:0$_st:1493894377372$ses_id:1493884453444%3Bexp-session$_pn:13%3Bexp-session; hbx_lid=no_id; AMCV_B8D07FF4520E94C10A490D4C%40AdobeOrg=-1248264605%7CMCMID%7C04909442894187309323347176412810276603%7CMCAAMLH-1494485852%7C11%7CMCAAMB-1494493958%7CcIBAx_aQzFEHcPoEv0GwcQ%7CMCOPTOUT-1493896358s%7CNONE%7CMCAID%7CNONE; AMCVS_B8D07FF4520E94C10A490D4C%40AdobeOrg=1; s_ptc=383%5E%5E11%5E%5E2%5E%5E204%5E%5E415%5E%5E833%5E%5E600000%5E%5E188%5E%5E600000; s_cc=true; s_ppvl=locatr.cloudapps.cisco.com%2Fwwchannels%2Flocatr%2Fopenbasicsearch.do%2C92%2C92%2C846%2C1463%2C846%2C1920%2C1080%2C1%2CP; s_ppv=locatr.cloudapps.cisco.com%2Fwwchannels%2Flocatr%2Fperformadvancesearch.do%2C15%2C15%2C475%2C1463%2C475%2C1920%2C1080%2C1%2CP; s_sq=%5B%5BB%5D%5D; cdc.cookie.newUser=1494485887733; _ga=GA1.2.1320785845.1493881194; _gid=GA1.2.128621710.1493891750; _bizo_bzid=d6c22699-eb76-47ae-9b17-31d788b8990f; _bizo_cksm=7D169E2D25E59ADE; _gd_visitor=ecad72da-4756-49e8-80af-b1791effba37; _gd_session=376faf2c-9cc1-4931-84e3-41030e446754; _gd_svisitor=d9010f177b4a000070d10a5911030000973b0300; _bizo_np_stats=14%3D221%2C; liveagent_oref=https://locatr.cloudapps.cisco.com/WWChannels/LOCATR/performAdvanceSearch.do; liveagent_vc=2; liveagent_sid=7668a9d3-6245-4be9-9f71-879b5d2bb7bb; liveagent_ptid=7668a9d3-6245-4be9-9f71-879b5d2bb7bb; gpv_v9=locatr.cloudapps.cisco.com%2Fwwchannels%2Flocatr%2Fopenbasicsearch.do; _uetsid=_uet3a1db03c'}
# form_data = {
#     'country':'US',
#     'companyName':'',
#     'countryCd':'US',
#     'countryName':'USA',
#     'certifiedPartner':'GOLD',
#     'certifiedPartner':'PREMIER',
#     'latitude':'37.09024',
#     'state':'',
#     'searchType':'',
#     'city':'',
#     'zip':'',
#     'longitude':'-95.71289100000001',
#     'lonlatRequired':'N',
#     'showMultiCountry':'N',
#     'keyWord':'',
#     'addressaddress':'',
#     'companyNameSearchType':'M',
#     'sortType':'25',
#     'countryDesc':'UNITED STATES',
#     'pageDropDownUp':'1',
#     'advanceAddress':'',
#     'advanceCountry':'US',
#     # 'sortType':'DEFAULT',
#     # 'sortType':'25',
# }
#
# body = encode_multipart_formdata(form_data)
# # print body
# # print 'sss'
# # result = s.post(url,headers=heders,data=body)
# result = s.get(url,headers=heders)
# # s.cookies.save()
# # print s.cookies
# html = result.text
# print html



# filename = 'htssss.html'
# html = open(filename,"r").read()
# soup = BeautifulSoup(html, 'html.parser',from_encoding='utf-8')
#
#
# resp2 = soup.findAll('td',attrs={'align':"left",'valign':"top",})
# lisss = []
# with open('sike.txt', 'a') as f:
#     for i in range(0,99,4):
#         st = resp2[i+1].text +';'+resp2[i+2].text+';'+resp2[i+3].text
#         re = st.replace('\n','').replace('				','').replace('\t','')
#         print re
#         f.write(re.encode('utf-8') + '\n')

filename = 'sike5.txt'
str = open(filename,"r").read()
str.replace('网站','*******')
with open('sike6.txt', 'a') as f:
    f.write(str)

# arr = str.split('网站')
# print len(arr)
# # for aaa in arr:
# #     minarr = aaa.split('\n')
# #     print minarr[0]
# #     print minarr[1:-1]
#
# with open('sike6.txt', 'a') as f:
#     for aaa in arr:
#         minarr = aaa.split('\n')
#         minarr0 = '网站' + minarr[0]
#         f.write(minarr0 + '\n')
#         if len(minarr) >2:
#             minstr = minarr[1]+';'
#             for strs in minarr[2:-2]:
#                 minstr = minstr + strs
#             minstr = minstr + ';' + minarr[-2] + minarr[-1]
#             f.write(minstr)