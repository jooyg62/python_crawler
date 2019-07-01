import bs4

html = '''<td class="title black">
<div class="tit3">
<a href="/movie/bi/mi/basic.nhn?code=161967" title="기생충" />
</div>
</td>'''

# 1. tag 조회
def ex1():
    bs = bs4.BeautifulSoup(html, 'html.parser')
    # print(bs)
    # print(type(bs))

    tag = bs.td
    # print(tag)
    # print(type(tag))

    tag = bs.a
    print(tag)
    print(type(tag))

    tag = bs.td.div.h4
    print(tag)
    print(type(tag))

# 2. attribute 값 가져오기
def ex2():
    bs = bs4.BeautifulSoup(html, 'html.parser')

    tag = bs.td
    print(tag['class'])

    tag = bs.div
    # 에러
    # print(tag['id'])
    print(tag.attrs)

#3. attribute로 태그 조회하기
def ex3():
    bs = bs4.BeautifulSoup(html, 'html.parser')

    tag = bs.find('td', attrs={'class': 'title'})
    print(tag)
    print(type(tag))



if __name__ == '__main__':
    # ex1()
    # ex2()
    ex3()