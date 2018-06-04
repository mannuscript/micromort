from micromort.data_stores.mysql_connection import db, cursor
import sys

def insertUrl(url, tweet_id):
    try:
    	url = url.strip()
        cursor.execute("""INSERT IGNORE INTO newsTweetid_Url(url, tweet_id) values(%s, %s)""", 
                   [url, long(tweet_id)])
    except Exception as e:
        print(e)


#file = sys.argv[1]
#with open('/home/mannu/Setup/micromort/' + file, 'r') as fp:
#     read_lines = fp.readlines()
#     for line in read_lines:
#         insertUrl(line.strip())
        
file = sys.argv[1]
with open('/home/mannu/code/work/micromort/urls/' + file, 'r') as fp:
     read_lines = fp.readlines()
     for line in read_lines:
	try:
        	insertUrl(line.split()[1], line.split()[0])
	except Exception as e:
		print(e)
		continue

