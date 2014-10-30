#! /usr/bin/env python3

import asyncio
import csv
from collections import deque
import io

import aiohttp
from sqlalchemy.orm import sessionmaker, scoped_session
import tqdm

from models import db_connect, create_table, Pixiv
import settings


@asyncio.coroutine
def get(*args, **kwargs):
    response = yield from aiohttp.request('get', *args, **kwargs)
    return (yield from response.text())


def parser(page):
    page = page.replace('\x00', '')
    reader = csv.reader(io.StringIO(page))
    content = list(reader)[0]
    result = {}
    result['illust_id'] = content[0]
    result['user_id'] = content[1]
    result['illust_ext'] = content[2]
    result['title'] = content[3]
    result['image_server'] = content[4]
    result['user_name'] = content[5]
    result['illust128'] = content[6]
    result['illust480'] = content[9]
    result['time'] = content[12]
    result['tags'] = content[13]
    result['software'] = content[14]
    result['vote'] = content[15]
    result['point'] = content[16]
    result['view_count'] = content[17]
    result['description'] = content[18][1:]
    result['pages'] = content[19]
    result['bookmarks'] = content[22]
    result['user_login_id'] = content[24]
    result['user_profile_image_url'] = content[29]
    return result


@asyncio.coroutine
def get_illust(url):
    with (yield from SEM):
        page = yield from get(url, compress=True, connector=CONN)
    if page:
        result = parser(page)
        WHOLERESULT.append(result)


@asyncio.coroutine
def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f


def connect_db():
    engine = db_connect()
    create_table(engine)
    sessionFactory = sessionmaker(bind=engine)
    global SESSION
    SESSION = scoped_session(sessionFactory)
    print('Connect db')


def insert_to_db():
    illust_list = [Pixiv(**result) for result in WHOLERESULT]
    SESSION.add_all(illust_list)
    SESSION.commit()


def main():
    start = settings.STARTNUMBER
    cache = settings.MAXCACHE

    while True:
        base_url = 'http://spapi.pixiv.net/iphone/illust.php?PHPSESSID=' + settings.PHPSESSID + '&illust_id='
        urls = [base_url + str(i) for i in range(start, start + cache)]
        loop = asyncio.get_event_loop()
        f = wait_with_progress([get_illust(url) for url in urls])
        print('Getting:', start, '-', start + cache)
        loop.run_until_complete(f)

        insert_to_db()

        global WHOLERESULT
        if not WHOLERESULT:
            print('Completed')
            break

        WHOLERESULT = deque()
        start += cache


WHOLERESULT = []
SEM = asyncio.Semaphore(settings.MAXCONNECTION)
CONN = aiohttp.TCPConnector()

if __name__ == '__main__':
    connect_db()
    main()