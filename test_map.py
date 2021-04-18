import csv
import pandas as pd

pos = '13'
neg = '2'
neu = '0'
with open('sentiment.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['pos','neg','neu'])
    writer.writerow([pos,neg,neu])

pan = pd.read_csv('sentiment.csv')
print (pan['pos'])