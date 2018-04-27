#coding=utf-8
import json
import traceback

import pymysql
import requests
from pypinyin import slug as hanzizhuanpinpin
import _mssql

#海拓token
token = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecf'
#车创token
token2 = '0011b9120f76196890f1bb33326128ef125a95d359dc2ecg'
baseurl = 'http://39.107.14.53:8080/'


headers = {
        'token':token,
        'source':'1',
        'Content-Type':'application/json',
        'Accept':'application/json',
    }

def main():
    addFile()



def addDirectory():
    times = 0

    datamanager = DataManager()

    for row in datamanager.allDirectory:
        times = times + 1
        parent = None
        try:
            userid = datamanager.getNewUserId(row['CreatorUserId'])
            dataroomid = datamanager.getNewDataroomId(row['DataRoomId'])
            if row['ParentId'] == 0:
                pass
            else:
                parentIsDelete = datamanager.checkParentDirectoryisDelete(row['ParentId'])
                if parentIsDelete:
                    print row['Id']
                    print 'isdelete'
                    continue
                else:
                    parent = datamanager.getNewDirectoryId(row['ParentId']),
                    if isinstance(parent,(tuple,list)):
                        if len(parent) > 0:
                            parent = parent[0]
            print row['Id']
            if dataroomid:
                dic = {
                    'dataroom': dataroomid,
                    'parent': parent,
                    'orderNO': row['OrderNo'],
                    'size': None,
                    'filename': row['Name'],
                    'key': None,
                    'bucket': 'file',
                    'isFile': False,
                }
                response = requests.post(baseurl + 'dataroom/file/', data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] != 1000:
                    print '新增失败' + str(response)
                    print str(row['Id'])+ '*****' + str(times)
                    print '====='
                else:
                    datamanager.allMySqlDirectory.append({'old': row['Id'], 'new': response['result']['id']})
                    f = open('dataroomdirectory-old_new_id', 'a')
                    f.writelines(json.dumps({'old': row['Id'], 'new': response['result']['id']}))
                    f.writelines('\n')
                    f.close()
            else:
                print '未找到匹配dataroom'  +  '***' + str(row['Id'])
                print dataroomid
                print '*****'
        except Exception:
            print '失败'  + str(row['Id'])
            print traceback.format_exc()
            print '-----'



def addFile():
    times = 0

    datamanager = DataManager()

    for row in datamanager.allFile:
        times = times + 1
        try:
            userid = datamanager.getNewUserId(row['CreatorUserId'])
            dataroomid = datamanager.getNewDataroomId(row['DataRoomId'])
            if dataroomid:
                dic = {
                    'dataroom': dataroomid,
                    'parent': datamanager.fileGetNewMySqlDirectoryId(row['DirectoryId']),
                    'orderNO': 1,
                    'size': row['Size'],
                    'filename': row['FileName'] if row['FileName'] else row['Key'],
                    'key': row['Key'],
                    'bucket': 'file',
                    'isFile': True,
                }
                response = requests.post(baseurl + 'dataroom/file/', data=json.dumps(dic), headers=headers).content
                response = json.loads(response)
                if response['code'] != 1000:
                    print '新增失败' + str(response)
                    print str(row['Id'])+ '*****' + str(times)
                    print '====='
                else:
                    f = open('dataroomfile-old_new_id', 'a')
                    f.writelines(json.dumps({'old': row['Id'], 'new': response['result']['id']}))
                    f.writelines('\n')
                    f.close()
            else:
                print '未找到匹配dataroom'  +  '***' + str(row['Id'])
                print dataroomid
                print '*****'
        except Exception:
            print '失败'  + str(row['Id'])
            print traceback.format_exc()
            print '-----'




class DataManager():
    def __init__(self):
        self.allDataroom = self.getAllDataroom()
        self.allDirectory = self.getAllDirectory()
        self.allMySqlDirectory = []

        self.allDirectory_MySqlDirectory = self.getAllDirectory_MySqlDirectory()
        self.allFile = self.getAllFile()

        self.allMySqlUser = self.getAllMySqlUser()


    def getAllMySqlUser(self):
        res = []
        file = open('user-old_new_id')
        for line in file:
            if len(line) > 10:
                res.append(json.loads(line.replace('\n', '')))
        return res

    def getNewUserId(self,oldid):
        if oldid:
            for dic in self.allMySqlUser:
                if dic['old'] == oldid:
                    return dic['new']
            return None
        else:
            return None




    def getAllDataroom(self):
        res = []
        file = open('dataroom-old_new_id')
        for line in file:
            if len(line) > 10:
                res.append(json.loads(line.replace('\n','')))
        return res

    def getNewDataroomId(self,sqlserverid):
        if sqlserverid:
            mysqlid = None
            for area in self.allDataroom:
                if area['old'] == sqlserverid:
                    mysqlid = area['new']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None

    def getAllDirectory(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT InvestargetDb_v2.dbo.ProjectDataRoomDirectory.* FROM InvestargetDb_v2.dbo.ProjectDataRoomDirectory INNER JOIN InvestargetDb_v2.dbo.ProjectDataRoom ON ProjectDataRoomDirectory.DataRoomId = ProjectDataRoom.Id WHERE  ProjectDataRoom.IsDeleted = 0 AND ProjectDataRoomDirectory.IsDeleted = 0 AND ProjectDataRoomDirectory.isShadowFolder = 0 AND ProjectDataRoomDirectory.Id >= 3728"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res


    def checkParentDirectoryisDelete(self,parentid):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = 'SELECT InvestargetDb_v2.dbo.ProjectDataRoomDirectory.* FROM InvestargetDb_v2.dbo.ProjectDataRoomDirectory WHERE Id = %s'%parentid
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        if res[0]['IsDeleted'] == 1:
            return True
        elif res[0]['ParentId'] != 0:
            return self.checkParentDirectoryisDelete(res[0]['ParentId'])
        else:
            return False


    def getNewDirectoryId(self,sqlserverid):
        if sqlserverid:
            mysqlid = None
            for area in self.allMySqlDirectory:
                if area['old'] == sqlserverid:
                    mysqlid = area['new']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None


    def getAllFile(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT InvestargetDb_v2.dbo.ProjectDataRoomAttachment.*,InvestargetDb_v2.dbo.ProjectDataRoomDirectory.DataRoomId FROM InvestargetDb_v2.dbo.ProjectDataRoomAttachment INNER JOIN InvestargetDb_v2.dbo.ProjectDataRoomDirectory ON InvestargetDb_v2.dbo.ProjectDataRoomAttachment.DirectoryId = InvestargetDb_v2.dbo.ProjectDataRoomDirectory.Id INNER JOIN InvestargetDb_v2.dbo.ProjectDataRoom ON ProjectDataRoom.Id  = ProjectDataRoomDirectory.DataRoomId WHERE ProjectDataRoomAttachment.IsDeleted = 0 AND ProjectDataRoomDirectory.IsDeleted=0 AND ProjectDataRoom.IsDeleted =0"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res

    def getAllDirectory_MySqlDirectory(self):
        res = []
        file = open('dataroomdirectory-old_new_id')
        for line in file:
            if len(line) > 10:
                res.append(json.loads(line.replace('\n', '')))
        return res

    def fileGetNewMySqlDirectoryId(self,sqlserverid):
        if sqlserverid:
            mysqlid = None
            for area in self.allDirectory_MySqlDirectory:
                if area['old'] == sqlserverid:
                    mysqlid = area['new']
            if mysqlid is not None:
                return mysqlid
            else:
                return None
        else:
            return None
if __name__=="__main__":
    main()
