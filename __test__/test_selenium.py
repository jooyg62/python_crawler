import time

from selenium import webdriver

wd = webdriver.Chrome('D:\cafe24\dev\chromedriver.exe')
wd.get('http://www.google.com')

time.sleep(2)
html = wd.page_source
print(html)

wd.quit()

