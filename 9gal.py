#!python3
import time
import requests
import re

def smbox(s,r):
    s.get('http://bbs.9gal.com/'+findBanner.search(r.text).group(1))
    print('点广告','http://bbs.9gal.com/'+findBanner.search(r.text).group(1))
    r=s.get('http://bbs.9gal.com/kf_smbox.php')
    s.get('http://bbs.9gal.com/'+findSMBox.search(r.text).group(1))
    print('抽取盒子','http://bbs.9gal.com/'+findSMBox.search(r.text).group(1))

def card(s):
    s.post('http://bbs.9gal.com/kf_fw_ig_one.php', data={'one':'1'})
    print('抽取卡片')



if __name__ == '__main__':
    parameters = {
    'jumpurl': 'index.php',
    'step': '2',
    'lgt': '1',
    'hideid': '1',
    'cktime': '31536000',
    'pwuser': 'XXXXX',
    'pwpwd': 'XXXXX'
    }
    s1=requests.session()
    s1.post('http://bbs.9gal.com/login.php?', data=parameters)
    findUser=re.compile(r'上次登录.*">(.*)</a>')
    findTime=re.compile(r'<span style="color:#339900">(.*)</span><br />')
    findKFB=re.compile(r'<span style="color:#339900">(.*)</span>')
    findBanner=re.compile(r'<a href="(diy_ad_move.php?.*)" target="_blank"')
    findSMBox=re.compile(r'.*<td><a href="(kf_smbox.*)">.{1,3}</a></td>.*')
    while True:
        try:
            print(time.strftime('%Y-%m-%d %H:%M:%S'))
            r=s1.get('http://bbs.9gal.com/index.php',timeout=10)
            print(findUser.search(r.text).group(1),findTime.search(r.text).group(1),findKFB.search(r.text).group(1))
            if '现在可以免费抽取奖励' in r.text:
                smbox(s1,r)
            if '现在可以抽取奖励' in r.text:
                card(s1)
            time.sleep(120)
        except Exception as e:
            print(e)