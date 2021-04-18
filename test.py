def save_list_file(self, keyword):
        from datetime import datetime
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        headers = ["update_time",'file_name']
        file_name = 'file_list_keywords.csv'
        try:
            csvfile = open(file_name, 'r')
            reader = csv.reader(csvfile, delimiter=',') # Checkink NotFoundError 

            tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')
            writer_re = csv.DictWriter(tempfile, fieldnames=headers)
            writer_re.writeheader()

            #csvfile = open(file_name, 'a', newline='')
            #writer = csv.DictWriter(csvfile, fieldnames=headers)
            #2021-02-01 00:00:00
            
            first = 0
            #n = len([i for i in reader])
            n = []
            for row in reader:
                if(first > 0):
                    if(row[1] == 'keyword_'+str(keyword)+'_output.csv'):
                        writer_re.writerow( {'update_time':date_time, 'file_name':'keyword_'+str(keyword)+'_output.csv'} )
                    else:
                        writer_re.writerow( {'update_time':row[0], 'file_name':row[1]} )
                n.append(row[1])
                first += 1

            if('keyword_'+str(keyword)+'_output.csv' not in n):
                writer_re.writerow( {'update_time':date_time, 'file_name':'keyword_'+str(keyword)+'_output.csv'} )

            tempfile.close()
            csvfile.close()

            shutil.move(tempfile.name, file_name)
            #writer.writerow( {'update_time':date_time, 'file_name':'keyword_'+str(keyword)+'_output.csv'} )
        except FileNotFoundError:
            csvfile = open(file_name, 'w', newline='')
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            
            csvfile = open(file_name, 'a', newline='')
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writerow( {'update_time':date_time, 'file_name':'keyword_'+str(keyword)+'_output.csv'} )
            csvfile.close()