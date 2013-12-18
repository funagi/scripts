#!python3
import urllib
import http.cookiejar
import re
import os
import html.parser
from bs4 import BeautifulSoup


def GetPage(Url,number=''):
    PrintInfo = "GetPage:"+ Url
    print (PrintInfo.center(60, '*'))
    html_src = urlOpener.open(Url).read().decode('utf-8')
    parser = BeautifulSoup(html_src)
    ResultName = parser.select('div.bookWidget')
    PictureLink = parser.select('p.detailbookImg')
    NextPage = parser.select('p.pager-next a[href]')

    FindResName = re.compile(r'<h2>『(.*)』の検索結果</h2>')
    FindPicName = re.compile(r'<img alt="(.*)" src=')
    FindPicName2 = re.compile(r"<img alt='(.*)' src=")
    FindPicUrl = re.compile(r'src="(.*?)(\d+)(.*)" width="200"')
    ResName = FindResName.search(str(ResultName)).group(1).replace('?','').replace('!','')
    PicName = []
    PicUrl = []
    for item in PictureLink:
        PicNumber = int(FindPicUrl.search(str(item)).group(2)) - 1
        if(FindPicName.search(str(item))!=None):
            PicName.append('coverImage' + str(PicNumber) + ' ' + FindPicName.search(str(item)).group(1).replace('?','').replace('!','') + FindPicUrl.search(str(item)).group(3))
        else:
            PicName.append('coverImage' + str(PicNumber) + ' ' + FindPicName2.search(str(item)).group(1).replace('"',"'" ).replace('?','').replace('!','') + FindPicUrl.search(str(item)).group(3))
        PicUrl.append((FindPicUrl.search(str(item)).group(1) + str(PicNumber) + FindPicUrl.search(str(item)).group(3)).replace('thumbnailImage', 'coverImage'))

    if not os.path.isdir(number+' '+ResName):
        os.mkdir(number+' '+ResName)
    for PName, PUrl in zip(PicName, PicUrl):
        if not '立ち読み版' in PName:
            FilePath = str(os.path.abspath(number+' '+ResName))
            FilePath += "\\" + PName
            if os.path.exists(FilePath):
                print (PName, " Already Saved")
            else:
                GetPicture(PName, PUrl, FilePath)

    if(NextPage!=[]):
        FindNextPage=re.compile(r'<a href="\.(.*)">後へ</a>')
        NextPageUrl =Url[:Url.find('/?order=')]+html.parser.HTMLParser().unescape(FindNextPage.search(str(NextPage[0])).group(1))
        GetPage(NextPageUrl,number)
    else:
        PrintInfo = "Over"
        print (PrintInfo.center(60, '*'))



def GetPicture(PicName, PicUrl, FilePath):
    print ("GetPicture:", PicUrl)
    picture = urlOpener.open(PicUrl)
    file_size = picture.getheader('Content-Length').strip()
    print ("Downloading: %s Bytes: %s" % (PicName, file_size))
    tempFile = picture.read()
    with open(FilePath, 'w+b') as file:
        file.write(tempFile)
    print (PicName, ' Saved\n')




def main():
    while True:
        number = input("输入序号：")
        Url='http://bookwalker.jp/series/'+number+'/?order=release&detail=1&qser='+number
        GetPage(Url,number)


if __name__ == '__main__':
    cookiejar = http.cookiejar.LWPCookieJar()
    urlOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar), urllib.request.HTTPHandler())
    urlOpener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')]
    main()

