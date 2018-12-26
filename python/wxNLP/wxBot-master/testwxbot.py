import os

from wxbot import WXBot


class MyWXBot(WXBot):

    def __init__(self):
        self.attach_dic = {}
        self.card_list = []
        self.link_list = []
        self.linkpdf_path = '/var/www/wxBot/linkfile/link.html'
        self.wxShareFile = '/var/www/investarget-web/investarget-desktop/wx_share_files'
        WXBot.__init__(self)

    def get_file(self, msg):
        cookiesList = {name: data for name, data in self.session.cookies.items()}
        url = self.base_uri + '/webwxgetmedia'
        params = {
            'sender': msg['FromUserName'],
            'mediaid': msg['MediaId'],
            'filename': msg['FileName'],
            'fromuser': self.uin,
            'pass_ticket': 'undefined',
            'webwx_data_ticket': cookiesList['webwx_data_ticket']
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}
        r = self.session.get(url, params=params, stream=True, headers=headers)
        data = r.content
        fn = 'file_' + msg['MsgId'] + os.path.splitext(msg['FileName'])[1]
        with open(os.path.join(self.wxShareFile, fn), 'wb') as f:
            f.write(data)
        return fn



    def handle_msg_all(self, msg):
        pass

def main():
    bot = MyWXBot()
    bot.DEBUG = True
    # bot.conf['qr'] = 'tty'
    bot.run()

if __name__ == '__main__':
    main()