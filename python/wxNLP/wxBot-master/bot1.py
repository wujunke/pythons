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


base_url = 'http://192.168.1.251:8080/'
token = '9fea5e61e4a86110972d22fd54cd7092d5ff5deeb4977d00'

class MyWXBot(WXBot):


    def __init__(self):
        self.des_list = []
        WXBot.__init__(self)



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
            fromgroup = msg.get('user', dict()).get('name', 'unknown_group')
            fromuser = msg_content.get('user', dict()).get('name', 'unknown_user')
            content = msg_content.get('data', 'unknown_content')
            if fromgroup in [u'特工',]:
                try:
                    if msg_content.get('type') == 0:
                        if u'机构：' in content:
                            if u'姓名：' in content:
                                username = content.replace('姓名：','').split()[-1]
                                orgname = content.replace('机构：','').split()[0]
                                user_id = self.get_user_id_by_orgAndUser(orgname,username)
                                if user_id:
                                    self.des_list.append({
                                        'user_id': user_id,
                                        'fromuser': fromuser,
                                        'time': int(time.time()),
                                    })
                    if msg_content.get('type') == 3:
                        msg_id = msg.get('msg_id')
                        img_path = os.path.join(self.temp_pwd, 'img_' + msg_id + '.jpg')
                        for des_user in self.des_list:
                            if fromuser == des_user['fromuser']:
                                if des_user['time'] < int(time.time()) + 300:
                                    key = self.upload_image(img_path)
                                    self.saveimgtouser(userid=des_user['user_id'], bucket_key=key, bucket='image')
                                    if os.path.exists(img_path):
                                        os.remove(img_path)
                                else:
                                    self.des_list.remove(des_user)
                                break
                except Exception:
                    print traceback.format_exc()

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

    def get_user_id_by_orgAndUser(self, orgname, username):
        user_id = None
        url = base_url + 'user/?usernameC=%s&search=%s' % (username, orgname)
        headers = {
            'token': token,
        }
        r = requests.get(url, headers=headers).content
        res = json.loads(r).get('result', dict()).get('data', list())
        if len(res) > 0:
            user = res[0]
            if user.get('id', None):
                user_id = user['id']
        return user_id

    def upload_image(self, img_path):
        url = base_url + 'service/qiniubigupload?topdf=0&bucket=image'
        files = {'images': open(img_path, 'rb')}
        headers = {
            'token':token,
        }
        r = requests.post(url, files=files, headers=headers).content
        key = json.loads(r).get('result',dict()).get('key', None)
        return key

    def saveimgtouser(self, userid, bucket_key, bucket):
        url = base_url + 'user/atta/'
        headers = {
            'Content-Type': 'application/json',
            'token': token,
        }
        data = {
            'user': userid,
            'bucket': bucket,
            'key': bucket_key,
            'filename': u'微信图片',
        }
        r = requests.post(url, data=json.dumps(data),headers=headers).content
        result = json.loads(r).get('result', dict())
        return result



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
