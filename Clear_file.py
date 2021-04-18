import csv
file_name = 'file_list_keywords.csv'
headers = ["update_time",'file_name']
csvfile = open(file_name, 'w', newline='')
writer = csv.DictWriter(csvfile, fieldnames=headers)
writer.writeheader()