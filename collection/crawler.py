import sys
from datetime import datetime
import ssl
from urllib.request import Request, urlopen

import pandas as pd
from bs4 import BeautifulSoup

def crawling(
        url='',
        encoding='utf-8',
        err=lambda e: print(f'{e} : {datetime.now()}', file=sys.stderr),
        proc1=lambda data: data,
        proc2=lambda data: data):
    try:
        request = Request(url)

        ssl._create_default_https_context = ssl._create_unverified_context
        response = urlopen(request)

        receive = response.read()

        return proc2(proc1(receive.decode(encoding, errors='replace')))

    except Exception as e:
        err(e)

