# https://www.borntodev.com/2020/04/07/%E0%B8%A1%E0%B8%B2%E0%B8%97%E0%B8%B3-unit-testing-%E0%B8%9A%E0%B8%99-python-%E0%B8%81%E0%B8%B1%E0%B8%99/

import Unittest
from API import*
from NLP import*
from Crawler_file1 import*

from Gui_API import*
from GUI_Crawler import*
from GUI_Finance import*

class API_test(unittest.TestCase):
    def test_API(self):
        api = Twitter_API("covid","en","2021-04-26","2021-04-27")
        #api.search()
        #self.assertIsNotNone(api)

class NLP_test(unittest.TestCase):
    def test_NLP(self):
        nlp = NLP('โควิด19','api')
        nlp.save_analysis('th','โควิด19','api')
        self.assertIsNotNone(nlp)

class Crawler_test(unittest.TestCase):
    def test_crawler(self):
        crawler = Search_Crawler()
        crawler.search('god','2021-04-26','2021-04-28')
        self.assertIsNotNone(crawler.search)



if __name__ == "__main__":
    unittest.main()