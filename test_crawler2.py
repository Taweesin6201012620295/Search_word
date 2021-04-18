# refference https://www.youtube.com/watch?v=hMxFnVVYGDk&ab_channel=IzzyAnalytics
import re
import csv
from time import sleep
from datetime import*
from bs4 import BeautifulSoup
import requests

'''class Search_thai_Crawler:
    def __init__(self):
        pass

    def get_thai_article(self,page):
        headline = page.find('span', 'jsx-2430232205 jsx-180597169 text-color-news').text  #กรองเอาเฉพาะข้อความที่ต้องการ
        link = page.find('a').get('href') #link
        time = page.find('time').get('datetime')  #date
        cont = page.find('p', 'jsx-2430232205 jsx-180597169 description').text #content

        article = (headline,time,cont,link)
        return article

    def get_thai_news(self,search):
        
        web = 'https://www.sanook.com/news/search/{}/'
        url = web.format(search)

        articles = []
        links = set()

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        pages = soup.find_all('div','jsx-4244751374')

        # extract articles from page
        for p in pages:
            article = self.get_thai_article(p) #เข้าถึงข้อมูล และclean ข้อมูล html
            link = article[-1]
            if not link in links:
                links.add(link)
                articles.append(article)
        
        with open(str(search)+'_crawler.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Headline','Posted','Link','Description'])
            writer.writerows(articles)

if __name__ == "__main__":
    crawler = Search_thai_Crawler()
    crawler.get_thai_news(str(input()))'''
'''self.URL_th = ["https://www.sanook.com/news/",
                        "https://thestandard.co/homepage/",
                        "https://www.thairath.co.th/",
                        "https://www.bangkokbiznews.com/",
                        "https://thestandard.co/wealth/",
                        "https://www.posttoday.com/"]'''

web = 'https://www.thairath.co.th/search/{}' # css-nsf6k6 e2foe9c8
web = 'https://www.mcot.net/search?title={}' # category-container clearfix
web = 'https://news.thaipbs.or.th/search?q={}tab=news&time=last_month' #news-content-list
web = 'https://www.thaipost.net/main/search?keyword={}'#col-md-8 col-xs-12
web = 'https://www.sanook.com/news/search/{}/' #jsx-4244751374
web = 'https://search.posttoday.com/search/result?category=all&q={}' #('ul','SearchList')
web = 'https://thestandard.co/?s={}&search=' # newsbox-archive
web = "http://news.google.com/news?q={}-19&hl=en-US&sort=date&gl=US&num=100&output=rss"
web = 'https://www.bing.com/search?q={}&form=PRTHTH&httpsmsn=1&msnews=1&refig=7388bfda75a649f99f4a1f01e812e3d8'
web = 'https://news.search.yahoo.com/search?p={}'
web = 'https://www.khaosod.co.th/search?s={}'

url = web.format("โควิด")
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
div = soup.find_all('div')
a = soup.find_all('a')
li = soup.find_all('li')
ol = soup.find_all('ol')

print(div)