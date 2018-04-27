#coding=utf-8
#it桔子Cookie（抓取使用）
Cookie = 'gr_user_id=3e9524a2-4693-416b-8c3c-dc8432051a65; MEIQIA_EXTRA_TRACK_ID=0vqN2YLRaP4z6UN9O4TzPsgXpYC; pgv_pvi=1923164160; identity=18616837957%40test.com; unique_token=439977; _ga=GA1.2.713347647.1509688885; _gid=GA1.2.2025274775.1513246201; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1512967844,1513055558,1513246202,1513303755; acw_tc=AQAAAEIll1evHQsARonnZYSZWKIuYnmE; Hm_lvt_80ec13defd46fe15d2c2dcf90450d14b=1512967849,1513055562,1513246203,1513303757; remember_code=s2Wi5%2FW0ny; user-radar.itjuzi.com=%7B%22n%22%3A%22%5Cu6854%5Cu53cb9ef285e61d740%22%2C%22v%22%3A3%7D; _gat=1; gr_session_id_eee5a46c52000d401f969f4535bdaa78=0c87a103-29fd-4e76-b23c-6ae2f48e3c56; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1513333561; session=4643664e9ff73a0386168ad965b95faf3be9242d; gr_cs1_0c87a103-29fd-4e76-b23c-6ae2f48e3c56=user_id%3A439977; Hm_lpvt_80ec13defd46fe15d2c2dcf90450d14b=1513333563'

#api的token（插入使用）
token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'

#data暂存路径
temp_path_base = ''

#插入数据地址
#base_url = 'http://192.168.1.201:8000/'
base_url = 'http://192.168.1.251:8080/'
#接口限速//每隔X秒读取一页内容并插入（抓取一条请求/插入15条请求）
insert_rate = 0
#隔X秒开始更新一次
find_rate = 3600

page_size = 15 #这是it桔子的页面大小，不要改动，判断是否重复爬取页面数据的依据

#代理ip
iplist=['61.155.164.112:3128','122.72.18.60:80']
iplist2 =['121.13.165.107:9797']


judgerepeat = True
