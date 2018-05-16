#coding=utf-8

# it桔子Cookie（抓取使用）
Cookie = 'acw_tc=AQAAAEhOBzyv+AcAAtNyDWYgyOV9JZ/e; _ga=GA1.2.1047965745.1526279819; _gid=GA1.2.1794278510.1526279819; _gat=1; gr_user_id=51551c4e-2ea3-4827-8021-6aae9bde09b7; Hm_lvt_1c587ad486cdb6b962e94fc2002edf89=1524217343,1524894738,1526018743,1526279820; Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89=1526279820; gr_session_id_eee5a46c52000d401f969f4535bdaa78=f562ee5e-f02c-474d-a7eb-69539cb84e98_true; MEIQIA_EXTRA_TRACK_ID=0zsxMGF1VQND1EHLYrVanekuTyE; acw_sc__=5af92e9ae416a515caeb9f3d82f1e0b72e77ebe5; identity=18616837957%40test.com; remember_code=9h4GEi6JJp; unique_token=439977; paidtype=vip; session=b5c22110317a87bb81d164313d0734dfc9f79c55'
# api的token（插入使用）
# token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'
# 39服务器
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'

# 插入数据地址
# base_url = 'http://192.168.1.201:8000/'
# base_url = 'http://192.168.1.251:8080/'
base_url = 'https://api.investarget.com/'

# 接口限速//每隔X秒读取一页内容并插入（抓取一条请求/插入15条请求）
insert_rate = 0

# 隔X秒开始更新一次
find_rate = 36000  #10分钟

page_size = 15  #这是it桔子的页面大小，不要改动，判断是否重复爬取页面数据的依据

# http:
iplist = ['140.205.222.3:80']
# https:'123.152.36.89:2682','123.152.66.19:2682', '123.152.36.149:2682'，'123.152.37.213:2682','123.152.67.108:2682','123.152.37.124:2682','58.243.30.186:4676'
iplist2 = ['114.215.95.188:3128']


temp_path_base = '/Users/investarget/Desktop/python/emptygit/data3/'

judgerepeat = False


# 修改string类型 -> int类型
'''
字段类型编号:
1 Double 浮点型
2 String UTF-8字符串都可表示为字符串类型的数据
3 Object 对象，嵌套另外的文档
4 Array 值的集合或者列表可以表示成数组
5 Binary data 二进制
7 Object id 对象id是文档的12字节的唯一 ID 系统默认会自动生成
8 Boolean 布尔类型有两个值TRUE和FALSE
9 Date 日期类型存储的是从标准纪元开始的毫秒数。不存储时区
10 Null 用于表示空值或者不存在的字段
11 Regular expression 采用js 的正则表达式语法
13 JavaScript code 可以存放Javasript 代码
14 Symbol 符号
15 JavaScript code with scope
16 32-bit integer 32位整数类型
17 Timestamp 特殊语义的时间戳数据类型
18 64-bit integer 64位整数类型
'''
# db.projdata.find({'com_id' : { $type : 2 }}).forEach(function(x) {x.com_id = NumberInt(x.com_id);db.projdata.save(x); })
# db.mergeandfinanceevent.find({'com_id' : { $type : 2 }}).forEach(function(x) {x.com_id = NumberInt(x.com_id);db.mergeandfinanceevent.save(x); })
# db.mergeandfinanceevent.find({'invse_id' : { $type : 2 }}).forEach(function(x) {x.invse_id = NumberInt(x.invse_id);db.mergeandfinanceevent.save(x); })
# db.mergeandfinanceevent.find({'merger_id' : { $type : 2 }}).forEach(function(x) {x.merger_id = NumberInt(x.merger_id);db.mergeandfinanceevent.save(x); })
# 删除数据
# db.mergeandfinanceevent.remove({_id:{$gt:ObjectId("59f2a662cfb83f609e3eb993")}})

# db.projdata.aggregate([
#  { $group: {
#  _id: { com_id:"$com_id"},
#  uniqueIds: { $addToSet:"$_id" },
#  count: { $sum: 1 }
#  } },
#  { $match: {
#  count: { $gte: 2 }
#  } },
# { $sort : { count : -1} },
# ]);
#
# while ( rs.hasNext() ) {
#     var r = rs.next().count;
#     var k = rs.next().uniqueIds;
#     for (var ii=0;ii<r-1;ii++){
#         db.projdata.remove({"_id":k[ii]},true)
#     }
# }
