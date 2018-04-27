#coding=utf-8
import json
import threading
import traceback

import requests
import time

from datetime import datetime

from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

Cookie = 'gr_user_id=476e6075-f262-4a3f-bb7d-bc50dd84bf6c; identity=18616837957%40test.com; remember_code=dgoYE5vTDL; unique_token=439977; pgv_pvi=4490570752; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1508918529,1508984104,1509083253,1509530406; acw_tc=AQAAAMuSLAP6mQoARonnZRwApV4o8Nxi; pgv_si=s9887466496; _ga=GA1.2.1158154884.1509083652; _gid=GA1.2.949417547.1509530406; Hm_lvt_80ec13defd46fe15d2c2dcf90450d14b=1508918544,1508984112,1509530423,1509589946; Hm_lpvt_80ec13defd46fe15d2c2dcf90450d14b=1509604171; session=8049c796682574c82e27657c5fd76c94317aead7; user-radar.itjuzi.com=%7B%22n%22%3A%22%5Cu6854%5Cu53cb9ef285e61d740%22%2C%22v%22%3A3%7D; gr_session_id_eee5a46c52000d401f969f4535bdaa78=e4acd0ad-6365-4f49-86d2-555c21be7a56; gr_cs1_e4acd0ad-6365-4f49-86d2-555c21be7a56=user_id%3A439977'

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
}

url_company_detail = 'http://radar.itjuzi.com/company/'
def getCompanyDetail(com_id):
    try:
        html = requests.get(url_company_detail + '%s'%com_id,headers=headers,proxies=proxie).content
        # print html
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        com_name = str(soup.title.text).replace(' | 桔子雷达', '')
        return com_name
    except Exception:
        return com_name

def updateComName(userid,new):
    if new:
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )

        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "UPDATE InvestargetDb_v2.dbo.\"User\" SET WeChat = \'%s\' WHERE Id = %s"%(new,userid)
        # sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND id = 1155"
        conn.execute_query(sql)
        conn.close()
