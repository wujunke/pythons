#coding=utf-8
import json
import re

baseUrl_huaxing = 'http://10.101.11.2:8080/ck/m?xwl='

url_angelVC = baseUrl_huaxing + 'TURBO/CMF_LIST/selectiiba'

url_efectVC = baseUrl_huaxing + 'TURBO/CMF_LIST/selectiivc'

url_newvvVC = baseUrl_huaxing + 'TURBO/CMF_LIST/selectinvc'

url_efectPE = baseUrl_huaxing + 'TURBO/CMF_LIST/selectiipe'

url_indusVC = baseUrl_huaxing + 'TURBO/CMF_LIST/selectiiid'

url_afterVC = baseUrl_huaxing + 'TURBO/CMF_LIST/selectiibs'


url_eventList = 'http://10.101.11.2:8080/ck/m?xwl=TURBO/CMF_INST_BSC_INF/CMF_INST_AWRD_PCP/select'





headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Pragma': 'no-cache',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Host': '10.101.11.2:8080',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Origin': 'http://10.101.11.2:8080',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
    'Referer': 'http://10.101.11.2:8080/ck/home',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=A9C2878A700E27695ABCAE5392C682F1',
    'X-Requested-With': 'XMLHttpRequest'
}

# 替换投资事件列表
def replaceRes(res):
    pattern = re.compile(r'Wb\.numValidator\([0-9]+\,[0-9]+\)')
    res = re.sub(pattern, '1', res)
    res = res.replace('"false"', 'false')
    res = res.replace('"true"', 'true')
    res = res.replace('INST_ID:', '"INST_ID":')
    res = res.replace('SEQ_NUM:', '"SEQ_NUM":')
    res = res.replace('AWRD_ID:', '"AWRD_ID":')
    res = res.replace('AWRD_NM:', '"AWRD_NM":')
    res = res.replace('WTHR_PBLC:', '"WTHR_PBLC":')
    res = res.replace('CEO_NM:', '"CEO_NM":')
    res = res.replace('IDY_DMN:', '"IDY_DMN":')
    res = res.replace('RGON:', '"RGON":')
    res = res.replace('WTHR_LEAD:', '"WTHR_LEAD":')
    res = res.replace('IVS_RND:', '"IVS_RND":')
    res = res.replace('IVS_DT:', '"IVS_DT":')
    res = res.replace('CTB_AMT_W:', '"CTB_AMT_W":')
    res = res.replace('AMOUNT_OF_CONTRIBUTION_UNIT:', '"AMOUNT_OF_CONTRIBUTION_UNIT":')
    res = res.replace('BGN_SHR_RTO:', '"BGN_SHR_RTO":')
    res = res.replace('CRN_MKT_EVL_Y:', '"CRN_MKT_EVL_Y":')
    res = res.replace('CURRENT_VALUATION_UNIT:', '"CURRENT_VALUATION_UNIT":')
    res = res.replace('CRN_SHR_RTO:', '"CRN_SHR_RTO":')
    res = res.replace('IRR_RTO:', '"IRR_RTO":')
    res = res.replace('CASE_CGY:', '"CASE_CGY":')
    res = res.replace('IVS_CASE:', '"IVS_CASE":')
    res = res.replace('MEMO:', '"MEMO":')
    res = res.replace('CTB_CCY:', '"CTB_CCY":')
    res = res.replace('WTHR_QUIT:', '"WTHR_QUIT":')
    res = res.replace('QUIT_DT:', '"QUIT_DT":')
    res = res.replace('QUIT_MODE:', '"QUIT_MODE":')
    res = res.replace('QTUM_RSLT_DESC:', '"QTUM_RSLT_DESC":')
    res = res.replace('RANK_CD:', '"RANK_CD":')
    res = res.replace('YEAR:', '"YEAR":')
    return res


# 替换机构列表
def replaceRes0(res):
    res = res.replace('"false"', 'false')
    res = res.replace('"true"', 'true')
    res = res.replace('INST_ID:', '"INST_ID":')
    res = res.replace('INST_NM:', '"INST_NM":')
    res = res.replace('RNK:', '"RNK":')
    res = res.replace('CNT_NUM:', '"CNT_NUM":')
    res = res.replace('CRN_IVS_CPTL_BLN:', '"CRN_IVS_CPTL_BLN":')
    res = res.replace('MGT_CPTL_TOT_BLN:', '"MGT_CPTL_TOT_BLN":')
    res = res.replace('UNSUBMIT:', '"UNSUBMIT":')
    res = res.replace('YEAR:', '"YEAR":')
    res = res.replace('UP_100MUSD:', '"UP_100MUSD":')
    res = res.replace('PRJ_QTY:', '"PRJ_QTY":')
    res = res.replace('BL3_100MUSD_FLAG:', '"BL3_100MUSD_FLAG":')
    res = res.replace('BL30_PRJ_QTY_FLAG:', '"BL30_PRJ_QTY_FLAG":')
    res = res.replace('BL5_UP_500MUSD_FLAG:', '"BL5_UP_500MUSD_FLAG":')
    res = res.replace('BL50_PRJ_QTY_FLAG:', '"BL50_PRJ_QTY_FLAG":')
    res = res.replace('BL10_PRJ_QTY_FLAG:', '"BL10_PRJ_QTY_FLAG":')
    res = res.replace('BL3_UP_100MUSD_FLAG:', '"BL3_UP_100MUSD_FLAG":')
    res = res.replace('BL5_QUIT_IPO_FLAG:', '"BL5_QUIT_IPO_FLAG":')
    res = res.replace('BL10_PRJ_QTY_FLAG:', '"BL10_PRJ_QTY_FLAG":')
    res = res.replace('BL5_PRJ_QTY_FLAG:', '"BL5_PRJ_QTY_FLAG":')
    res = res.replace('QUIT_IPO:', '"QUIT_IPO":')
    res = res.replace('UP_500MUSD:', '"UP_500MUSD":')
    res = res.replace('UP_100MUSD:', '"UP_100MUSD":')
    res = res.replace('FND_SZ:', '"FND_SZ":')
    # res = res.replace('QUIT_DT:', '"QUIT_DT":')
    # res = res.replace('QUIT_MODE:', '"QUIT_MODE":')
    # res = res.replace('QTUM_RSLT_DESC:', '"QTUM_RSLT_DESC":')
    # res = res.replace('RANK_CD:', '"RANK_CD":')
    # res = res.replace('YEAR:', '"YEAR":')
    return res



def writrFileLines(lines, filename, mode):
    with open(filename, mode) as f:
        for line in lines:
            f.write(json.dumps(line))
            f.write('\n')

def readFileLines(filename):
    returnlist = []
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            returnlist.append(json.loads(line))
    return returnlist