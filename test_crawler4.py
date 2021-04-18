import feedparser
from pprint import pprint
from bs4 import BeautifulSoup

web = 'https://www.bing.com/search?q={}&form=PRTHTH&httpsmsn=1&msnews=1&refig=7388bfda75a649f99f4a1f01e812e3d8'
url = web.format("covid")

class ParseFeed():

    def __init__(self, url):
        self.feed_url = url
        
    def clean(self, html):
        '''
        Get the text from html and do some cleaning
        '''
        soup = BeautifulSoup(html)
        text = soup.get_text()
        text = text.replace('\xa0', ' ')
        return text

    def parse(self):
        '''
        Parse the URL, and print all the details of the news 
        '''
        feeds = feedparser.parse(self.feed_url).entries
        for f in feeds:
            Description = self.clean(f.get("description", ""))
            Published_Date = f.get("published", "")
            Title = f.get("title", "")
            Url = f.get("link", "")
            article = (Title, Published_Date, Description, Url)
        print(feeds)

feed = ParseFeed(url)
feed.parse()