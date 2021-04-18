# https://www.borntodev.com/2020/04/07/%E0%B8%A1%E0%B8%B2%E0%B8%97%E0%B8%B3-unit-testing-%E0%B8%9A%E0%B8%99-python-%E0%B8%81%E0%B8%B1%E0%B8%99/
# https://docs.python.org/3/library/unittest.html#unittest.TestCase

import unittest
import pandas as pd
import csv
from API import *
from Crawler_file1 import *
from NLP import *

class Unit_test(unittest.TestCase):
    def test_search(self):
        self.API = Twitter_API("คลองสุเอซ","th","2021-03-25","2021-04-01")
        self.assertIsNotNone(self.API.search())

'''
class Calculator():
    def add_num(self):
        pan = pd.read_csv("covid" + "_Data.csv")
        return pan

class TestNumber(unittest.TestCase):
    def test(self):
        pan1 = pd.read_csv("dek64" + "_Data.csv")
        self.assertIsNotNone(pan1)

    def test_hello_world(self):
        myCal = Calculator()
        self.assertIsNotNone(myCal.add_num())
'''
if __name__ == '__main__':
   unittest.main()