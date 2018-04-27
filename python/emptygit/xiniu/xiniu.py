#coding=utf-8
import json

import requests


# 烯牛数据cookie
import time

Cookie = 'userid=6430; keeploginsecret=RGXK3UDYZY273YLZULZUCQAIHYI13WMN; token=TVF8USW6P8CYBDLU79QG3XOMF022JNQS; Hm_lvt_42317524c1662a500d12d3784dbea0f8=1514960034,1515037345; Hm_lpvt_42317524c1662a500d12d3784dbea0f8=1515058628; location=http%3A%2F%2Fwww.xiniudata.com%2F%23%2Fcompany%2Fbjbzhxxkjxgs%2Foverview'
# 海拓3.0 token
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
base_url = 'http://39.107.14.53:8080/'
sleeptime = 10


# 获取公司code  url
# http://www.xiniudata.com/api/search/complete  post body={"data":"SIA国际艺术教育"}

# 获取公司基本信息
# http://www.xiniudata.com/api2/service/company/basic  post  body = {payload: {code: "hfjHyphen"}}    code在codeurl返回

# 获取公司工商信息
# http://www.xiniudata.com/api2/service/gongshang/list_by_corporate  post  body = {payload: {corporateId: 4995}}  corporateId 在基本信息接口返回
search_url = "http://www.xiniudata.com/api/search/complete"
company_basic = "http://www.xiniudata.com/api2/service/company/basic"
company_gongshang = "http://www.xiniudata.com/api2/service/gongshang/list_by_corporate"



get_code_headers = {
            'Accept':'*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host':'www.xiniudata.com',
            'Origin':'http://www.xiniudata.com',
            'Referer':'http://www.xiniudata.com/search/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie':Cookie,
}


get_basic_headers = {
            'Accept':'*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host':'www.xiniudata.com',
            'Origin':'http://www.xiniudata.com',
            'Referer':'http://www.xiniudata.com/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest',
            'Cookie':Cookie,
}

get_gongshang_headers = {
            'Accept':'*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
            'Host':'www.xiniudata.com',
            'Origin':'http://www.xiniudata.com',
            'Referer':'http://www.xiniudata.com/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'Cookie':Cookie,
}


def get_comcode(com_name):
    com_code = None
    res = requests.post(search_url, data=json.dumps({"data": com_name}), headers=get_code_headers)
    if res.status_code == 200:
        result = json.loads(res.content)
        if result.has_key('name'):
            searchlist = result['name']
            if len(searchlist) > 0:
                com_code = searchlist[0]['code']
                print com_code
            else:
                print '未找到com_code**%s'%com_name
        else:
            print result
    else:
        print 'code请求出错，状态码--%s'%res.status_code
    return com_code


def get_combasic(com_code):
    corporateId = None
    data = json.dumps({"payload": {"code": com_code}})
    res = requests.post(company_basic, data=data, headers=get_basic_headers)
    if res.status_code == 200:
        result = json.loads(res.content)
        if result.has_key('companyVO'):
            companyVO = result['companyVO']
            company_info = companyVO['company']
            print  company_info
            com_web = company_info['website']
            com_name = company_info['name']
            corporateId = company_info['corporateId']
            if corporateId:
                print corporateId
            else:
                print '未找到basic**%s'%com_code
        else:
            print result
    else:
        print '基本信息请求出错，状态码--%s'%res.status_code
    return corporateId

def get_comgongshang(corporateId):
    projindustryinfo = None
    data = json.dumps({"payload": {"corporateId": corporateId}})
    res = requests.post(company_gongshang, data=data, headers=get_gongshang_headers)
    if res.status_code == 200:
        result = json.loads(res.content)
        if result.has_key('list'):
            gongshanglist = result['list']
            if len(gongshanglist) > 0:
                gongshanginfo = gongshanglist[0]
                # print gongshanginfo
                gongshangdic = json.loads(gongshanginfo)
                gongshangdic.pop('_id')
                projindustryinfo = {
                    'indus_member': gongshangdic.pop('members'),
                    'indus_shareholder': gongshangdic.pop('investors'),
                    'indus_busi_info': gongshangdic.pop('changeInfo'),
                    'indus_foreign_invest': gongshangdic.pop('invests'),
                    'indus_base': gongshangdic
                }
                print gongshangdic['name']
            else:
                print '未找到gongshang**%s'%corporateId
        else:
            print result
    else:
        print '工商请求出错，状态码--%s'%res.status_code
    return projindustryinfo




def get_gongshangwithname(com_name, com_id):
    com_code = get_comcode(com_name)
    if com_code:
        corporateId = get_combasic(com_code)
        if corporateId:
            gongshanginfo = get_comgongshang(corporateId)
            if gongshanginfo:
                gongshanginfo['com_id'] = com_id

                res = requests.post(base_url + 'mongolog/projinfo', data=json.dumps(gongshanginfo),
                                    headers={'Content-Type': 'application/json', 'token': token}).content
                res = json.loads(res)
                if res['code'] == 1000:
                    print '新增indus_info--' + str(res['result'].get('com_id', None))
                    pass
                elif res['code'] == 8001:
                    pass
                else:
                    # print filepath
                    print '错误数据indus_info----' + 'com_id=%s' % com_id
                    print res




def get_companglist(page_index):
    projlist = None
    res = requests.get(base_url + 'mongolog/proj?page_size=10&sort=true&page_index=%s' % page_index, headers={'Content-Type': 'application/json', 'token': token})
    if res.status_code == 200:
        res = json.loads(res.content)
        if res['code'] == 1000:
            projlist = res['result']['data']
        else:
            # print filepath
            print '获取全库项目列表有误----' + 'page_index=%s' % page_index
            print res
    return projlist





page_index = 1
while page_index < 9000:
    projlist = get_companglist(page_index)
    page_index += 1
    if projlist:
        for proj in projlist:
            com_id = proj['com_id']
            com_name = proj['com_name']
            get_gongshangwithname(com_name=com_name, com_id=com_id)
            time.sleep(sleeptime)





