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





while True:
    room = itchat.search_chatrooms(name=u'别墅1')
    # print room

    roomusername = room[0]['UserName']


    try:
        itchat.send_file(u'/Users/investarget/Desktop/django_server/pdffile/中文.pdf', toUserName=roomusername)
        print("success")
    except:
        print("fail")

    time.sleep(30)