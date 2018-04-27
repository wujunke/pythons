#coding=utf-8
import _mssql
import json

import sys

import sys

import requests

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)



import xlwt, xlrd


def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print str(e)
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的索引  ，by_index：表的索引
def excel_table_byindex(file,colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    colnames =  table.row_values(colnameindex) #某一行数据
    list =[]
    for rownum in range(1,nrows):
         row = table.row_values(rownum)
         if row:
             app = {}
             for i in range(len(colnames)):
                app[colnames[i]] = row[i]
             list.append(app)
    return list




def saveToFile(res):
    # style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('users')
    hang = 0
    ws.write(hang, 0, '姓名')
    ws.write(hang, 1, '机构名称')
    ws.write(hang, 2, '部门')
    ws.write(hang, 3, '职位')
    ws.write(hang, 4, '标签')
    ws.write(hang, 5, '手机')
    ws.write(hang, 6, '微信')
    ws.write(hang, 7, '邮箱')
    ws.write(hang, 8, '交易师')

    hang = hang + 1
    for row in res:
        lie = 0
        orgname = row['org']['orgnameC']
        title = row['title']['nameC'] if row['title'] else '暂无'
        tags = '/'.join(tag['nameC'] for tag in row['tags']) if row['tags'] else '暂无'
        trader = row['trader_relation']['traderuser']['usernameC'] if row['trader_relation'] else '暂无'
        ws.write(hang, lie + 0, str(row['usernameC']))
        ws.write(hang, lie + 1, orgname)
        ws.write(hang, lie + 2, str(row['department']) if row['department'] else '暂无')
        ws.write(hang, lie + 3, title)
        ws.write(hang, lie + 4, tags)
        ws.write(hang, lie + 5, str(row['mobile']) if row['mobile'] else '暂无')
        ws.write(hang, lie + 6, str(row['wechat']) if row['wechat'] else '暂无')
        ws.write(hang, lie + 7, str(row['email']) if row['email'] else '暂无')
        ws.write(hang, lie + 8, trader)



        # f = open('user-1.txt', 'a')
        # f.writelines(str(row[1])+';'+str(row[2])+';'+str(row[3])+';'+str(row[4])+';'+str(row[5])+';'+str(row[6])+';'+tags+';'+remarks)
        # f.writelines('\n')
        # f.close()
        hang = hang + 1
    wb.save('users.xls')



# token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'
# baseurl = 'http://192.168.1.201:8000/'

token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
baseurl = 'https://api.investarget.com/'

headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }


def getOrg(stockcode):
    orgid = None
    if not orgid:
        if stockcode and stockcode != '':
            orglist = json.loads(requests.get(baseurl + 'org/?stockcode=%s' % stockcode, headers=headers).content).get(
                'result', {}).get('data', [])
            if len(orglist) > 0:
                orgid = orglist[0]['id']
            else:
                print '代码-未匹配--%s' % stockcode
    return orgid


def getOrgWithName(name):
    orgidlist = []
    if name and name != '':
            orglist = json.loads(requests.get(baseurl + 'org/?search=%s' % name, headers=headers).content).get(
                'result', {}).get('data', [])
            if len(orglist) > 0:
                for org in orglist:
                    orgidlist.append(org['id'])
            else:
                print '简称-未匹配--%s' % name
    return orgidlist



def getUsersWithOrgid(orgid, page_index=None, users=None):
    if not users:
        users = []
    if not page_index:
        page_index = 1
    if orgid:
        userlist = json.loads(requests.get(baseurl + 'user/?org=%s&page_index=%s' % (orgid, page_index), headers=headers).content).get(
            'result', {}).get('data', [])
        if len(userlist) > 0:
            users = users + userlist
        if len(userlist) == 10:
            page_index += 1
            users = getUsersWithOrgid(orgid, page_index, users)
    return users


tables = excel_table_byindex('/Users/investarget/Desktop/201803.xlsx')

userslist = []
for row in tables:
    # stockcode = row[u'证券代码']
    orgname = row[u'证券简称']
    # orgid = getOrg(stockcode)
    # if orgid:
    #     users = getUsersWithOrgid(orgid)
    #     userslist = userslist + users
    #
    # else:
    orgidlist = getOrgWithName(orgname)
    for orgid in orgidlist:
        users = getUsersWithOrgid(orgid)
        userslist = userslist + users

saveToFile(userslist)