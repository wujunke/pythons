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
base_url = 'http://192.168.1.251/'

class MyWXBot(WXBot):


    def __init__(self):
        self.des_list = []
        super(MyWXBot, self).__init__()



    def handle_msg_all(self, msg):
        """
        处理所有消息，请子类化后覆盖此函数
        msg:
            msg_id  ->  消息id
            msg_type_id  ->  消息类型id
            user  ->  发送消息的账号id
            content  ->  消息内容
        :param msg: 收到的消息
        """
        if msg.get('msg_type_id') == 3:
            # 3 -> 群聊类型消息
            # 2 -> File Helper
            msg_content = msg.get('content')
            fromuser = msg_content.get('user', dict()).get('name', 'unknown_user'),
            content = msg_content.get('data', 'unknown_content')
            if fromuser in [u'特工',]:
                try:
                    if msg_content.get('type') == 0:
                        if u'机构：' in content:
                            if u'姓名：' in content:
                                self.des_list.append({
                                    'username': '',
                                    'orgname': '',
                                    'user_id': '',
                                    'fromuser': fromuser,
                                    'time': int(time.time()),
                                })
                    if msg_content.get('type') == 3:
                        msg_id = msg.get('msg_id')
                        img_path = os.path.join(self.temp_pwd, 'img_' + msg_id + '.jpg')
                        for des_user in self.des_list:
                            if fromuser == des_user['fromuer']:
                                if des_user['time'] < int(time.time()) + 300:
                                    key = self.upload_image(img_path)
                                    self.saveimgtouser(userid=des_user['user_id'], bucket_key=key, bucket='image')
                                else:
                                    self.des_list.remove(des_user)
                                break
                except Exception:
                    pass

            if msg_content.get('type') == 0:
                # 0 -> Text
                # 1 -> Location
                # 3 -> Image
                # 4 -> Voice
                # 5 -> Recommend
                # 6 -> Animation
                # 7 -> Share
                # 8 -> Video
                # 9 -> VideoCall
                # 10 -> Redraw
                # 11 -> Empty
                # 99 -> Unknown
                msg_from = msg.get('user')
                payload = {
                    'name': msg_content.get('user', dict()).get('name', 'unknown_user'),
                    'content': content,
                    'group_name': msg_from.get('name', 'unknown_group'),
                    'createtime': datetime.datetime.now(),
                    'isShow': False,
                }
                WXCollection.insert(payload)

    def upload_image(self, img_path):
        url = base_url + 'service/qiniubigupload?topdf=0&bucket=image'
        files = {'images': open(img_path, 'rb')}
        headers = {
            'token':'',
        }
        r = requests.post(url, files=files, headers=headers).content
        key = json.loads(r).get('result',dict()).get('key', None)
        return key

    def saveimgtouser(self, userid, bucket_key, bucket):
        url = base_url
        headers = {
            'token': '',
        }
        data = {
            'user': userid,
            'bucket': bucket,
            'key': bucket_key,
            'filename': '微信图片',
        }
        r = requests.post(url, data=json.dumps(data),headers=headers).content
        key = json.loads(r).get('result', dict())
        return key



    # def schedule(self):
    #     rootdir = '/Users/investarget/Desktop/django_server/pdffile/'
    #     filelist = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    #     print len(filelist)
    #     for i in range(0, 1):
    #         filepath = os.path.join(rootdir, filelist[i])
    #         # print filepath
    #
    #
    #         if os.path.isfile(filepath):
    #             # for group in self.group_list:
    #             #     groupname = group['UserName']
    #             groupnames = [u'别墅1']
    #             for groupname in groupnames:
    #
    #                 if self.send_file_msg_by_uid(filepath, self.get_user_id(groupname)):
    #                     print '发送成功'
    #                 else:
    #                     print '发送失败'
    #                 time.sleep(60)
    #             os.remove(filepath)

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.run()

if __name__ == '__main__':
    main()
