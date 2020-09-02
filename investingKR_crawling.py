import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager 
from tqdm import tqdm
from datetime import datetime

options = webdriver.ChromeOptions()
#options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
options.add_argument('user-agent=Mozilla/5.0(Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
options.add_argument('lang=ko_KR')
driver=webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

ROOT = 'https://kr.investing.com'
URL = ROOT + '/news/economy'
df = pd.DataFrame(data = {"url" : [], "contents" : []})
data_list = []

def Crawling(page_url) :
    POSTLIST = []
    driver.get(ROOT + page_url)
    html = driver.page_source
    s = bs(html, 'html.parser')
    post_list = s.select('#leftColumn > div.largeTitle > article > a')
    for post in post_list :
        POSTLIST.append(post.get('href'))

    for post in POSTLIST :
        articleText = []
        driver.get(ROOT + post)
        html = driver.page_source
        s = bs(html, 'html.parser')
        contents = s.select('#leftColumn > div.WYSIWYG.articlePage > p')
        for i in contents : 
            i = remove_whitespace(i)
            articleText.append(i)
        # contents = contents.text()
        # contents = remove_whitespace(contents)
        data = {"url" : ROOT + post, "contents" : articleText}
        data_list.append(data)

def craw_page_list() :
    driver.get(URL)
    html = driver.page_source
    s = bs(html, 'html.parser')
    page_link = s.select("#paginationWrap > div.midDiv.inlineblock > a")
    for i in tqdm(page_link, desc="running") :
        if i.text == '1' : 
            continue
        Crawling(i.get('href'))


def remove_whitespace(text) :
    pat = re.compile('<.*>')
    return re.sub(pat, '', str(text))

if __name__ =='__main__' : 
    Crawling('/news/economy')
    craw_page_list()
    Result = pd.DataFrame(data_list, columns=['url', 'contents'])
    Result.to_excel("result_investingKR" + str(datetime.today().strftime("%d%H%M"))+ ".xlsx", index=False) 
    driver.close()