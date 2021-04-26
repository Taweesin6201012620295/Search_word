from datetime import *
import unittest
import pandas as pd

class Search_Crawler():

    def search(self,keyword ,since ,until) :

        all_result = {}

        #- - - - - - - - - - - - เริ่มส่วนที่เเก้ - - - - - - - - - - - - - - - - - -
        day_list = []
        date_start = datetime.strptime(str(since) ,'%Y-%m-%d')
        date_end = datetime.strptime(str(until) ,'%Y-%m-%d')

        while int((date_end - date_start).days) >= 0 : 
            day_list.append("crawler_" + date_start.strftime('%Y-%m-%d') + "_.csv")
            date_start +=  timedelta(days = 1)
        print(day_list)
        first = True

        for news in day_list :
            try:
                read_data_file = pd.read_csv(news)

                head_news = read_data_file['head_news'].str.lower()
                head_keyword = read_data_file[head_news.str.contains(str(keyword), na=False)]

                if first :
                    for column in head_keyword :
                        all_result[column] = []
                    for column in head_keyword :
                        for data in head_keyword[column] :
                            all_result[column].append(data)
                    first = False
                else :
                    for column in head_keyword :
                        for data in head_keyword[column] :
                            all_result[column].append(data)
            except FileNotFoundError:
                pass
        
        
        df = pd.DataFrame(data = all_result)
        df.to_csv('C:\\Users\\Lenovo\\Desktop\\csv\\' + str(keyword)+'_crawler.csv',index = False,encoding='utf-8')
        print(df)
        return df

if __name__ == "__main__":

    class Unit_test(unittest.TestCase):
        def test_crawler(self):
            crawler = Search_Crawler()
            crawler.search('god','2021-04-26','2021-04-26')
            self.assertIsNotNone(crawler.search)
 
    unittest.main()