import csv
import threading
import html.parser
import urllib
import urllib.request
import http.cookiejar
import os
import io
import psycopg2
import time
import queue

parseQuene = queue.Queue()
parsedIllust = []

PHPSESSID=0
cookiejar = http.cookiejar.LWPCookieJar()
urlOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar), urllib.request.HTTPHandler())
urlOpener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')]
urllib.request.install_opener(urlOpener)



def login():
    if not os.path.exists(r"cookie.txt"):
        PixivID = input("ID:")
        password = input("Password:")
        post_data = {
            'mode': 'login',
            'skip': '1'
        }
        post_data["pixiv_id"] = PixivID
        post_data["pass"] = password
        request = urllib.request.Request('http://www.pixiv.net/login.php',
                                         urllib.parse.urlencode(post_data).encode(encoding='utf_8'))
        urlOpener.open(request)
        cookiejar.save("cookie.txt")
    else:
        cookiejar.load("cookie.txt")


def parseIllust():
    while not parseQuene.empty():
        global parsedIllust

        start = time.clock()
        tempID = parseQuene.get()
        url = "http://spapi.pixiv.net/iphone/illust.php?PHPSESSID=" + PHPSESSID + "&illust_id=" + str(
            tempID)
        try:
            htmlSrc = urllib.request.urlopen(url, timeout=10).read().decode('utf-8')
            if htmlSrc:
                reader = csv.reader(io.StringIO(htmlSrc.replace('\0', '')))
                finalList = list(reader)[0]
                if finalList[12]:
                    tempParsedIllust = []
                    tempParsedIllust.append(tempID)
                    tempParsedIllust.append(int(finalList[1]))
                    tempParsedIllust.extend(finalList[2:4])
                    if finalList[4]:
                        tempParsedIllust.append(int(finalList[4]))
                    else:
                        tempParsedIllust.append(0)
                    tempParsedIllust.extend(finalList[5:13])
                    temp1 = finalList[13].split()
                    tempParsedIllust.append(temp1)
                    tempParsedIllust.extend(finalList[14:15])
                    tempParsedIllust.append(int(finalList[15]))
                    tempParsedIllust.append(int(finalList[16]))
                    tempParsedIllust.append(int(finalList[17]))
                    tempParsedIllust.append(finalList[18])
                    if not finalList[19] or finalList[19] == '0':
                        tempParsedIllust.append(1)
                    else:
                        tempParsedIllust.append(int(finalList[19]))
                    tempParsedIllust.extend(finalList[20:22])
                    if not finalList[22] or finalList[22] == '0':
                        tempParsedIllust.append(1)
                    else:
                        tempParsedIllust.append(int(finalList[22]))
                    tempParsedIllust.extend(finalList[23:])
                    print(tempID, time.clock() - start)
                    parsedIllust.append(tempParsedIllust)
        except Exception as e:
            print(e)
            if str(e)=="time out":
                parseQuene.put(tempID)
        finally:
            parseQuene.task_done()


def insert():
    global parsedIllust
    if parsedIllust:
        query = ''.join('insert into base values')
        for i in parsedIllust:
            query += '('
            for j in i:
                if isinstance(j, int):
                    query += str(j) + ','
                elif isinstance(j, list):
                    if j:
                        query += "'{"
                        for k in j:
                            query += '"' + k.replace('"', "'").replace("'", "''").replace('\\', '\\\\') + '",'
                        query = query[:-1] + "}',"
                    else:
                        query += "'{}',"
                else:
                    query += "'" + j.replace('"', "'").replace("'", "''").replace('\\', '\\\\') + "',"
            query = query[:-1] + '),'
        query = query[:-1] + ';'
        parsedIllust = []
        return query


conn = psycopg2.connect("dbname=xxx user=xxx password=xxx")
cur = conn.cursor()
login()
global PHPSESSID
for i in cookiejar:
    if i.name == "PHPSESSID":
        PHPSESSID = i.value


first = 36490000
while True:
    totalStart = time.clock()
    querys = []
    for i in range(6):
        start = time.clock()
        for i in range(first, first + 10000):
            parseQuene.put(i)
        th = []
        for i in range(30):
            t = threading.Thread(target=parseIllust)
            t.start()
            th.append(t)
        for i in th:
            i.join()
        querys.append(insert())
        print('Time:', time.clock() - start)
        first += 10000
    for query in querys:
        cur.execute(query)
        print(query)
    conn.commit()
    print('Total Time:', time.clock() - totalStart)


