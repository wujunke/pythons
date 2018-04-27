# -*- coding: utf-8 -*-
import codecs
import os
import traceback
import  xdrlib ,sys

import re
from pypinyin import slug as hanzizhuanpinpin
import requests
import xlrd
import json

reload(sys)
sys.setdefaultencoding('utf-8')

# 遍历文件夹下的文件，返回路径list
def eachFile(filepath):
    filelist = []
    pathDir =  os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s/%s' % (filepath, allDir))
        if child != '/Users/investarget/Desktop/投资机构/.DS_Store':
            filelist.append(child)
    return filelist

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print str(e)

#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的索引  ，by_index：表的索引
def excel_table_byindex(file,colnameindex=0,by_index=0):
    print file
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames = ['col0',	'col1',	'col2', 'col3', 'col4', 'col5', 'col6', 'col7',] #某一行数据
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list

# token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'
baseurl = 'http://192.168.1.201:8000/'

token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
# baseurl = 'https://api.investarget.com/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }



def main():

    # filepathlist = eachFile('/Users/investarget/Desktop/投资机构')
    filepathlist = [
                    '/Users/investarget/Desktop/投资机构/投资机构（前200）/凯鹏华盈.xls',
                    '/Users/investarget/Desktop/投资机构/投资机构（前400）/苏州昆吾九鼎.xls',
                    '/Users/investarget/Desktop/投资机构/投资机构（前200）/基石资本.xls',
                    '/Users/investarget/Desktop/投资机构/投资机构（前600）/成都高投.xls',
                    '/Users/investarget/Desktop/投资机构/投资机构（前600）/东湖创投.xls',
                    '/Users/investarget/Desktop/投资机构/投资机构（前800）/嘉富诚.xls',
                    '/Users/investarget/Desktop/投资机构/投资机构（前200）/九鼎投资.xls',
                    '/Users/investarget/Desktop/投资机构/投资机构（前1400）/通用投资.xls',
                    '/Users/investarget/Desktop/投资机构/投资机构（前800）/国科嘉和.xls',
                    '/Users/investarget/Desktop/投资机构/投资机构（前200）/CVC.xls'
                    ]







    for filepath in filepathlist:
        aaa = []
        times = 0
        tables = excel_table_byindex(filepath)
        for row in tables:
            times = times + 1
            aaa.append(row)
        linedic = {
            '机构介绍': {'start': 0, 'end': 0, },
            '联系方式': {'start': 0, 'end': 0, },
            '机构描述': {'start': 0, 'end': 0, },
            '管理团队': {'start': 0, 'end': 0, },
            '投资策略': {'start': 0, 'end': 0, },
            '管理基金': {'start': 0, 'end': 0, },
            '投资事件': {'start': 0, 'end': 0, },
            '合作关系': {'start': 0, 'end': 0, },
            '退出分析': {'start': 0, 'end': 0, },
        }
        linelist = ['机构介绍', '联系方式', '机构描述', '管理团队', '投资策略', '管理基金', '投资事件', '合作关系', '退出分析']
        orgname = ''
        for i in range(0,len(aaa)):
            if aaa[i]['col0'] == '中文名称：':
                orgname = aaa[i]['col1']
            for tag in linelist:
                if aaa[i]['col0'] == tag:
                    linedic[tag] = {'start': i + 2}
                if aaa[i]['col0'] == '':
                    if aaa[i + 1]['col0'] != '地址：':
                        if linedic.get(tag, None):
                            if linedic[tag].get('end', 0) == 0 and i - 1 >= linedic[tag].get('start', 0) and linedic[tag].get('start', 0) != 0:
                                linedic[tag].update({'end':i - 1})

        # orgid = getOrgIdWithFullName(aaa[linedic['机构介绍']['start']]['col1'])  #简称匹配
        orgid = getOrgIdWithFullName(orgname)    #全称匹配

        # members = []
        # if linedic['管理团队']['start'] > 0 and linedic['管理团队']['end'] > linedic['管理团队']['start']:
        #     for i in range(linedic['管理团队']['start'], linedic['管理团队']['end'] + 1):
        #         fund = {
        #             'name': aaa[i]['col0'],
        #             'title': aaa[i]['col1'] if aaa[i]['col1'] != 'N/A' else None,
        #             'phone': aaa[i]['col2'] if aaa[i]['col2'] != 'N/A' else None,
        #             'email': aaa[i]['col4'] if aaa[i]['col4'] != 'N/A' else None,
        #         }
        #         if '【离职】' in fund['name'] or u'【离职】' in fund['name'] :
        #             pass
        #         else:
        #             members.append(fund)
        # for user in members:
        #     userid = getUserId(username=user['name'], orgid=orgid)
        #     if not userid:
        #         pass
        #         data = {
        #             'name':user['name'],
        #             'title':getTitleIdWithTitleC(user['title']),
        #             'org':orgid,
        #             'mobile':user['phone'],
        #             'email':user['email'],
        #         }
        #         response = requests.post(baseurl + 'user/unuser/', data=json.dumps(data), headers=headers).content
        #         response = json.loads(response)
        #         if response['code'] != 1000:
        #             print '新增用户失败--%s' % user['name'] + str(response)
        #     else:
        #         if user['email']:
        #             data = {
        #                 'email': user['email'],
        #             }
        #             response = requests.post(baseurl + 'user/chnageuser/%s'%userid, data=json.dumps(data), headers=headers).content
        #             response = json.loads(response)
        #             if response['code'] != 1000:
        #                 print '修改用户失败--%s' % user['name'] + str(response)



        # fundSize = aaa[linedic['机构介绍']['start']]['col6']
        # if fundSize != 'N/A':
        #     if '万' in fundSize:
        #         avl = '00'
        #     elif '亿' in fundSize:
        #         avl = '000000'
        #     else:
        #         avl = None
        #     if '美元' in fundSize:
        #         currency = 2
        #     else:
        #         currency = 1
        #     fundSize = re.findall(r"\d+\.?\d*", fundSize)[0]
        #     if avl:
        #         fundSize = fundSize.replace(',', '').replace('.', '') + avl
        #     else:
        #         fundSize = float(fundSize)
        # else:
        #     currency = None
        # orgsum = {
        #     'orgfullname':orgname,
        #     'orgnameC': aaa[linedic['机构介绍']['start']]['col1'] if aaa[linedic['机构介绍']['start']]['col1'] != 'N/A' else None,
        #     'orgnameE': aaa[linedic['机构介绍']['start'] + 1]['col1'] if aaa[linedic['机构介绍']['start'] + 1]['col1'] != 'N/A' else None,
        #     'fundSize': fundSize if currency else None,
        #     'orgtype': 1,
        #     'currency':currency if currency else 1,
        #     'fundSize_USD': fundSize if currency == 2 else None,
        #     'establishedDate': str(aaa[linedic['机构介绍']['start'] + 2]['col1']) + 'T12:00:00' if aaa[linedic['机构介绍']['start'] + 2]['col1'] != 'N/A' else None,
        #     'address':aaa[linedic['机构介绍']['end']]['col1'] if aaa[linedic['机构介绍']['end']]['col1'] != 'N/A' else None,
        #     'webSite':aaa[linedic['机构介绍']['start'] + 2]['col6'] if aaa[linedic['机构介绍']['start'] + 2]['col6'] != 'N/A' else None,
        # }
        # # print orgsum
        #
        # orgdesc = ''
        # for i in range(linedic['机构描述']['start'], linedic['机构描述']['end'] + 1):
        #     orgdesc = orgdesc + aaa[i]['col0']
        #
        # # print orgdesc
        #
        # investceluo = ''
        #
        # for i in range(linedic['投资策略']['start'], linedic['投资策略']['end'] + 1):
        #     investceluo = investceluo + aaa[i]['col0']
        #     investceluo = investceluo + aaa[i]['col1'] + '\n'
        #
        # # print investceluo
        # orgsum['description'] = orgdesc
        # orgsum['investmentStrategy'] = investceluo
        #
        # # print orgsum
        #
        #
        # #增加机构
        # response = requests.post(baseurl+'org/', data=json.dumps(orgsum), headers=headers).content
        # response = json.loads(response)
        # if response['code'] != 1000:
        #     print '新增失败--%s' % orgsum['orgfullname'] + str(response)
        # else:
        #     orgid = response['result']['id']
        #     f = open('org', 'a')
        #     key = str(orgsum['orgfullname'])
        #     content = '{\'%s\': %s}'% (key, orgid)
        #     f.writelines(content)
        #     f.writelines('\n')
        #     f.close()



        # #管理基金
        # managefund = []
        # if linedic['管理基金']['start'] > 0 and linedic['管理基金']['end'] > linedic['管理基金']['start']:
        #     for i in range(linedic['管理基金']['start'], linedic['管理基金']['end'] + 1):
        #         fund = {
        #             'fund': aaa[i]['col0'],
        #             'type': aaa[i]['col1'] if aaa[i]['col1'] != 'N/A' else None,
        #             'fundsource': aaa[i]['col2'] if aaa[i]['col2'] != 'N/A' else None,
        #             'fundraisedate': aaa[i]['col3'] + 'T12:00:00' if aaa[i]['col3'] != 'N/A' else None,
        #             'fundsize': unicode(str(aaa[i]['col4']) + str(aaa[i]['col5'])),
        #         }
        #         managefund.append(fund)

        #创建管理基金
        # for fund in managefund:
        #     funddic = {
        #             # 'orgfullname': fund['fund'],
        #             'orgnameC': fund['fund'],
        #             # 'orgnameE': fund['fund'],
        #             'orgtype': 1,
        #         }
        #     response = requests.post(baseurl + 'org/', data=json.dumps(funddic), headers=headers).content
        #     response = json.loads(response)
        #     if response['code'] != 1000:
        #         print '新增失败--%s' % fund['fund'] + str(response)
        #     else:
        #         orgid = response['result']['id']
        #         f = open('org', 'a')
        #         key = str(fund['fund'])
        #         content = '{\'%s\': %s}' % (key, orgid)
        #         f.writelines(content)
        #         f.writelines('\n')
        #         f.close()



        # #管理基金与机构建立关系
        # for fund in managefund:
        #     fund['org'] = orgid
        #     fund['fund'] = getOrgIdWithFullName(fund['fund'])
        #     response = requests.post(baseurl + 'org/managefund/', data=json.dumps(fund), headers=headers).content
        #     response = json.loads(response)
        #     if response['code'] != 1000:
        #         print '新增失败--%s' % fund['fund'] + str(response)




        # cooprelation = []
        # if linedic['合作关系']['start'] > 0 and linedic['合作关系']['end'] > linedic['合作关系']['start']:
        #     for i in range(linedic['合作关系']['start'], linedic['合作关系']['end'] + 1):
        #         relation = {
        #             'cooperativeOrg': aaa[i]['col0'],
        #             'investDate': aaa[i]['col1'] if aaa[i]['col1'] != 'N/A' else None,
        #             'comshortname': aaa[i]['col2'],
        #         }
        #         cooprelation.append(relation)



        # for coop in cooprelation:
        #     coopdic = {
        #         # 'orgfullname': coop['cooperativeOrg'],
        #         'orgnameC': coop['cooperativeOrg'],
        #         # 'orgnameE': coop['cooperativeOrg'],
        #         'orgtype': 1,
        #     }
        #     response = requests.post(baseurl + 'org/', data=json.dumps(coopdic), headers=headers).content
        #     response = json.loads(response)
        #     if response['code'] != 1000:
        #         print '新增失败--%s' % coop['cooperativeOrg'] + str(response)
        #     else:
        #         orgid = response['result']['id']
        #         f = open('org', 'a')
        #         key = str(coop['cooperativeOrg'])
        #         content = '{\'%s\': %s}' % (key, orgid)
        #         f.writelines(content)
        #         f.writelines('\n')
        #         f.close()



        # # 合作机构与机构建立关系
        # for coop in cooprelation:
        #     coop['org'] = orgid
        #     coop['cooperativeOrg'] = getOrgIdWithFullName(coop['cooperativeOrg'])
        #     if coop['investDate']:
        #         datelist = coop['investDate'].split('/')
        #     else:
        #         datelist = []
        #     shornamelist = coop['comshortname'].split('/')
        #     if len(datelist) > 1:
        #         for i in range(0, len(datelist)):
        #             coop['investDate'] = datelist[i] + 'T12:00:00'
        #             coop['comshortname'] = shornamelist[i]
        #
        #             response = requests.post(baseurl + 'org/cooprelation/', data=json.dumps(coop),
        #                                      headers=headers).content
        #             response = json.loads(response)
        #             if response['code'] != 1000:
        #                 print '新增失败--%s' % coop['cooperativeOrg'] + str(response)
        #     else:
        #         coop['investDate'] = coop['investDate'] + 'T12:00:00' if coop['investDate'] else None
        #         response = requests.post(baseurl + 'org/cooprelation/', data=json.dumps(coop), headers=headers).content
        #         response = json.loads(response)
        #         if response['code'] != 1000:
        #             print '新增失败--%s' % coop['cooperativeOrg'] + str(response)


        # contactlist = []
        # if linedic['联系方式']['start'] > 0 and linedic['联系方式']['end'] > linedic['联系方式']['start']:
        #     contactdic = {}
        #     for i in range(linedic['联系方式']['start'],linedic['联系方式']['end'] + 2):
        #         if aaa[i]['col0'] == '地址：':
        #             if aaa[i]['col6'] != 'N/A':
        #                 phone = aaa[i]['col6'].replace('+', '').split('-')
        #                 if len(phone) == 3:
        #                     numbercode = phone[2]
        #                     countrycode = phone[0]
        #                     areacode = phone[1]
        #                 elif len(phone) == 2:
        #                     numbercode = phone[1]
        #                     countrycode = phone[0]
        #                     areacode = None
        #                 else:
        #                     countrycode = None
        #                     areacode = None
        #                     numbercode = phone[0]
        #             else:
        #                 countrycode = None
        #                 areacode = None
        #                 numbercode = None
        #             contactdic.update({'address': aaa[i]['col1'], 'numbercode': numbercode,'countrycode':countrycode,'areacode':areacode })
        #         if aaa[i]['col0'] == '电话':
        #             if aaa[i]['col6'] != 'N/A':
        #                 fax = aaa[i]['col6'].split('-')
        #                 if len(fax) == 3:
        #                     faxcode = fax[2]
        #                 elif len(fax) == 2:
        #                     faxcode = fax[1]
        #                 else:
        #                     faxcode = fax[0]
        #             else:
        #                 faxcode = None
        #             contactdic.update({'postcode': aaa[i]['col1'] if aaa[i]['col1'] != 'N/A' else None, 'faxcode': faxcode})
        #         if aaa[i]['col0'] == '邮编：':
        #             contactdic.update({'email': aaa[i]['col6'] if aaa[i]['col6'] != 'N/A' else None})
        #         if aaa[i]['col0'] == '':
        #             contactlist.append(contactdic)
        #             contactdic = {}
        #
        #
        # if orgid:
        #     for contact in contactlist:
        #         contact['org'] = orgid
        #         response = requests.post(baseurl + 'org/contact/', data=json.dumps(contact), headers=headers).content
        #         response = json.loads(response)
        #         if response['code'] != 1000:
        #             print '新增失败--%s' % orgname + str(response)









        # investevent = []
        # if linedic['投资事件']['start'] > 0 and linedic['投资事件']['end'] > linedic['投资事件']['start']:
        #     for i in range(linedic['投资事件']['start'], linedic['投资事件']['end'] + 1):
        #
        #         event = {
        #             'comshortname': aaa[i]['col0'],
        #             'industrytype': aaa[i]['col1'],
        #             'area': aaa[i]['col2'],
        #             'investor': aaa[i]['col3'],
        #             'investDate': aaa[i]['col4'] + 'T12:00:00' if aaa[i]['col4'] != 'N/A' else None,
        #             'investType': aaa[i]['col5'],
        #             'investSize': unicode(aaa[i]['col6']) + aaa[i]['col7'],
        #         }
        #         fundSize = event['investSize']
        #         if fundSize == 'N/A':
        #             event['investSize'] = None
        #         investevent.append(event)
        #
        #     # print len(investevent)
        #
        # #新建投资事件
        # for event in investevent:
        #     event['org'] = orgid
        #     event['area'] = getAreaIdWithCountryC(event['area'])
        #     response = requests.post(baseurl + 'org/investevent/', data=json.dumps(event), headers=headers).content
        #     response = json.loads(response)
        #     if response['code'] != 1000:
        #         print '新增失败--%s' % event['comshortname'] + str(response)





        buyout = []
        if linedic['退出分析']['start'] > 0 and linedic['退出分析']['end'] > linedic['退出分析']['start']:
            for i in range(linedic['退出分析']['start'], linedic['退出分析']['end'] + 1):
                out = {
                    'comshortname': aaa[i]['col0'],
                    'buyoutDate': aaa[i]['col1'] + 'T12:00:00' if aaa[i]['col1'] != 'N/A' else None,
                    'buyoutorg': aaa[i]['col2'] if aaa[i]['col2'] != 'N/A' else None,
                    'buyoutType': aaa[i]['col3'],
                }
                buyout.append(out)
        # for out in buyout:
        #     if out['buyoutorg']:
        #         funddic = {
        #             # 'orgfullname': fund['fund'],
        #             'orgnameC': out['buyoutorg'],
        #             # 'orgnameE': fund['fund'],
        #             'orgtype': 1,
        #         }
        #         response = requests.post(baseurl + 'org/', data=json.dumps(funddic), headers=headers).content
        #         response = json.loads(response)
        #         if response['code'] != 1000:
        #             print '新增失败--%s' % out['comshortname'] + str(response)
        #         else:
        #             orgid = response['result']['id']
        #             f = open('org', 'a')
        #             key = str(funddic['orgnameC'])
        #             content = '{\'%s\': %s}' % (key, orgid)
        #             f.writelines(content)
        #             f.writelines('\n')
        #             f.close()

        # ## 退出分析与机构建立关系
        # for out in buyout:
        #     out['org'] = orgid
        #     out['buyoutorg'] = getOrgIdWithFullName(out['buyoutorg'])
        #     response = requests.post(baseurl + 'org/buyout/', data=json.dumps(out),
        #                              headers=headers).content
        #     response = json.loads(response)
        #     if response['code'] != 1000:
        #         print '新增失败--%s' % out['comshortname'] + str(response)




#251
# orgnameid = {
#     u'S&PCapitalIQ':1398,
#     u'健合(H&H)国际控股有限公司':11286,
#     u'J.H. Whitney & Co., LLC':12799,
#     u'JK&B Capital':12800,
#     u'Kohlberg Kravis Roberts & Co., L.P.':12802,
#     u'SBI & 北大青鸟中国基金': 14384,
#     u'Asset & Ashe Investment Limited':17728,
#     u'JK&B':18040,
# }

#39


orgnameid = {
    u'S&PCapitalIQ':311,
    u'健合(H&H)国际控股有限公司':12116,
    u'上汽投资&创投':13026,
    u'JK&B': 23602,
    u'SBI & 北大青鸟中国基金':24676,
    u'Asset & Ashe Investment Limited':28025,
    u'淡马锡':5060,
}



def getAreaIdWithCountryC(countryC):
    countryId = None
    if countryC and countryC != 'N/A':
        if '/' in countryC:
            countryC =  countryC.split('/')[0]
        if u'中国' in countryC and len(countryC) > len(u'中国'):
            countryC = countryC.replace(u'中国', '')
        countrylist = json.loads(requests.get(baseurl + 'source/country?countryC=%s' % countryC, headers=headers).content)
        countrylist = countrylist.get('result', [])
        if len(countrylist) > 0:
            if len(countrylist) > 1:
                print '匹配到%s个地区--%s'% (len(countrylist), str(countrylist))
            countryId = countrylist[0]['id']
        else:
            print '未匹配到地区--%s' % countryC
    else:
        print '地区名为空'
    return countryId


def getTitleIdWithTitleC(titleC):
    titleId = None
    if titleC and titleC != 'N/A':
        if '/' in titleC:
            titleC =  titleC.split('/')[0]
        if u'区总裁' in titleC:
            titleC = u'总裁'
        countrylist = json.loads(requests.get(baseurl + 'source/title?search=%s' % titleC, headers=headers).content)
        countrylist = countrylist.get('result', [])
        if len(countrylist) > 0:
            if len(countrylist) > 1:
                print '匹配到%s个职位--%s'% (len(countrylist), titleC)
            titleId = countrylist[0]['id']
        else:
            print '未匹配到职位--%s' % titleC
    else:
        print '职位为空'
    if not titleId:
        titleId = 8
    return titleId



def getOrgIdWithFullName(orgname):
    if orgname:
        if orgname == ' 成都博源兴邦投资合伙企业':
            orgname = '成都博源兴邦投资合伙企业'
        orgid = orgnameid.get(orgname, None)
        if orgid:
            return orgid
        # if orgname and orgname != 'N/A':
        #     orglist = json.loads(requests.get(baseurl + 'org/?orgname=%s' % orgname, headers=headers).content).get(
        #         'result', {}).get('data', [])
        #     if len(orglist) > 0:
        #         orgid = orglist[0]['id']
        #     else:
        #         print '未匹配到相应机构--%s' % orgname
        if not orgid:
            if orgname and orgname != 'N/A':
                orglist = json.loads(requests.get(baseurl + 'org/?orgfullname=%s' % orgname, headers=headers).content).get(
                    'result', {}).get('data', [])
                if len(orglist) > 0:
                    orgid = orglist[0]['id']
                else:
                    print '全称未匹配到机构--%s' % orgname
    else:
        print '机构名称为空'
        return None
    return orgid



def getUserId(username, orgid):
    userid = None
    if username and username != 'N/A' and orgid:
        orglist = json.loads(requests.get(baseurl + 'user/?usernameC=%s&org=%s' % (username, orgid), headers=headers).content).get(
            'result', {}).get('data', [])
        if len(orglist) > 0:
            userid = orglist[0]['id']
        else:
            print '未匹配到相应用户--%s' % username
    return userid

def test():
    orgid = getOrgIdWithFullName('亚洲搭档')
    print orgid
# 亚洲搭档/狮享家/ 成都博源兴邦投资合伙企业

if __name__=="__main__":
    main()




