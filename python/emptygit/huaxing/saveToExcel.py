#coding=utf-8
import xlwt
from huaxing.huaxing_url import readFileLines


orgs = readFileLines('orglist')
events = readFileLines('events')


def getINST_NM(INST_ID):
    for org in orgs:
        if org['INST_ID'] == INST_ID:
            return org['INST_NM']
    return None


def saveToFile(data_qs):
    wb = xlwt.Workbook(encoding='utf-8')
    ws_org = wb.add_sheet('机构列表')
    event1 = data_qs[0]
    keylist = event1.keys()

    ws_org.write(0, 0, u'INST_NM')
    j = 1
    for key in keylist:
        ws_org.write(0, j, key)  # 全称
        j += 1

    ws_org_hang = 1
    for data in data_qs:
        INST_NM = getINST_NM(data['INST_ID'])
        ws_org.write(ws_org_hang, 0, INST_NM)  #机构名称
        j = 1
        for key in keylist:
            ws_org.write(ws_org_hang, j, data[key])
            j += 1
        ws_org_hang += 1
    wb.save('org_event.xls')


saveToFile(events)
