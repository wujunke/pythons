#coding=utf-8
import _mssql

import sys

reload(sys)
sys.setdefaultencoding('utf-8')



import xlwt






def getAllCountry():
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT [User].Id,[User].Name,Organization.Name,Title.TitleC, [User].Mobile,[User].EmailAddress,[User].PartnerName FROM InvestargetDb_v2.dbo.[User]INNER JOIN InvestargetDb_v2.dbo.Organization ON [User].OrganizationId = Organization.Id INNER JOIN InvestargetDb_v2.dbo.Title ON [User].TitleId = Title.Id WHERE [User].OrganizationId IS NOT NULL AND [User].IsDeleted = 0 AND [User].Id IN (SELECT UserCommonTransaction.UserId FROM InvestargetDb_v2.dbo.UserCommonTransaction WHERE [UserCommonTransaction].IsDeleted = 0)"
    conn.execute_query(sql)
    res = []
    for area in conn:
        res.append(area)
    conn.close()
    return res

def saveToFile(res):
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('A Test Sheet')


    hang = 0
    for row in res:
        lie = 0

        tags = getUserTag(row[0])
        remarks = getUserRemark(row[0])
        ws.write(hang, lie, str(row[1]))
        ws.write(hang, lie + 1, str(row[2]))
        ws.write(hang, lie + 2, str(row[3]))
        ws.write(hang, lie + 3, str(row[4]))
        ws.write(hang, lie + 4, str(row[5]))
        ws.write(hang, lie + 5, str(row[6]))
        ws.write(hang, lie + 6, tags)
        ws.write(hang, lie + 7, remarks)


        # f = open('user-1.txt', 'a')
        # f.writelines(str(row[1])+';'+str(row[2])+';'+str(row[3])+';'+str(row[4])+';'+str(row[5])+';'+str(row[6])+';'+tags+';'+remarks)
        # f.writelines('\n')
        # f.close()
        hang = hang + 1
    wb.save('test.xls')




def getTags():
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT User_Tags.UserId,Tag.TagNameC FROM InvestargetDb_v2.dbo.Tag INNER JOIN InvestargetDb_v2.dbo.User_Tags ON User_Tags.TagId = Tag.Id AND User_Tags.IsDeleted = 0"
    conn.execute_query(sql)
    res = []
    for area in conn:
        res.append(area)
    conn.close()
    return res


def getRemarks():
    conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
    # SELECT 短链接查询操作（一次查询将所有数据取出）
    sql = "SELECT UserId,Remark FROM InvestargetDb_v2.dbo.UserRemarks WHERE UserRemarks.IsDeleted = 0"
    conn.execute_query(sql)
    res = []
    for area in conn:
        res.append(area)
    conn.close()
    return res

allremarks = getRemarks()
allTags = getTags()

def getUserTag(userid):
    res = []
    for remark in allTags:
        if userid == remark[0]:
            res.append(remark[1])
    return '、'.join(res)


def getUserRemark(userid):
    res = []
    for remark in allremarks:
        if int(userid) == int(remark[0]):
            remarka = remark[1].replace('\n', ' ').replace(';', '、')
            res.append(remarka)
    return '*'.join(res)

saveToFile(getAllCountry())

