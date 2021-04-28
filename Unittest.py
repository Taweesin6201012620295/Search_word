# https://www.borntodev.com/2020/04/07/%E0%B8%A1%E0%B8%B2%E0%B8%97%E0%B8%B3-unit-testing-%E0%B8%9A%E0%B8%99-python-%E0%B8%81%E0%B8%B1%E0%B8%99/

import Unittest
from API import*

class API_test(unittest.TestCase):
    def test_API(self):
        obj = Twitter_API("covid","en","2021-04-26","2021-04-27")
        obj.search()
        self.assertIsNotNone(obj)

class NLP_test(unittest.TestCase):
    def test_NLP(self):
        
class Crawler_test(self):
    def test_crawler(self):


if __name__ == "__main__":
    unittest.main()