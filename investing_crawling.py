import requests as rq
import pandas as pd
import re
from datetime import datetime
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm

options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument('user-agent=Mozilla/5.0(Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
options.add_argument('lang=ko_KR')
driver=webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

ROOT = 'https://www.investing.com'
URL = ROOT + '/news/world-news'
Result = []

def crawling(page) :
    temp = []
    pat = re.compile('[\t\n\r\f\v]')

    driver.get(ROOT + page)
    html = driver.page_source
    s = bs(html, 'html.parser')
    contents = s.select('#leftColumn > div.WYSIWYG.articlePage > p')
    for i in contents :
        temp.append(re.sub(pat, '', i.text))

    temp = ' '.join(temp)

    return temp

def preparePageList() :    
    result = []
    driver.get(URL)
    html = driver.page_source
    s = bs(html, 'html.parser')    
    news_list = s.select('#paginationWrap > div.midDiv.inlineblock > a')
    for i in tqdm(news_list) :
        if i.text != '1' : 
            driver.get(ROOT + i.get('href'))
        post = s.select('#leftColumn > div.largeTitle > article > div.textDiv > a')
        for j in post :
            cont_page = j.get('href')
            title = j.text
            contents = crawling(cont_page)
            while contents == '' :
                contents = crawling(cont_page)
            data = {"Text" : contents, "url": cont_page, "Title" : title}
            result.append(data)

    return result
if __name__ == '__main__' :
    Result = preparePageList()

    pd.DataFrame(Result, columns=['Text', 'url','Title']).to_excel(f'result_investing' + datetime.today().strftime("%d%H%M") + ".xlsx")