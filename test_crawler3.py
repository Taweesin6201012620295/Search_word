import csv
import feedparser
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import datetime

# ใช้ได้
class ParseFeed():
    def __init__(self):
        self.headers = ['Headline', 'Posted', 'Description', 'Link']
        self.file_name = 'google.csv'
        
    def clean(self, html):
        '''
        Get the text from html and do some cleaning
        '''
        soup = BeautifulSoup(html)
        text = soup.get_text()
        text = text.replace('\xa0', ' ')

        return text
    
    def get_time(self,date):
        date = date.split(" ")
        day = date[1]
        month = date[2]
        year = date[3]
        time = date[4]
        Published_Date = str(year) + '-' + str(month) + '-'+ str(day) +' '+ str(time)
        date_time_obj = datetime.strptime(Published_Date, '%Y-%b-%d %H:%M:%S')
        return date_time_obj

    def get_article(self,f):
        Description = self.clean(f.get("description", ""))
        Published_Date = self.get_time(f.get("published", ""))
        Title = f.get("title", "")
        Url = f.get("link", "")
        article = (Title, Published_Date, Description, Url)
        return article

    def parse(self,search):
        '''
        Parse the URL, and print all the details of the news 
        '''
        try:
            template = "http://news.google.com/news?q={}-19&hl=en-US&sort=date&gl=US&num=100&output=rss"
            self.url = template.format(search)
            feeds = feedparser.parse(self.url).entries
            csvfile = open(self.file_name, 'r', newline='')
            csvfile = open(self.file_name, 'a', newline='')
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            for f in feeds:
                article = self.get_article(f)
                writer.writerow( {'Headline':article[0], 'Posted':article[1], 'Description':article[2], 'Link':article[3]} )
            csvfile.close()

        except FileNotFoundError:
            template = "http://news.google.com/news?q={}-19&hl=en-US&sort=date&gl=US&num=100&output=rss"
            self.url = template.format(search)
            feeds = feedparser.parse(self.url).entries
            csvfile = open(self.file_name, 'w', newline='')
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            writer.writeheader()
            for f in feeds:
                article = self.get_article(f)
                writer.writerow( {'Headline':article[0], 'Posted':article[1], 'Description':article[2], 'Link':article[3]} )
            csvfile.close()

if __name__ == "__main__":  
    feed = ParseFeed()
    feed.parse(str(input()))

'''# refference https://www.youtube.com/watch?v=hMxFnVVYGDk&ab_channel=IzzyAnalytics
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

    def get_eng_news(self,search):
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
    crawler.get_eng_news(str(input()))'''