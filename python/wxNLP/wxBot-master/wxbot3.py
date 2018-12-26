#coding:utf-8
import datetime
import threading

import pymongo
import json
from wxbot import *
import sys
import fileinput
reload(sys)
sys.setdefaultencoding('utf-8')

client = pymongo.MongoClient('mongodb://192.168.1.251:27017/')
db = client.wxnlp
# db.authenticate("wxnlp", "investarget")
WXCollection = db.wxchatdata

# base_url = 'https://api.investarget.com/'
# token = 'a7305831f4903690feb349c16ab37f9b4962197305ba32c7'
base_url = 'http://192.168.1.251:8080/'
token = '8ba7e74177bee4dfe2f3da4cfd4c1f9e9e541c4d256d1bc5'

trader_list = {
    u'周炫Fabian': 100000002,
    u'贺斯渡 Serena': 100005379,
    u'裔传麒Vans': 100017321,
    u'Eric周': 100017320,
    u'Joy': 100009226,
    u'Lois': 100005504,
    u'蔡云东方 Erik': 100017193,
    u'尹乐鸣': 100010424,
    u'chenyi': 100014845,
    u'叶师傅': 100007593,
    u'樊杨阳': 100000005,
    u'王菲': 100000004,
}


class MyWXBot(WXBot):

    def __init__(self):
        self.attach_dic = {}
        self.card_list = []
        self.link_list = []
        self.linkpdf_path = '/var/www/wxBot/linkfile/link.html'
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
            if fromgroup:
                try:
                    if msg_content.get('type') == 0:
                        if len(content.split()) == 2:
                            if self.attach_dic.get(fromuser):
                                username = content.split()[-1]
                                orgname = content.split()[0]
                                user_id = self.get_user_id_by_orgAndUser(orgname, username)
                                if user_id:
                                    for attach in self.attach_dic.get(fromuser, []):
                                        if fromuser == attach['fromuser']:
                                            if attach['time'] > int(time.time()) - 300:
                                                img_path = attach['img_path']
                                                key = self.upload_image(img_path)
                                                self.saveimgtouser(userid=user_id, bucket_key=key,
                                                                       bucket='image')
                                                if os.path.exists(img_path):
                                                    os.remove(img_path)
                                            else:
                                                if len(self.attach_dic.get(fromuser, [])) > 0:
                                                    self.attach_dic.get(fromuser, []).pop()
                                            break
                                if len(self.attach_dic.get(fromuser, [])) > 0:
                                    self.attach_dic[fromuser].remove(self.attach_dic[fromuser][0])
                        elif content == '名片':
                            self.card_list.append({
                                        'fromuser': fromuser,
                                        'time': int(time.time()),
                                    })
                        elif content == '是':
                            for link in self.link_list:
                                if link['time'] > int(time.time()) - 300:
                                    if link['fromuser'] == fromuser:
                                        if link['fileMsg']:
                                            fileins = self.get_file(link['fileMsg'])
                                            link['link_url'] = '/wxShareFile/' + fileins
                                        self.savelink(link['link_url'], link['link_title'], link['link_desc'], fromuser)
                                        self.link_list.remove(link)
                                        break
                        elif content == u'不保存':
                            self.attach_dic.pop(fromuser)
                    elif msg_content.get('type') == 3:
                        t = threading.Thread(target=self.handleImagecontent, args=(msg, fromuser, fromgroup))
                        t.start()
                    elif msg_content.get('type') == 7:
                        self.link_list.append({
                                        'link_url': content.get('url', None),
                                        'link_title': content.get('title', None),
                                        'link_desc': content.get('desc', None),
                                        'fromuser': fromuser,
                                        'time': int(time.time()),
                                        'fileMsg': content.get('fileMsg', None)
                                    })
                        self.send_msg_by_uid('%s，是否将该分享链接保存至系统，请回答 \'是\' 或者 \'否\' ' % fromuser, self.get_user_id(fromgroup))
                except Exception:
                    self.saveException(traceback.format_exc())

    def saveException(self, error):
        with open('wxbot2.log', 'a') as f:
            f.write(str(datetime.datetime.now())[:19])
            f.write(error)
            f.write('\n')



    def handleImagecontent(self, msg, fromuser, fromgroup):
        msg_id = msg.get('msg_id')
        img_path = os.path.join(self.temp_pwd, 'img_' + msg_id + '.jpg')
        is_card = False
        for card_user in self.card_list:
            if fromuser == card_user['fromuser'] and card_user['time'] > int(time.time()) - 300:
                is_card = True
                res = self.ccupload_image(img_path)
                userdata = self.parseCCUploadResult(res)
                if userdata:
                    user_id = self.get_user_id_by_account(userdata.get('mobile'))
                    if user_id:
                        self.addUserTrader(user_id, fromuser)
                        key = self.upload_image(img_path)
                        data = {
                            'userlist': [user_id],
                            'userdata': {
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
                                'cardBucket': 'image',
                                'groups': [1, ],
                                'cardKey': key,
                                'usernameC': userdata.get('user'),
                                'mobile': userdata.get('mobile'),
                                'email': userdata.get('email'),
                            }
                            resu = self.createuser(data)
                            if resu.get('code') == 1000:
                                user_id = resu.get('result').get('id')
                                self.addUserTrader(user_id, fromuser)
                                self.send_msg_by_uid('%s，该投资人(%s)不在平台上，已增加到平台' % (fromuser, userdata.get('mobile')),
                                                     self.get_user_id(fromgroup))
                            else:
                                self.send_msg_by_uid('%s，该投资人(%s)不在平台上，新增失败，error--%s' % (
                                fromuser, userdata.get('mobile'), resu.get('errormsg')),
                                                     self.get_user_id(fromgroup))
                        else:
                            self.send_msg_by_uid('%s，该投资人不在平台上，未识别出投资人姓名，无法新增' % fromuser, self.get_user_id(fromgroup))
                else:
                    self.send_msg_by_uid('%s，该名片识别失败' % fromuser, self.get_user_id(fromgroup))
                    #  self.card_list.remove(card_user)
                break
        if not is_card:
            self.attach_dic[fromuser] = []
            self.attach_dic.get(fromuser).append({
                'img_path': img_path,
                'fromuser': fromuser,
                'time': int(time.time()),
            })
            self.send_msg_by_uid('%s，保存至附件请回复所属投资人的机构及姓名，中间以空格分隔，如\'多维海拓  summer\'，如不保存则回复 \'不保存\'' % fromuser,
                                 self.get_user_id(fromgroup))


    def addUserTrader(self, user_id, trader_user_name):
        trader_id = trader_list.get(trader_user_name)
        if trader_id:
            data = {
                'investoruser': user_id,
                'traderuser': trader_id,
                'relationtype': True,
                #'familiar': 99,
            }
            url = base_url + 'user/relationship/'
            headers = {
                'Content-Type': 'application/json',
                'token': token,
                'source': '1',
            }
            r = requests.post(url, data=json.dumps(data), headers=headers).content
            result = json.loads(r)
            if result['code'] == 1000 or result['code'] == 2012:
                return True
        return False


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
                    tel = teldic['item'].get('number','').replace('+86', '').replace('-', '').replace(' ', '')

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

    def save_file_to_dataroom(self, filekey, filename):
        data = {
            'dataroom': 214,
            'parent': 26147,
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
    
    def schedule(self):

        pass
        # expiredate = int(time.time()) - 300
        # for dic in self.link_list:
         #    if dic['time'] < expiredate:
         #        self.link_list.remove(dic)
         #        break
        # for dic in self.card_list:
         #    if dic['time'] < expiredate:
         #        self.card_list.remove(dic)
         #        break
        # for key, value in self.attach_dic.items():
         #    if len(value) > 1:
         #        self.attach_dic[key] = value[-1:]
         #    if len(self.attach_dic[key]) == 1:
         #        if self.attach_dic[key][0]['time'] < expiredate:
         #            self.attach_dic[key] = []
        #
        #
        # if os.path.exists(self.linkpdf_path):
         #    from bs4 import BeautifulSoup
         #    fp = open(self.linkpdf_path, mode='r').read()
         #    soup = BeautifulSoup(fp, 'html.parser')
         #    title = soup.find('h1').text
         #    detester = title.replace('海拓一周好文分享', '').replace('-*上传日期*', '').replace('/', '-').replace('\n','')
        # datetimeStruct = datetime.datetime.strptime(detester, '%Y-%m-%d')
        # if datetimeStruct < (datetime.datetime.now() - datetime.timedelta(hours=24 * 7)):
         #        for lineone in fileinput.input(self.linkpdf_path, inplace=1):
         #            lineone = lineone.replace('*上传日期*', (str(datetime.datetime.now())[:10]).replace('-', '/'))
         #            print lineone
		# key = self.upload_file(self.linkpdf_path)
         #        if key:
         #            filename = str(datetimeStruct)
         #            self.save_file_to_dataroom(key, filename)
         #            os.remove(self.linkpdf_path)
        #
        # rootdir = '/var/www/apilog/pdffile/'
        # filelist = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        # print len(filelist)
        # for i in range(0, len(filelist)):
         #    filepath = os.path.join(rootdir, filelist[i])
         #    if os.path.isfile(filepath) and os.path.splitext(filepath)[1] == '.pdf':
         #        projtitle = os.path.basename(filepath)
         #        contentkey = projtitle.split('：')[0]
         #        content = None
         #        with open("/var/www/apilog/pdffile/projdesc.txt","r") as f:
         #            lines = f.readlines()
         #        with open("/var/www/apilog/pdffile/projdesc.txt","w") as f_w:
         #            for line in lines:
         #                if contentkey in line:
         #                    content = line
         #                    continue
         #                f_w.write(line)
		# if len(content) > 0:
         #            ds = json.loads(content)
         #            content = ds.get(unicode(contentkey, "utf-8"), None)
         #        groupnames = [u'多维海拓投资人交流11群·大健康', u'多维海拓投资人交流1群', u'多维海拓投资人交流10群', u'多维海拓投资人交流9群',
         #                        u'多维海拓投资人交流3群', u'多维海拓投资人交流4群', u'多维海拓投资人交流12群·AR·VR', u'多维海拓投资人交流5群', u'特工']
         #        for groupname in groupnames:
         #            groupid = self.get_user_id(groupname)
         #            if content:
         #                self.send_msg_by_uid(content, groupid)
         #            if self.send_file_msg_by_uid(filepath, groupid):
         #                print '发送成功'
         #            else:
         #                print '发送失败'
         #            time.sleep(20)
         #        os.remove(filepath)
         #        time.sleep(10)



def main():
    bot = MyWXBot()
    bot.DEBUG = True
    # bot.conf['qr'] = 'tty'
    bot.run()

if __name__ == '__main__':
    main()

