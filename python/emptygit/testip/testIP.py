#coding=utf-8
import traceback
import  xdrlib ,sys
from bs4 import BeautifulSoup
import requests
import xlrd
import json

reload(sys)
sys.setdefaultencoding('utf-8')



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

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_name：Sheet1名称
def excel_table_byname(file,colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数
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


def getIPs():
    ips = []
    tables = excel_table_byindex('http.xls')
    for row in tables:
        ip = row[u'IP地址']+ u':' + row[u'端口']
        ips.append(ip)
    return ips


def testIP(ip):
    url = 'https://www.itjuzi.com/user/login'
    header = \
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
        }
    pox = {'https':'https://%s' % str(ip)}
    try:
        res = requests.get(url, headers=header, proxies=pox, timeout=3).content
        soup = BeautifulSoup(res, 'html.parser')
    except Exception:
        print traceback.format_exc()
    else:
        title = soup.title
        if title:
            title = title.text
        if title in ['用户登录 | IT桔子', u'用户登录 | IT桔子']:
            print 'ip-  %s  -可用' % str(ip)
        else:
            print 'ip-  %s  -不可用' % str(ip)




if __name__ == "__main__":
    ips = getIPs()

    for ip in ips:
        testIP(ip)

