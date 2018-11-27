# coding:utf-8
import datetime
import pymongo
from wxbot import *


pdfDir = '/var/www/apilog/traderWXPdf'
tempDir = '/var/www/wxBot/trader_temp'
client = pymongo.MongoClient('mongodb://192.168.1.251:27017/')
db = client.wxnlp
# db.authenticate("wxnlp", "investarget")
WXCollection = db.wxchatdata

# base_url = 'https://api.investarget.com/'
# token = 'a7305831f4903690feb349c16ab37f9b4962197305ba32c7'
base_url = 'http://192.168.1.251:8080/'
token = '8ba7e74177bee4dfe2f3da4cfd4c1f9e9e541c4d256d1bc5'


class TraderWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

    # 处理消息保存
    def handle_msg_all(self, msg):
        if msg.get('msg_type_id') == 3:
            # 3 -> 群聊类型消息
            msg_content = msg.get('content')
            msg_from = msg.get('user')
            if msg_content.get('type') == 0:  # 文字消息
                content = msg_content.get('data', '')
            elif msg_content.get('type') == 3:   # 图片消息
                msg_id = msg.get('msg_id')
                img_path = os.path.join(self.temp_pwd, 'img_' + msg_id + '.jpg')
                savekey = self.upload_image(img_path)
                content = ('https://image.investarget.com/' + savekey) if savekey else ('图片丢失-%s' % msg_id)
                if savekey:
                    if os.path.exists(img_path):
                        os.remove(img_path)
            else:
                content = None
            if content:
                payload = {
                    'name': msg_content.get('user', dict()).get('name', 'unknown_user'),
                    'content': content,
                    'group_name': msg_from.get('name', 'unknown_group'),
                    'createtime': datetime.datetime.now(),
                    'isShow': False,
                    }
                WXCollection.insert(payload)

        elif msg.get('msg_type_id') == 4:
            # 4 -> 联系人类型消息
            msg_content = msg.get('content', {})
            fromuser = msg.get('user', dict()).get('name', 'unknown_user')
            if fromuser == u'self':
                fromuser = self.my_account.get(u'NickName')
                touser = self.get_contact_name(msg.get('to_user_id'))
                if touser:
                    touser = touser.get('NickName')
            else:
                touser = self.my_account.get(u'NickName')
            if msg_content.get('type') == 0:  # 文字消息
                content = msg_content.get('data', '')
            elif msg_content.get('type') == 3:   # 图片消息
                msg_id = msg.get('msg_id')
                img_path = os.path.join(self.temp_pwd, 'img_' + msg_id + '.jpg')
                savekey = self.upload_image(img_path)
                content = ('https://image.investarget.com/' + savekey) if savekey else ('图片丢失-%s' % msg_id)
                if savekey:
                    if os.path.exists(img_path):
                        os.remove(img_path)
            else:
                content = None
            if content:
                payload = {
                        'name': fromuser,
                        'content': content,
                        'touser': touser,
                        'createtime': datetime.datetime.now(),
                        'isShow': False,
                    }
                WXCollection.insert(payload)

    def upload_image(self, img_path):
        try:
            url = base_url + 'service/qiniubigupload?topdf=0&bucket=image'
            files = {'images': open(img_path, 'rb')}
            headers = {
                'token':token,
                'source': '1',
            }
            r = requests.post(url, files=files, headers=headers).content
            key = json.loads(r).get('result',dict()).get('key', None)
            return key
        except Exception:
            return None


    def schedule(self, ):
        if self.status != 'loginsuccess':
            print('login out')
        else:
            filelist = os.listdir(pdfDir)  # 列出文件夹下所有的目录与文件
            for i in range(0, len(filelist)):
                filepath = os.path.join(pdfDir, filelist[i])
                if os.path.isfile(filepath) and os.path.splitext(filepath)[1] == '.pdf':
                    projtitle = os.path.basename(filepath)
                    contentkey = projtitle.split('：')[0]
                    content = ''
                    with open(os.path.join(pdfDir, 'projdesc.txt'), "r") as f:
                        lines = f.readlines()
                    with open(os.path.join(pdfDir, 'projdesc.txt'), "w") as f_w:
                        for line in lines:
                            if contentkey in line:
                                content = line
                                continue
                            f_w.write(line)
                    if len(content) > 0:
                        ds = json.loads(content)
                        content = ds.get(unicode(contentkey, "utf-8"), None)
                    for user in self.contact_list:
                        if content:
                            self.send_msg_by_uid(content, user['UserName'])
                        self.send_file_msg_by_uid(filepath, user['UserName'])
                    os.remove(filepath)
                    self.status = 'wait4loginout'






def main():
    bot = TraderWXBot()
    bot.DEBUG = True
    bot.temp_pwd = os.path.join(os.getcwd(),'trader_temp')
    # bot.conf['qr'] = 'tty'
    bot.run()



if __name__ == '__main__':
    main()


