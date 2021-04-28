import requests, bs4
import re, pandas, collections
import datetime, os, ast, operator, functools
from Twidty import Twidty 

class NewsCrawler(object):

	def __init__(self):
		self.list_news_links = [	"https://abcnews.go.com", # 0
									"https://apnews.com", # 1
									"https://bangkok-today.com", # 2
									"https://elitedaily.com", # 3
									"https://gawker.com", # 4
									"https://mashable.com", # 5
									"https://mgronline.com", # 6
									"https://mic.com", # 7
									"http://news.ch3thailand.com", # 8
									"https://news.ch7.com", # 9
									"https://news.google.com", # 10
									"https://news.microsoft.com", # 11
									"https://news.sky.com", # 12
									"https://news.yahoo.com", # 13
									"https://nypost.com", # 14
									"https://siamrath.co.th", # 15
									"https://stock.gapfocus.com", # 16
									"https://techcrunch.com", # 17
									"https://thestandard.co", # 18
									"https://thethaiger.com", # 19
									"https://time.com", # 20
									"https://tna.mcot.net", # 21
									"https://today.line.me", # 22
									"https://www.al.com", # 23
									"https://www.amarintv.com", # 24
									"https://www.bangkokbiznews.com", # 25
									"https://www.bangkokpost.com", # 26
									"https://www.banmuang.co.th", # 27
									"https://www.bbc.com", # 28
									"https://www.bloomberg.com", # 29
									"https://www.boston.com", # 30
									"https://www.bostonglobe.com", # 31
									"https://www.businessinsider.com", # 32
									"https://www.cbsnews.com", # 33
									"https://www.chiangmainews.co.th", # 34
									"https://www.chicagotribune.com", # 35
									"https://www.chron.com", # 36
									"https://www.cnbc.com", # 37
									"https://www.cnet.com", # 38
									"https://www.dailymail.co.uk", # 39
									"https://www.dailynews.co.th", # 40
									"https://www.efinancethai.com", # 41
									"https://www.engadget.com", # 42
									"https://www.forexfactory.com", # 43
									"https://www.foxnews.com", # 44
									"https://www.freep.com", # 45
									"https://www.huffpost.com", # 46
									"https://www.independent.co.uk", # 47
									"https://www.infoquest.co.th", # 48
									"https://www.intergold.co.th", # 49
									"https://www.investing.com", # 50
									"https://www.kaohoon.com", # 51
									"https://www.komchadluek.net", # 52
									"https://www.latimes.com", # 53
									"https://www.marketingoops.com", # 54
									"https://www.marketwatch.com", # 55
									"https://www.matichon.co.th", # 56
									"https://www.mirror.co.uk", # 57
									"https://www.mlive.com", # 58
									"https://www.mrlikestock.com", # 59
									"https://www.msn.com", # 60
									"https://www.naewna.com", #61 
									"https://www.nationthailand.com", # 62
									"https://www.nbcnews.com", # 63
									"https://www.nj.com", # 64
									"https://www.npr.org", # 65
									"https://www.nydailynews.com", # 66
									"https://www.nytimes.com", # 67
									"https://www.one31.net", # 68
									"https://www.posttoday.com", # 69
									"https://www.pptvhd36.com", # 70
									"https://www.prachachat.net", # 71
									"https://www.prd.go.th", # 72
									"https://www.reuters.com", # 73
									"https://www.ryt9.com", # 74
									"https://www.salon.com", # 75
									"https://www.sanook.com", # 76
									"https://www.set.or.th", # 77
									"https://www.settrade.com", # 78
									"https://www.sfgate.com", # 79
									"http://www.siamdara.com", # 80
									"https://www.slate.com", # 81
									"https://www.stock2morrow.com", # 82
									"https://www.telegraph.co.uk", # 83
									"https://www.thaipbs.or.th", # 84
									"https://www.thaipost.net", # 85
									"https://www.thairath.co.th", # 86
									"https://www.thansettakij.com", # 87
									"https://www.theatlantic.com", # 88
									"https://www.theblaze.com", # 89
									"https://www.thedailybeast.com", # 90
									"https://www.theguardian.com", # 91
									"https://www.thunhoon.com", # 92
									"https://www.tv5.co.th", # 93
									"https://www.upworthy.com", # 94
									"https://www.usatoday.com", # 95
									"https://www.vice.com", # 96
									"https://www.vox.com", # 97
									"https://www.washingtonpost.com", # 98
									"https://www.xinhuathai.com"	] #99

	def check_dup_text(self, text_list):
		# casting text list in set type
		text_list = set(text_list)
		# create empty set for contain seen text
		seen_text = set()
		# create empty list for give result
		result = []
		# access in text list @set type
		for item in text_list:
			# if this text item is not ever seen, so it has to give in result
			if item not in seen_text:
				seen_text.add(item)
				result.append(item)
		return result

	def find_main_headlines(self, url):
		# request data in url
		web_data = requests.get(url)
		# get html code from web_data
		soup = bs4.BeautifulSoup(web_data.content, 'html.parser')
		# find all <a> in html inspect
		all_a_tags = soup.find_all("a", href=True)
		# list for keeping all links in navigation bar
		nav_links = []
		# list for keeping all homepage links of url
		main_links = []
		# list for keeping all headlines news 
		main_headlines = []
		try:
			# access for getting links in navigation bar
			nav = soup.nav 
			# find all <a> in <nav>
			a_in_nav = nav.find_all("a", href=True)
			# saving <nav> href
			for a_nav in a_in_nav:
				# save in nav_links list()
				nav_links.append(a_nav['href'])
		except:
			pass
		# access in all of <a> that found
		for a_tag in all_a_tags:
			# limit homepage news only 100 headlines
			if len(main_links) == 100:
				break
			# assign href each of headlines
			news_link = a_tag['href']
			# checking [Is the href in navigation bar??]
			if news_link in nav_links:
				continue
			else:
				# some architecture of each website are diffrent
				# # some of them are has the url domain
				# # but the other haven't got, so they have sub link
				if url not in news_link:
					# adding domain of website in front of it
					news_link = url + news_link
				if news_link in main_links or a_tag.getText() == "" or a_tag.getText() in "\t\n ":
					continue
				else:
					# keeping link of homepage headlines
					main_links.append(news_link)
					# keeping text of headlines
					main_headlines.append(a_tag.getText())
		# return it in dict()
		return {"main_links":main_links, "main_headlines":main_headlines}

	def find_all_headlines(self, url):
		# use this method for find homepage headlines and sub page headlines
		main_news = self.find_main_headlines(url)
		# give main news links and main headlines content
		main_links = main_news['main_links']
		headlines = main_news['main_headlines']
		# print(headlines)
		# print(len(headlines))
		index_link = []
		# access every homepage links
		for link in main_links:
			# if len(index_link) == 500:
				# break
			check_link = main_links.index(link)
			if check_link in index_link:
				continue
			else:
				index_link.append(check_link)
				# print(check_link)
			try:
				# carry the sub headlines news
				sub_head_carry = self.find_main_headlines(link)
			except:
				continue
			# get all sub headlines text
			sub_headlines = sub_head_carry['main_headlines']
			# add all sub headlines in old headlines
			headlines += sub_headlines 
		# duplicate the same content of headlines
		result = self.check_dup_text(headlines)
		# return result values
		return result

	def get_freq_tokenize(self, str_of_list):
		# convert string list to list type
		list_tokenize = []
		# access all tokenize list
		for a_list in str_of_list:
			# summation all string list and casting in list
			list_tokenize.extend(ast.literal_eval(a_list))
		# count tokenize word
		collect_tokenize = dict(collections.Counter(list_tokenize))
		# key is the tokenize word
		key = list(collect_tokenize.keys())
		# all punctuations in sentences
		punctuations = '''[!()-[]{}:;'\",<>./?@$%^&*_~ๆ“”‘’|]฿—'''
		try:
			for key in keys:
				# if key is punctuation pop it from dict()
				if key in punctuations:
					collect_tokenize.pop(key)
			# try to pop space bar
			collect_tokenize.pop(' ')
			collect_tokenize.pop('\u200b')
		except:
			pass
		return collect_tokenize

	def update_data(self, website):
		twidty = Twidty()
		# create new data frame for store data
		df = pandas.DataFrame(columns=['Date', 'Text', 'Tokenize', 'Sentiment'])
		# set Date column in each row to TODAY date
		datetime_now = datetime.datetime.now() # date + time
		# casting datetime to string and give only date (day, month, year)
		date_now = str(datetime_now.date())
		# use regex for give host name from url
		dir_name = re.search('https?://([A-Za-z_0-9.-]+).*', website)
		if dir_name:
			dir_name = dir_name.group(1)
		# use host name to save new folder
		path = r"D:\vs code\soft_dev_2\midterm_pro\data\crawler"
		path_all_date = path + r"\{}".format(dir_name)
		# check is this new website ??
		all_data = os.listdir(path)
		if dir_name not in all_data:
			print("New Website")
			os.mkdir(path_all_date)
		# check if it has todaynews
		all_date = os.listdir(path_all_date)
		# if today's news have already >> tell user
		if date_now + '.csv' in all_date:
			print("Today's news are ready!!!")
			return False
		else:
			# request to the url website that you want to crawler
			news_headlines = self.find_all_headlines(website)
			print("*****{}--{}*****".format(website, len(news_headlines)))
			# access all headlines for tokenizing sentences and save to_csv data
			for headline in news_headlines:
				# print(news_headlines.index(headline))
				# intercept all punctuation, enter, tab, mention, hashtag and web in text content
				text_intercept = twidty.text_intercept(headline)
				text_intercept = " ".join(text_intercept.split())
				# tokenize headline for analyzing word nearby keyword when searching
				text_tokenize = twidty.nlp(text_intercept, '')
				# try to give sentiment emotion in headline
				try:
					text_sentiment = twidty.sentiment(headline)
				except:
					# if it cannot analysis sentiment, pass it away and do next
					continue
				# get all data in pandas row (series data)
				data_row = pandas.Series([date_now, 
										text_intercept, 
										str(text_tokenize), 
										text_sentiment], index=df.columns)
				# append data row to data frame
				df = df.append(data_row, ignore_index=True)
			# get all tokenize string list text
			all_tokenize = df['Tokenize']
			# counting keyword which it is tokenize word
			counter_word = self.get_freq_tokenize(all_tokenize)
			# make data frame that save only keyword (word tokenize) and their frequencies
			freq_df = pandas.DataFrame(columns=['Keywords', 'Frequencies', 'Sentiment'])
			# access all items in counter_word
			for item in counter_word:
				# key of item
				key = item
				try: 
					# search key in Text column
					relate_df = df[df['Text'].str.contains(key)]
				except:
					continue
				# calculate for including sentiment of keyword
				keyword_sentiment = dict(collections.Counter(relate_df['Sentiment']))
				# check what all of sentiments are in dict(keyword_sentiment)
				sentiment_keys = keyword_sentiment.keys()
				# if its 'neutral' is 0 
				if 'neutral' not in sentiment_keys:
					# dict adding key => 'neutral' and value => 0
					keyword_sentiment['neutral'] = 0
				# if its 'positive' is 0
				if 'positive' not in sentiment_keys:
					# dict adding key => 'positive' and value = 0
					keyword_sentiment['positive'] = 0
				# if its 'negative' is 0
				if 'nagative' not in sentiment_keys:
					keyword_sentiment['negative'] = 0
				# values of item
				freq = counter_word[item]
				# keep in series row for saving in csv file
				freq_row = pandas.Series([key.lower(), freq, keyword_sentiment], index=freq_df.columns)
				# append freq_row in freq_df for save csv
				freq_df = freq_df.append(freq_row, ignore_index=True)
			# save healine today
			freq_df.to_csv(path_all_date + r'\{}.csv'.format(date_now))
		print("{}\t\tComplete Update!!!".format(website))

	def search(self, keyword, start, stop):
		twidty = Twidty()
		# change start (string) date in date object
		start_d = datetime.datetime.strptime(start, '%Y-%m-%d')
		# change stop (string) date in date object
		stop_d = datetime.datetime.strptime(stop, '%Y-%m-%d')
		# setting step next day is adding 1 day
		step_d = datetime.timedelta(days=1)
		# setting list for dict() of website : number of keywords that searching in website
		result = {}
		# list of dict for containing result of sentiment of keyword
		result_sent = []
		# path of database
		path_crawler = r"D:\vs code\soft_dev_2\midterm_pro\data\crawler"
		# acceess all website folder
		all_folder = os.listdir(path_crawler)
		# print(all_folder)
		# access earch website folder and give result for plotting graph
		for web in all_folder:
			# print(web)
			# list for containing frequencies keyword start to stop day
			freq_carry = []
			# give range of date# 
			while start_d <= stop_d:
				# keeping data
				try:
					# read dataframe for keeping result
					read_df = pandas.read_csv(path_crawler + r"\{}".format(web) + r"\{}.csv".format(str(start_d.date())))
					# search keyword from database
					search_keyword = read_df[read_df['Keywords'].str.match(keyword)]
					# get frequencies of keyword
					freq_word = search_keyword['Frequencies']
					# get sentiment of keyword
					sent_word = search_keyword['Sentiment']
					# get value of freqencies list type
					freq = freq_word.values
					# append value in list() freq to freq_carry
					freq_carry.append(freq[0])
					# get values of sentiments list of dict type
					sent = sent_word.values
					# append values in string of dict to result_sent list
					result_sent.append(ast.literal_eval(sent[0]))
					# find keyword in next day find
					start_d += step_d
				except:
					# if it doesn't have keyword search next day
					start_d += step_d
			# summation the frequencies of keyword
			sum_freq = sum(freq_carry)
			# if it doesn't have keyword in this website, go to next website
			if sum_freq == 0:
				result[web] = 0
			else:
				# saving data in result dict for showing in graph
				result[web] = sum_freq
			# setting defualt of start day to search
			start_d = datetime.datetime.strptime(start, '%Y-%m-%d')
		try:
			# summation of positive, neutral and negative
			sentiment_result = dict(functools.reduce(operator.add, map(collections.Counter, result_sent)))
		except:
			# this case for detecting non keyword in database
			sentiment_result = {'positive':0, 'neutral':0, 'negative':0}
		# # print(result)
		# # print(sentiment_result)
		# make top 5 ranking result of keyword
		result_ranking = dict(sorted(result.items(), key=operator.itemgetter(1), 
										reverse=True)[:5])
		# # print(result_ranking)
		return {"related_words":result_ranking, "sentiment":sentiment_result}


'''
news_crawler = NewsCrawler()
list_web = news_crawler.list_news_links
news_crawler.update_data(list_web[0])
'''
'''
news_crawler = NewsCrawler()
print(news_crawler.search("โควิด", "2021-03-28", "2021-04-10"))
'''
'''
news_crawler = NewsCrawler()
news_crawler.update_data(news_crawler.list_news_links[97])
'''