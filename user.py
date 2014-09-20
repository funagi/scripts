import re
import threading
import time

import requests


class User:
    def __init__(self, account, password):
        self.account = account
        self.password = password
        self.session = False
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}

    def login(self):

        params = {'jumpurl': 'index.php',
                  'step': '2',
                  'lgt': '1',
                  'hideid': '1',
                  'cktime': '31536000'}
        params['pwuser'] = self.account
        params['pwpwd'] = self.password
        s = requests.session()
        s.post('http://bbs.9gal.com/login.php?', data=params, headers=self.headers)
        self.session = s


    def smbox(self):
        r = self.session.get('http://bbs.9gal.com/index.php', timeout=10, headers=self.headers)
        findBanner = re.compile(r'<a href="(diy_ad_move.php?.*)" target="_blank"')
        findSMBox = re.compile(r'.*<td><a href="(kf_smbox.*)">.{1,3}</a></td>.*')
        self.s.get('http://bbs.9gal.com/' + findBanner.search(r.text).group(1), headers=self.headers)
        print('点广告', 'http://bbs.9gal.com/' + findBanner.search(r.text).group(1))
        r = self.s.get('http://bbs.9gal.com/kf_smbox.php', headers=self.headers)
        self.s.get('http://bbs.9gal.com/' + findSMBox.search(r.text).group(1), headers=self.headers)
        print('抽取盒子', 'http://bbs.9gal.com/' + findSMBox.search(r.text).group(1))

    def card(self):
        self.session.post('http://bbs.9gal.com/kf_fw_ig_one.php', data={'one': '1'}, headers=self.headers)
        print('抽取卡片')

    def print_info(self):
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        r = self.session.get('http://bbs.9gal.com/index.php', timeout=10, headers=self.headers)
        user = re.search(r'profile\.php\?action=.*?>(.*)</a>', r.text).group(1)
        zaixian = re.search(r'="color:#339900">(.*)</span> 分钟', r.text).group(1).strip()
        KFB = re.search(r'="color:#339900">(.*)</span> KFB', r.text).group(1).strip()

        print(user, '时间(分钟)：', zaixian, 'KFB:', KFB)

    def work(self):
        while True:
            try:
                self.print_info()

                r = self.session.get('http://bbs.9gal.com/index.php', timeout=10, headers=self.headers)
                findSM = re.compile(r'神秘盒子</a>(.*?)</div>')
                findCard = re.compile(r'道具卡片</a>(.*?)</div>')
                if '现在可以抽取' in findSM.search(r.text).group(1):
                    self.smbox()
                if '现在可以抽取' in findCard.search(r.text).group(1):
                    self.card()
                print('sleep 120')
                time.sleep(120)
            except Exception as e:
                print(e)

    def start(self):
        self.login()
        t = threading.Thread(target=self.work)
        t.start()