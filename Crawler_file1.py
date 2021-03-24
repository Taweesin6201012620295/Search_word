import csv
import feedparser
from pprint import pprint
from bs4 import BeautifulSoup
from datetime import datetime

# ใช้ได้
class Search_Crawler():
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

if __name__ == "__main__":  
    feed = Search_Crawler()
    feed.get_eng_news(str(input()))