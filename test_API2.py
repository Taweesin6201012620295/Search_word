import re
import csv
from time import sleep
from datetime import*
from bs4 import BeautifulSoup
import requests

template = 'https://tna.mcot.net/?s={}'
url = template.format('โควิด')
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
cards = soup.find_all('div','s-grid')
print(cards)
print(len(cards))
articles = []
links = set()

'''def get_article(card):
    #Extract article information from the raw html
    headline = card.find('h2','entry-title').text
    #posted = card.find('span', 's-time').text.replace('·', '').strip()
    #description = card.find('p', 's-desc').text.strip()
    raw_link = card.find('a').get('href')
    unquoted_link = requests.utils.unquote(raw_link)
    #pattern = re.compile(r'RU=(.+)\/RK')
    #clean_link = re.search(pattern, unquoted_link).group(1)
        
    article = (headline, unquoted_link)
    return article


for card in cards:
    article = get_article(card)
    link = article[-1]
    if not link in links:
        links.add(link)
        articles.append(article)
print(articles)'''

##########################################################################################
'''template = 'https://news.search.yahoo.com/search?p={}'
url = template.format('covid')
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
cards = soup.find_all('div','NewsArticle')
print(cards)
print(len(cards))

for card in cards:
    print(card.find('h4', 's-title').text)'''