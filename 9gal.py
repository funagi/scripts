#!python3
import time
import requests
import re

userName=''
userPWD=''

def smbox(s, r):
    findBanner = re.compile(r'<a href="(diy_ad_move.php?.*)" target="_blank"')
    findSMBox = re.compile(r'.*<td><a href="(kf_smbox.*)">.{1,3}</a></td>.*')
    s.get('http://bbs.9gal.com/' + findBanner.search(r.text).group(1), headers=headers)
    print('点广告', 'http://bbs.9gal.com/' + findBanner.search(r.text).group(1))
    r = s.get('http://bbs.9gal.com/kf_smbox.php', headers=headers)
    s.get('http://bbs.9gal.com/' + findSMBox.search(r.text).group(1), headers=headers)
    print('抽取盒子', 'http://bbs.9gal.com/' + findSMBox.search(r.text).group(1))


def card(s):
    s.post('http://bbs.9gal.com/kf_fw_ig_one.php', data={'one': '1'}, headers=headers)
    print('抽取卡片')


def main():
    parameters = {
        'jumpurl': 'index.php',
        'step': '2',
        'lgt': '1',
        'hideid': '1',
        'cktime': '31536000',
        'pwuser': userName,
        'pwpwd': userPWD
    }
    while True:
        try:
            s1 = requests.session()
            s1.post('http://bbs.9gal.com/login.php?', data=parameters, headers=headers)
            break
        except Exception as e:
            print(e)
            time.sleep(5)

    while True:
        findUser = re.compile(r'上次登录.*">(.*)</a>')
        findTime = re.compile(r'<span style="color:#339900">(.*)</span><br />')
        findKFB = re.compile(r'<span style="color:#339900">(.*)</span>')
        try:
            print(time.strftime('%Y-%m-%d %H:%M:%S'))
            r = s1.get('http://bbs.9gal.com/index.php', timeout=10, headers=headers)
            print(findUser.search(r.text).group(1), findTime.search(r.text).group(1), findKFB.search(r.text).group(1))
            if '现在可以免费抽取奖励' in r.text:
                smbox(s1, r)
            if '现在可以抽取奖励' in r.text:
                card(s1)
            print('sleep 120')
            time.sleep(120)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'}
    main()