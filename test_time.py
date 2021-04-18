import csv
import pandas as pd

day_1,day_2 = '16','18'
month1,month2 = '04', '08'
year1, year2 = '2021', '2021'
    
pan = pd.read_csv('โควิด19_Data.csv',error_bad_lines=False)
if len(day_1) == 1:
    day_1 = '0' + day_1
if len(day_2) == 1:
    day_2 = '0' + day_2
if len(month1) == 1: 
    month1 = '0' + month1
if len(month2) == 1:
    month2 = '0' + month2

colume1 = pan['time'] >= f'{year1}-{month1}-{day_1} 00:00:00'
colume2 = pan['time'] <= f'{year2}-{month2}-{day_2} 23:59:59'
between = colume1 & colume2
print(between.sort_values(by="time")['time'])