import os
import sys
import time
from datetime import datetime
from urllib.request import Request, urlopen
from itertools import count

# import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler


def crawling_pelicana():
    results = []

    for page in count(start=1):
        url = 'https://pelicana.co.kr/store/stroe_search.html?gu=&si=&page=%d' % page
        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class', 'table mt20'})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split()[:2]
            t = (name, address) + tuple(sidogu)
            results.append(t)

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gubun'])
    # table.to_csv('__results__/pelicana.csv', encoding='utf-8', mode='w', index=True)


def crawling_nene():
    results = []

    for page in range(1, 3):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d' % page
        try:
            request = Request(url)

            # ssl._create_default_https_context = ssl._create_unverified_context
            response = urlopen(request)

            receive = response.read()
            html = receive.decode('utf-8', errors='replace')

            print(f'{datetime.now()}: success for request [{url}]')
        except Exception as e:
            print(f'{e} : {datetime.now()}', file=sys.stderr)
            continue

        bs = BeautifulSoup(html, 'html.parser')
        tags_div = bs.findAll('div', attrs={'class', 'shopInfo'})

        for tag_div in tags_div:
            shop_name = str(tag_div.find('div', attrs={'class', 'shopName'}).string)
            shop_add = str(tag_div.find('div',  attrs={'class', 'shopAdd'}).string)
            sidogu = shop_add.split()[1:3]
            t = (shop_name, shop_add) + tuple(sidogu)
            results.append(t)

        # 끝 검출
        tag_pagination = bs.find('div', attrs={'class', 'pagination'})
        tags_ahref = tag_pagination.findAll('a')
        if tags_ahref[-1]['href'] == '#':
            break

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gubun'])

    # os.path.dirname: 상위 디렉토리
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # table.to_csv('/root/crawling_results/nene.csv', encoding='utf-8', mode='w', index=True)


def crawling_kyochon():
    results = []
    for sido1 in range(1, 18):
        for sido2 in range(1, 27):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d' % (sido1, sido2)
            html = crawler.crawling(url)

            # 끝 검출
            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})
            tags_span = tag_ul.findAll('span', attrs={'class': 'store_item'})

            for tag_span in tags_span:
                strings = list(tag_span.strings)

                name = strings[1]
                address = strings[3].strip('\r\n\t')
                sidogu = address.split()[:2]

                results.append((name, address) + tuple(sidogu))

    for t in results:
        print(t)

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gubun'])
    # table.to_csv('__results__/kyochon.csv', encoding='utf-8', mode='w', index=True)


def crawling_goobne():
    results = []
    url = 'http://goobne.co.kr/store/search_store.jsp'

    # 첫 페이지 로딩
    wd = webdriver.Chrome('D:\cafe24\dev\chromedriver.exe')
    wd.get(url)
    time.sleep(5)

    for page in count(1):
        # 자바스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now()}: success for request [{script}]')
        time.sleep(3)

        # 실행결과 HTML(동적으로 렌더링 된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # detect last page
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name, address) + tuple(sidogu))

    wd.quit()
    for result in results:
        print(result)

    # store
    # table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gubun'])
    # table.to_csv('__results__/goobne.csv', encoding='utf-8', mode='w', index=True)


if __name__ == '__main__':
    # pelicana
    # crawling_pelicana()

    # nene 과제
    crawling_nene()

    # kyochon
    # crawling_kyochon()

    # kyochon
    # crawling_goobne()
