import re
import csv
import unittest
import feedparser
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import datetime


class Search_Crawler():

    def check_lan(self,lang): #Check Language
        if re.match('[ก-๙]',lang) != None:
            th = Search_thai_Crawler()
            th.get_thai_news(lang)
            en = " "
        else:
            en = Search_en_Crawler()
            en.get_eng_news(lang)
            th = " "
        return th,en

class Search_en_Crawler(): #Search English word
    def __init__(self):
        pass
        
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

    def get_eng_news(self,search):
        '''
        Parse the URL, and print all the details of the news 
        '''
        self.headers = ['Headline', 'Posted', 'Description', 'Link']
        self.file_name = str(search)+'_crawler.csv'
        try:
            template = "http://news.google.com/news?q={}-19&hl=en-US&sort=date&gl=US&num=100&output=rss"
            self.url = template.format(search)
            feeds = feedparser.parse(self.url).entries
            csvfile = open(self.file_name, 'r', newline='', encoding='utf-8')
            csvfile = open(self.file_name, 'a', newline='', encoding='utf-8')
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            for f in feeds:
                article = self.get_article(f)
                writer.writerow( {'Headline':article[0], 'Posted':article[1], 'Description':article[2], 'Link':article[3]} )
            csvfile.close()

        except FileNotFoundError:
            template = "http://news.google.com/news?q={}-19&hl=en-US&sort=date&gl=US&num=100&output=rss"
            self.url = template.format(search)
            feeds = feedparser.parse(self.url).entries
            csvfile = open(self.file_name, 'w', newline='', encoding='utf-8')
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            writer.writeheader()
            for f in feeds:
                article = self.get_article(f)
                writer.writerow( {'Headline':article[0], 'Posted':article[1], 'Description':article[2], 'Link':article[3]} )
            csvfile.close()

class Search_thai_Crawler: #Search thai Wrod
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

    class Unit_test(unittest.TestCase):
        def test_crawler(self):
            test = Search_Crawler()
            test.check_lan("God")
            self.assertIsNotNone(test)
 
    unittest.main()