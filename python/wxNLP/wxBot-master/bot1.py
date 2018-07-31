# coding: utf-8


import datetime
import pymongo
from pymongo import WriteConcern
import fileinput
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
        self.card_list = []
        self.link_list = []
        self.linkpdf_path = '/Users/investarget/Desktop/django_server/link.html'
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
                                for user_des in self.des_list:
                                    if user_des['fromuser'] == fromuser:
                                        self.des_list.remove(user_des)
                                        break
                                if user_id:
                                    self.des_list.append({
                                        'user_id': user_id,
                                        'fromuser': fromuser,
                                        'time': int(time.time()),
                                    })

                        elif content == u'名片':
                            self.card_list.append({
                                        'fromuser': fromuser,
                                        'time': int(time.time()),
                                    })
                        elif content == u'是':
                            for link in self.link_list:
                                if link['time'] > int(time.time()) - 300:
                                    if link['fromuser'] == fromuser:
                                        self.savelink(link['link_url'], link['link_title'], link['link_desc'], fromuser)
                                        self.link_list.remove(link)
                                        break

                    elif msg_content.get('type') == 3:
                        msg_id = msg.get('msg_id')
                        img_path = os.path.join(self.temp_pwd, 'img_' + msg_id + '.jpg')
                        key = None
                        for card_user in self.card_list:
                            if fromuser == card_user['fromuser']:
                                res = self.ccupload_image(img_path)
                                userdata = self.parseCCUploadResult(res)
                                if userdata:
                                    user_id = self.get_user_id_by_account(userdata.get('mobile'))
                                    if user_id:
                                        key = self.upload_image(img_path)
                                        data = {
                                            'userlist':[user_id],
                                            'userdata':{
                                                'cardBucket': 'image',
                                                'cardKey': key,
                                            }
                                        }
                                        resu = self.updateuser(data)
                                        if resu.get('code') == 1000:
                                            self.send_msg_by_uid('%s，该投资人名片已更新' % fromuser,
                                                                 self.get_user_id(fromgroup))
                                        else:
                                            self.send_msg_by_uid('%s，该投资人名片更新失败，error--%s' % (fromuser, repr(resu)),
                                                                 self.get_user_id(fromgroup))
                                    else:
                                        if userdata.get('user'):
                                            key = self.upload_image(img_path)
                                            data = {
                                                'title': self.get_title_id_by_titleC(userdata.get('title')),
                                                'org': self.get_org_id_by_title(userdata.get('org')),
                                                'cardBucket': 'image',
                                                'cardKey': key,
                                                'usernameC':userdata.get('user'),
                                                'mobile': userdata.get('mobile'),
                                                'email': userdata.get('email'),
                                            }
                                            resu = self.createuser(data)
                                            if resu.get('code') == 1000:
                                                self.send_msg_by_uid('%s，该投资人不在平台上，已增加到平台' % fromuser, self.get_user_id(fromgroup))
                                            else:
                                                self.send_msg_by_uid('%s，该投资人不在平台上，新增失败，error--%s' % (fromuser, repr(resu)),
                                                                     self.get_user_id(fromgroup))
                                        else:
                                            self.send_msg_by_uid('%s，该投资人不在平台上，未识别出投资人姓名，无法新增' % fromuser, self.get_user_id(fromgroup))
                                else:
                                    self.send_msg_by_uid('%s，该名片识别失败' % fromuser, self.get_user_id(fromgroup))
                                if os.path.exists(img_path):
                                    os.remove(img_path)
                                self.card_list.remove(card_user)
                                break
                        if not key:
                            for des_user in self.des_list:
                                if fromuser == des_user['fromuser']:
                                    if des_user['time'] > int(time.time()) - 300:
                                        key = self.upload_image(img_path)
                                        self.saveimgtouser(userid=des_user['user_id'], bucket_key=key, bucket='image')
                                        if os.path.exists(img_path):
                                            os.remove(img_path)
                                    else:
                                        self.des_list.remove(des_user)
                                    break
                    elif msg_content.get('type') == 7:
                        self.link_list.append({
                                        'link_url': content.get('url', None),
                                        'link_title': content.get('title', None),
                                        'link_desc': content.get('desc', None),
                                        'fromuser': fromuser,
                                        'time': int(time.time()),
                                    })
                        self.send_msg_by_uid('%s，是否将该分享链接保存至系统，请回答 \'是\' 或者 \'否\' ' % fromuser, self.get_user_id(fromgroup))
                except Exception:
                    print traceback.format_exc()

            # if msg_content.get('type') == 0:
            #     # 0 -> Text
            #     # 1 -> Location
            #     # 3 -> Image
            #     # 4 -> Voice
            #     # 5 -> Recommend
            #     # 6 -> Animation
            #     # 7 -> Share
            #     # 8 -> Video
            #     # 9 -> VideoCall
            #     # 10 -> Redraw
            #     # 11 -> Empty
            #     # 99 -> Unknown
            #     msg_from = msg.get('user')
            #     payload = {
            #         'name': msg_content.get('user', dict()).get('name', 'unknown_user'),
            #         'content': content,
            #         'group_name': msg_from.get('name', 'unknown_group'),
            #         'createtime': datetime.datetime.now(),
            #         'isShow': False,
            #     }
            #     WXCollection.insert(payload)
            elif msg_content.get('type') == 3 and fromgroup in [u'特工']:
                msg_from = msg.get('user')
                msg_id = msg.get('msg_id')
                img_path = os.path.join(self.temp_pwd, 'img_' + msg_id + '.jpg')
                savekey = self.upload_image(img_path)
                payload = {
                    'name': msg_content.get('user', dict()).get('name', 'unknown_user'),
                    'content': ('https://o79atf82v.qnssl.com/' + savekey) if savekey else ('图片丢失-%s'%msg_id),
                    'group_name': msg_from.get('name', 'unknown_group'),
                    'createtime': datetime.datetime.now(),
                    'isShow': False,
                }
                WXCollection.insert(payload)
                if savekey:
                    if os.path.exists(img_path):
                        os.remove(img_path)

    def savelink(self, link_url, link_title, link_desc, share_user):
        if not os.path.exists(self.linkpdf_path):
            f = open(self.linkpdf_path, 'a')
            f.writelines('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
            f.writelines('<h1 style="text-align:center">海拓一周好文分享%s-*上传日期*</h1>' % (str(datetime.datetime.now())[:10]).replace('-','/'))
            f.close()
        f = open(self.linkpdf_path, 'a')
        content = ('<a href=%s>%s</a><br>'
                   '描述： %s<br>'
                   '分享人： %s' % (link_url, link_title, link_desc, share_user)).encode('utf-8')
        f.writelines(content)
        f.writelines('<br><br>')
        f.close()


    def save_file_to_dataroom(self, filekey, filename):
        data = {
            'dataroom': 1396,   #251 上id是1396，39上是214
            'parent': 67196,
            'orderNO': 15,
            'filename': '微信分享' + filename[:10],
            'key': filekey,
            'bucket': 'file',
            'isFile': True,
        }
        url = base_url + 'dataroom/file/'
        headers = {
            'Content-Type': 'application/json',
            'token': token,
            'source': '1',
        }
        r = requests.post(url, data=json.dumps(data), headers=headers).content
        result = json.loads(r)
        if result['code'] == 1000:
            return result['result']['id']
        return None


    def get_user_id_by_orgAndUser(self, orgname, username):
        user_id = None
        url = base_url + 'user/?usernameC=%s&search=%s' % (username, orgname)
        headers = {
            'token': token,
            'source': '1',
        }
        r = requests.get(url, headers=headers).content
        res = json.loads(r).get('result', dict()).get('data', list())
        if len(res) > 0:
            user = res[0]
            if user.get('id', None):
                user_id = user['id']
        return user_id

    def get_user_id_by_account(self, account):
        user_id = None
        if account:
            url = base_url + 'user/checkexists/?account=%s' % account
            headers = {
                'token': token,
                'source': '1',
            }
            r = requests.get(url, headers=headers).content
            user = json.loads(r).get('result', dict()).get('user')
            if user:
                user_id = user['id']
        return user_id

    def get_org_id_by_title(self, orgtitle):
        org_id = None
        if orgtitle:
            url = base_url + 'org/?search=%s' % orgtitle
            headers = {
                'token': token,
                'source': '1',
            }
            r = requests.get(url, headers=headers).content
            res = json.loads(r).get('result', dict()).get('data', list())
            if len(res) > 0:
                org = res[0]
                if org.get('id', None):
                    org_id = org['id']
        return org_id

    def get_title_id_by_titleC(self, titleC):
        titleId = None
        headers = {
            'token': token,
            'source': '1',
        }
        if titleC:
            if u'区总裁' in titleC:
                titleC = u'总裁'
            countrylist = json.loads(requests.get(base_url + 'source/title?search=%s' % titleC, headers=headers).content)
            countrylist = countrylist.get('result', [])
            if len(countrylist) > 0:
                titleId = countrylist[0]['id']
            if not titleId:
                titleId = 8
        return titleId

    def upload_image(self, img_path):
        url = base_url + 'service/qiniubigupload?topdf=0&bucket=image'
        files = {'images': open(img_path, 'rb')}
        headers = {
            'token':token,
            'source': '1',
        }
        r = requests.post(url, files=files, headers=headers).content
        key = json.loads(r).get('result',dict()).get('key', None)
        return key

    def upload_file(self, file_path):
        url = base_url + 'service/qiniubigupload?topdf=0&bucket=file'
        files = {'file': open(file_path, 'rb')}
        headers = {
            'token':token,
            'source': '1',
        }
        r = requests.post(url, files=files, headers=headers).content
        key = json.loads(r).get('result',dict()).get('key', None)
        return key

    #名片识别
    def ccupload_image(self, img_path):
        url = base_url + 'service/ccupload'
        files = {'images': open(img_path, 'rb')}
        headers = {
            'token':token,
            'source': '1',
        }
        r = requests.post(url, files=files, headers=headers).content
        res = json.loads(r)
        return res

    def parseCCUploadResult(self, result):
        try:
            res = json.loads(result['result'])
            username = None
            name = res.get('formatted_name', [])
            if len(name) > 0:
                username = name[0]['item']
            orgname = None
            organizations = res.get('organization', [])
            for organization in organizations:
                if organization['item'].get('name'):
                    orgname = organization['item'].get('name')

            tel = None
            tels = res.get('telephone', [])
            for teldic in tels:
                if u'cellular' in teldic['item']['type']:
                    tel = teldic['item'].get('number','').replace('+86', '').replace('-', '')

            email = None
            emails = res.get('email', [])
            if len(emails) > 0:
                email = emails[0]['item']


            title = None
            titles = res.get('title', [])
            if len(titles) > 0:
                title = titles[0]['item']

            resa = {
                'title': title,
                'org': orgname,
                'user': username,
                'mobile': tel,
                'email': email,
            }
            return resa
        except Exception:
            return None

    def saveimgtouser(self, userid, bucket_key, bucket):
        url = base_url + 'user/atta/'
        headers = {
            'Content-Type': 'application/json',
            'token': token,
            'source': '1',
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

    def updateuser(self, data):
        url = base_url + 'user/'
        headers = {
            'Content-Type': 'application/json',
            'token': token,
            'source': '1',
        }
        r = requests.put(url, data=json.dumps(data), headers=headers).content
        result = json.loads(r)
        return result

    def createuser(self, data):
        url = base_url + 'user/'
        headers = {
            'Content-Type': 'application/json',
            'token': token,
            'source': '1',
        }
        r = requests.post(url, data=json.dumps(data), headers=headers).content
        result = json.loads(r)
        return result


    def createOrg(self, data):
        url = base_url + 'org/?&lang=cn'
        headers = {
            'Content-Type': 'application/json',
            'token': token,
            'source': '1',
        }
        r = requests.post(url, data=json.dumps(data), headers=headers).content
        result = json.loads(r)
        if result['code'] == 1000:
            return result['result']['id']
        return None


    def schedule(self):
        expiredate = int(time.time()) - 300
        for dic in self.link_list:
            if dic['time'] < expiredate:
                self.link_list.remove(dic)
                break
        for dic in self.card_list:
            if dic['time'] < expiredate:
                self.card_list.remove(dic)
                break
        for dic in self.des_list:
            if dic['time'] < expiredate:
                self.des_list.remove(dic)
                break


        if os.path.exists(self.linkpdf_path):
            from bs4 import BeautifulSoup
            fp = open(self.linkpdf_path, mode='r').read()
            soup = BeautifulSoup(fp, 'html.parser')
            title = soup.find('h1').text
            detester = title.replace('海拓一周好文分享', '').replace('-*上传日期*', '').replace('/', '-').replace('\n','')
            datetimeStruct = datetime.datetime.strptime(detester, '%Y-%m-%d')
            if datetimeStruct < (datetime.datetime.now() - datetime.timedelta(seconds=60)):
                for lineone in fileinput.input(self.linkpdf_path, inplace=1):
                    lineone = lineone.replace('*上传日期*', (str(datetime.datetime.now())[:10]).replace('-', '/'))
                    print lineone
                key = self.upload_file(self.linkpdf_path)
                if key:
                    filename = str(datetimeStruct)
                    self.save_file_to_dataroom(key, filename)
                    os.remove(self.linkpdf_path)

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.run()

if __name__ == '__main__':
    main()
