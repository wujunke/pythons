#coding=utf-8
import json

import pymysql
import requests
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
    addPublicDataroom()



def addPublicDataroom():
    times = 0
    datamanager = DataManager()
    for row in datamanager.allDataroom:
        times = times + 1
        proj = datamanager.getNewProjId(row['ProjectId'])
        createuser = datamanager.getNewUserId(row['CreatorUserId'])
        dic = {
                'proj':proj,
                'createuser': createuser if createuser else 1,
                'createdtime':str(row['CreationTime']),
            }
        try:
            response = requests.post(baseurl + 'dataroom/add/', data=json.dumps(dic), headers=headers).content
            response = json.loads(response)
            if response['code'] not in [1000]:
                print '新增失败' + str(response)
                print row['Id']
            else:
                f = open('dataroom-old_new_id', 'a')
                f.writelines(json.dumps({'old': row['Id'], 'new': response['result']['id'], 'UserType': row['UserType'],
                                         'isPublic': row['IsPublic']}))
                f.writelines('\n')
                f.close()
        except Exception as err:
            print 'shibai'
            print  err
            print row['Id']
        else:
            pass
    print times

class DataManager():
    def __init__(self):
        self.allMySqlUser = self.getAllMySqlUser()
        self.allMySqlProj = self.getAllMySqlProj()

        self.allDataroom = self.getAllDataroom()

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




    def getAllMySqlProj(self):
        res = []
        file = open('proj-old_new_id')
        for line in file:
            if len(line) > 10:
                res.append(json.loads(line.replace('\n', '')))
        return res

    def getNewProjId(self,oldid):
        if oldid:
            for dic in self.allMySqlProj:
                if dic['old'] == oldid:
                    return dic['new']
            return None
        else:
            return None



    def getAllDataroom(self):
        conn = _mssql.connect(server='101.201.47.50', user='sa', password='Investarget@2016', )
        # SELECT 短链接查询操作（一次查询将所有数据取出）
        sql = "SELECT * FROM InvestargetDb_v2.dbo.ProjectDataRoom WHERE IsDeleted = 0 AND IsPublic = 1"
        conn.execute_query(sql)
        res = []
        for area in conn:
            res.append(area)
        conn.close()
        return res





if __name__=="__main__":
    main()



# createtime = statudata.pop('createdtime').encode('utf-8')[0:19]
                        # if createtime not in ['None',None,u'None','none']:
                            # statudata['createdtime'] = datetime.datetime.strptime(createtime, "%Y-%m-%d %H:%M:%S")