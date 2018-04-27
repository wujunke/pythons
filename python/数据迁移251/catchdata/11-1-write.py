#coding=utf-8
import _mssql

import datetime

import readFromExcel
from datacomparsion2.util import checkMobileExist, checkEmailExist


def updateUserEmail(userid,new):
    if new:
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )

        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "UPDATE InvestargetDb_v2.dbo.\"User\" SET EmailAddress = \'%s\' WHERE Id = %s"%(new,userid)
        # sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND id = 1155"
        conn.execute_query(sql)
        conn.close()

def updateUserMobile(userid,new):
    if new:
        if not isinstance(new,(str,unicode)):
            new = str(int(new))
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )

        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "UPDATE InvestargetDb_v2.dbo.\"User\" SET Mobile = \'%s\' WHERE Id = %s"%(new,userid)
        # sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND id = 1155"
        conn.execute_query(sql)
        conn.close()

def updateUserWechat(userid,new):
    if new:
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )

        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "UPDATE InvestargetDb_v2.dbo.\"User\" SET WeChat = \'%s\' WHERE Id = %s"%(new,userid)
        # sql = "SELECT * FROM InvestargetDb_v2.dbo.Organization WHERE IsDeleted = 0 AND id = 1155"
        conn.execute_query(sql)
        conn.close()

def insertUserRemark(userid,new):
    if new:
        if len(new) > 1:
            conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
            # SELECT 短链接查询操作（一次查询将所有数据取出）
            sql = "INSERT INTO InvestargetDb_v2.dbo.UserRemarks (Remark,UserId,IsDeleted,CreationTime) VALUES (\'%s\',%s,0 , getdate())"%(new,userid)
            conn.execute_query(sql)
            conn.close()


times = 0
tables = readFromExcel.excel_table_byindex('/Users/investarget/Desktop/11-1.xlsx')





for row in tables:
    times = times + 1
    if row['ID'] > 0:
        mobile = row['mobile']
        wxchat = None
        if isinstance(mobile,unicode):
            if '微信' in mobile:
                wxchat = str(mobile).replace('微信：','')
                mobile = None
                # print wxchat
        userlist1 = checkMobileExist(mobile)
        userlist2 = checkEmailExist(row['email'])
        if len(userlist1) > 0 and len(userlist2) > 0:
            pass
            # if userlist1[0]['Id'] == userlist2[0]['Id']:
            #     insertUserRemark(userlist1[0]['Id'], row['remark'])
        elif len(userlist1) > 0 and len(userlist2) == 0:
            pass
            # updateUserEmail(userlist1[0]['Id'],row['email'])
            # insertUserRemark(userlist1[0]['Id'],row['remark'])
        elif len(userlist1) == 0 and len(userlist2) > 0:
            pass
            # updateUserMobile(userlist2[0]['Id'],row['mobile'])
            # insertUserRemark(userlist2[0]['Id'], row['remark'])
            # updateUserWechat(userlist2[0]['Id'], wxchat)
        else:
            continue
        print row['ID']