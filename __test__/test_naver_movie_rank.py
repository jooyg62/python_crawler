from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from collection import crawler
from datetime import datetime


def ex01():
    request = Request('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
    response = urlopen(request)
    html = response.read().decode('cp949')
    # print(html)

    bs = BeautifulSoup(html, 'html.parser')
    # print(bs.prettify())

    divs = bs.findAll('div', attrs={'class': 'tit3'})
    # print(divs)
    for index, div in enumerate(divs):
        print(index+1, div.a.text, div.a['href'], sep=':')

    print('===============================================')


def proc_naver_movie_rank(html):
    # processing
    bs = BeautifulSoup(html, 'html.parser')
    divs = bs.findAll('div', attrs={'class': 'tit3'})

    return divs


def error():
    pass


def store_naver_movie_rank(data):
    # output(store)
    for index, div in enumerate(data):
        print(index + 1, div.a.text, div.a['href'], sep=':')


def ex02():
    # fetch
    crawler.crawling(
        url='https://movie.naver.com/movie/sdb/rank/rmovie.nhn',
        err=error,
        encoding='cp949',
        proc1=proc_naver_movie_rank,
        proc2=lambda data: list(map(lambda t: print(t[0], t[1].a.text, t[1].a['href'], sep=':'), enumerate(data)))
    )


__name__ == '__main__' and not\
    ex01() and not \
    ex02()


