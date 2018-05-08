#coding=utf-8
import itchat
import time
from itchat.content import TEXT


# @itchat.msg_register(TEXT, isGroupChat=True)
# def text_reply(msg):
#     if msg.isAt:
#         msg.user.send(u'@%s\u2005I received: %s' % (
#             msg.actualNickName, msg.text))

itchat.auto_login()
# itchat.run()




while True:
    room = itchat.search_chatrooms(name=u'特工')
    print room

    roomusername = room[0]['UserName']


    try:
        itchat.send_file('/Users/investarget/Desktop/猕猴桃.pdf', toUserName=roomusername)
        print("success")
    except:
        print("fail")

    time.sleep(30)