# coding: utf-8


import datetime
import pymongo
from pymongo import WriteConcern

from wxbot import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

client = pymongo.MongoClient('mongodb://192.168.1.251:27017/')
db = client.wxnlp
WXCollection = db.wxchatdata


class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        pass

    def schedule(self):
        rootdir = '/Users/investarget/Desktop/django_server/pdffile/'
        filelist = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        print len(filelist)
        for i in range(0, 1):
            filepath = os.path.join(rootdir, filelist[i])
            # print filepath


            if os.path.isfile(filepath):
                # for group in self.group_list:
                #     groupname = group['UserName']
                groupnames = [u'别墅1']
                for groupname in groupnames:

                    if self.send_file_msg_by_uid(filepath, self.get_user_id(groupname)):
                        print '发送成功'
                    else:
                        print '发送失败'
                    time.sleep(60)
                os.remove(filepath)

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.run()

if __name__ == '__main__':
    main()
