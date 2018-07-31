#coding=utf-8
import json
import xlwt

# 机构全称、标签、描述、投资事件（简介、网址、联系方式以及历史融资情况）、合伙人/投委会成员
def saveToFile(org_qs):
    wb = xlwt.Workbook(encoding='utf-8')
    style = xlwt.XFStyle()  # 初始化样式
    alignment = xlwt.Formatting.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 垂直对齐
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 水平对齐
    alignment.wrap = xlwt.Alignment.WRAP_AT_RIGHT  # 自动换行
    style.alignment = alignment
    ws_org = wb.add_sheet('机构列表')
    ws_org.write(0, 0, '机构全称')
    ws_org.write(0, 1, '描述')
    ws_org.write(0, 2, '合伙人/投委会成员')
    ws_org.write(0, 3, '标签')
    ws_org.write(0, 4, '投资事件')

    ws_org_hang = 1
    for org in org_qs:
        tags = org.tags
        tagnamelist = []
        for tag in tags:
            tagnamelist.append(tag.nameC)
        tagstr = '、'.join(tagnamelist)
        investevents = org.org_orgInvestEvent.all().filter(is_deleted=False)
        # event_list = []
        # for event in investevents:
        #     event_list.append('项目名称：%s, 行业：%s , 投资日期：%s , 投资轮次：%s, 投资金额：%s' % (event.comshortname, event.industrytype , event.investDate, event.investType, event.investSize))
        # eventstr = '；'.join(event_list)
        ws_org.write(ws_org_hang, 0, str(org.orgfullname))        #全称
        ws_org.write(ws_org_hang, 1, str(org.description))    #描述
        ws_org.write(ws_org_hang, 2, str(org.partnerOrInvestmentCommiterMember))    #合伙人/投委会
        ws_org.write(ws_org_hang, 3, tagstr)    #标签
        # ws_org.write(ws_org_hang, lie + 4, eventstr, style)    #投资事件

        com_list = ProjectData.objects.filter(com_id__in=investevents.value_list('com_id'))

        ws_com_hang = 1
        for com in com_list:
            com_sheet = wb.add_sheet(org.orgfullname)
            com_sheet.write(0, 0, '机构全称')
            com_sheet.write(0, 1, '描述')
            com_sheet.write(0, 2, '合伙人/投委会成员')
            com_sheet.write(0, 3, '标签')
            com_sheet.write(0, 4, '投资事件')
            com_sheet.write(ws_com_hang, 0, str(com.com_name))  # 全称
            com_sheet.write(ws_com_hang, 1, str(com.com_des))  # 简介
            com_sheet.write(ws_com_hang, 2, str(com.com_web))  # 网址
            com_sheet.write(ws_com_hang, 3, str(com.mobile))  # 电话
            com_sheet.write(ws_com_hang, 4, str(com.email))  # 邮箱
            com_sheet.write(ws_com_hang, 5, str(com.com_addr))  # 地址
            com_sheet.write(ws_com_hang, 6, str(com.com_name))  # 融资历史
            ws_com_hang += 1
        ws_org_hang += 1
    wb.save('test.xls')



