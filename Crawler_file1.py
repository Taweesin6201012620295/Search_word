# refference https://www.youtube.com/watch?v=hMxFnVVYGDk&ab_channel=IzzyAnalytics
import re
import csv
from time import sleep
from datetime import*
from bs4 import BeautifulSoup
import requests

class Search_Crawler:
    def __init__(self):
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://www.google.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
        }

    def get_article(self,card):
        try:
            #Extract article information from the raw html
            headline = card.find('h4', 's-title').text
            source = card.find("span", 's-source').text
            posted = card.find('span', 's-time').text.replace('·', '').strip()
            description = card.find('p', 's-desc').text.strip()
            raw_link = card.find('a').get('href')
            unquoted_link = requests.utils.unquote(raw_link)
            pattern = re.compile(r'RU=(.+)\/RK')
            
            clean_link = re.search(pattern, unquoted_link).group(1)
            
            article = (headline, source, posted, description, clean_link)
        except AttributeError:
            article = (headline, source, posted, description, unquoted_link)
        return article

    def get_the_news(self,search):
        #Run the main program
        template = 'https://news.search.yahoo.com/search?p={}'
        url = template.format(search)
        articles = []
        links = set()
        start = datetime.now()

        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', 'NewsArticle')
            
            
        # extract articles from page
        for card in cards:
            article = self.get_article(card)
            link = article[-1]
            if not link in links:
                links.add(link)
                articles.append(article)

        # save article data
        finish = datetime.now()
        diff = finish-start
        print(diff)
        with open(str(search)+'_crawler.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Headline', 'Source', 'Posted', 'Description', 'Link'])
            writer.writerows(articles)
        return articles


if __name__ == "__main__":
    crawler = Search_Crawler()
    crawler.get_the_news(str(input()))