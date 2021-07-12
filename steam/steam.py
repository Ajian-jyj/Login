import time

import execjs
import requests
from Crypto.PublicKey import RSA

class SteamLogin():

    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.session = requests.session()
        self.session.headers = {
            'Host': 'store.steampowered.com',
            'Origin': 'https://store.steampowered.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
            'Referer': 'https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_4__global-header',
        }

    def get_timestamp(self):
        timestamp = int(time.time()*1000)
        timestamp = str(timestamp)
        return timestamp

    def get_rsakey(self):
        data = {
            'donotcache': self.get_timestamp(),
            'username': self.username,
        }
        url = 'https://store.steampowered.com/login/getrsakey/'
        response = self.session.post(url=url,data=data)
        rsakey = response.json()
        return rsakey

    def encryption(self,publickey_mod,publickey_exp):
        with open('encryption.js', 'r', encoding='utf8') as f:
            jsFile= f.read()
        encryption = execjs.compile(jsFile).call('test', self.password, publickey_mod, publickey_exp)
        return encryption


    def login(self):
        rsakey = self.get_rsakey()
        publickey_exp = rsakey['publickey_exp']
        publickey_mod = rsakey['publickey_mod']
        encryption = self.encryption(publickey_mod=publickey_mod,publickey_exp=publickey_exp)
        timestamp = rsakey['timestamp']
        data = {
            'donotcache': self.get_timestamp(),
            'password': encryption,
            'username': self.username,
            'twofactorcode': '',
            'emailauth': '',
            'loginfriendlyname': '',
            'captchagid': '-1',
            'captcha_text': '',
            'emailsteamid': '',
            'rsatimestamp': timestamp,
            'remember_login': 'false',
        }
        url = 'https://store.steampowered.com/login/dologin/'
        response = self.session.post(url=url,data=data)
        data = response.json()
        if 'emailauth_needed' not in data.keys():
            return False
        else:
            return True

    def main(self):
        b = self.login()
        if b == False:
            print('登录失败')
        else:
            emailauth = input('请输入验证码:')
            rsakey = self.get_rsakey()
            publickey_exp = rsakey['publickey_exp']
            publickey_mod = rsakey['publickey_mod']
            encryption = self.encryption(publickey_mod=publickey_mod, publickey_exp=publickey_exp)
            timestamp = rsakey['timestamp']
            data = {
                'donotcache': self.get_timestamp(),
                'password': encryption,
                'username': self.username,
                'twofactorcode': '',
                'emailauth': emailauth,
                'loginfriendlyname': '',
                'captchagid': '-1',
                'captcha_text': '',
                'emailsteamid': '',
                'rsatimestamp': timestamp,
                'remember_login': 'false',
            }
            url = 'https://store.steampowered.com/login/dologin/'
            response = self.session.post(url=url, data=data)
            if response.json()['success'] == True:
                print('登录成功!')
            else:
                print('登录失败!')

username = 'mo2716'
password = 'JiangZe199956@'
d = SteamLogin(username=username,password=password)
d.main()