# refference https://www.youtube.com/watch?v=hMxFnVVYGDk&ab_channel=IzzyAnalytics
import re
import csv
from time import sleep
from datetime import*
from bs4 import BeautifulSoup
import requests

class Search_thai_Crawler:
    def __init__(self):
        pass

    def get_thai_article(self,page):
        Headline = page.find('span', 'jsx-2430232205 jsx-180597169 text-color-news').text
        Link = page.find('a').get('href')
        Posted = page.find('time').get('datetime')
        Description = page.find('p', 'jsx-2430232205 jsx-180597169 description').text

        article = (Headline,Posted,Description,Link)
        return article

    def get_thai_news(self,search):

        web = 'https://www.sanook.com/news/search/{}/'
        url = web.format(search)

        articles = []
        links = set()
        while True:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            pages = soup.find_all('div','jsx-4244751374')

            for p in pages:
                article = self.get_thai_article(p)
                link = article[-1]
                if not link in links:
                    links.add(link)
                    articles.append(article)
            # find the next page
            try:
                url = soup.find('div', 'gsc-cursor-page').get('href')
                sleep(1)
            except AttributeError:
                break
        
        with open(str(search)+'_crawler.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Headline','Posted','Description','Link'])
            writer.writerows(articles)

if __name__ == "__main__":
    crawler = Search_thai_Crawler()
    crawler.get_thai_news(str(input()))