# coding: utf-8


import datetime
import pymongo
from pymongo import WriteConcern

from wxbot import *


client = pymongo.MongoClient('mongodb://192.168.1.251:27017/')
db = client.wxnlp
WXCollection = db.wxchatdata


class MyWXBot(WXBot):
    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            self.send_msg_by_uid(u'hi', msg['user']['id'])
            self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            self.send_file_msg_by_uid("img/1.png", msg['user']['id'])

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
        if msg.get('msg_type_id') in [1,3]:
            # 3 -> 群聊类型消息
            # 2 -> File Helper
            msg_content = msg.get('content')
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
                    'name' : msg_content.get('user',dict()).get('name','unknown_user'),
                    'content': msg_content.get('data','unknown_content'),
                    'group_name': msg_from.get('name','unknown_group'),
                    'createtime': datetime.datetime.now(),
                }
                res = WXCollection.insert(payload)
                print 'response' + str(res)
                # r = requests.post('http://192.168.1.201:8000/mongolog/',data=payload)
                # print r


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.run()

if __name__ == '__main__':
    main()
