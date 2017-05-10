#!/user/bin/python

import praw
import datetime
import unicodedata
import os.path
from os.path import dirname, abspath
import json
import sys
from io import StringIO

# this script takes 2 command line arguments:
#       1. the name of the subreddit to be looked at
#       2. the chosen title of the document(s) to be writen to
# all arguments must be enetered or the program will NOT run

def get_date(submission):
    time = submission.created
    date_created = datetime.date.fromtimestamp(time)
    return str(date_created)

reddit = praw.Reddit(client_id='z73mnLBFLFS1Jg',
                     client_secret='c5OtReBzJrCXIdKeB1pwXno-qT4',
                     password='Oracle1998',
                     user_agent='collects data for analysis by /u/azurerose98',
                     username='azurerose98')

if len(sys.argv) != 3:
    print('ERROR: INVALID ARGUMENTS')
    exit

subreddit_name = sys.argv[1].lower()
filename = sys.argv[2]

path1 = os.getcwd() + '/' + filename + '-Jan' + '.json'
path2 = os.getcwd() + '/' + filename + '-Dec' + '.json'
path3 = os.getcwd() + '/' + filename + '-Nov' + '.json'
datafile1 = open(path1,'w')
datafile2 = open(path2,'w')
datafile3 = open(path3,'w')

datafile1.truncate()
datafile2.truncate()
datafile3.truncate()

#for submission in reddit.subreddit('learnpython').hot(limit=10):
#    print(submission.title)

subreddit = reddit.subreddit(subreddit_name)

#print(subreddit.VALID_TIME_FILTERS)

json_data1 = []
json_data2 = []
json_data3 = []

LIMIT = 5000
DAY_LIMIT = 1
count = 0

day_count = {}

###

#for submission in subreddit.submissions():
#    for comment in submission.comments:
#        print(comment.body)

#exit()

###

for submission in subreddit.submissions():

    #print(submission.title)
    #print(submission.selftext)
    #print(get_date(submission))
    
    this_date = get_date(submission)
    date_partition = this_date.split('-')
    year = date_partition[0]
    month = date_partition[1]
    day = date_partition[2]

    if month == '02':
        pass
    else:

        if this_date not in day_count.keys():
            day_count[this_date] = 0
        else:
            pass
        
        if day_count[this_date] < DAY_LIMIT:
            
            day_count[this_date] += 1

            this_dict = {}

            print(this_date)

            this_title = submission.title
            this_text = submission.selftext

            this_dict['title'] = this_title
            this_dict['text'] = this_text
            this_dict['date'] = this_date

            comments = []
            
            for comment in submission.comments:

                #print(comment)

                #print(comment.body)
                #print(get_date(comment))
                
                this_text = comment.body
                this_date = get_date(comment)
                com_dict = {}

                com_dict['text'] = this_text
                com_dict['date'] = this_date

                #print(this_text)

                comments.append(com_dict)       

            this_dict['comments'] = comments

            print(comments)

            print(this_dict)

            if month == '01':
                
                #json_data1[count] = this_dict
                json_data1.append(this_dict)
                
            elif month == '12':
                
                #json_data2[count] = this_dict
                json_data2.append(this_dict)
                
            elif month == '11':
                
                #json_data3[count] = this_dict
                json_data3.append(this_dict)
                
            else:
                print('MONTH OUT OF RANGE')
                break
            
            count += 1
        
        else:
            pass

    #json1 = json.dumps(json_data1)
    #datafile1.write(json1)
    #json2 = json.dumps(json_data2)
    #datafile2.write(json2)
    #json3 = json.dumps(json_data3)
    #datafile3.write(json3)

    


json1 = {}
json2 = {}
json3 = {}

json1['collection_date'] = datetime.date
json2['collection_date'] = datetime.date
json3['collection_date'] = datetime.date

json1['collection_time'] = datetime.time
json2['collection_time'] = datetime.time
json3['collection_time'] = datetime.time

json1['content'] = json_data1
json2['content'] = json_data2
json3['content'] = json_data3    

json_1 = json.dumps(json1)
datafile1.write(json_1)
datafile1.close()
json_2 = json.dumps(json2)
datafile2.write(json_2)
datafile2.close()
json_3 = json.dumps(json3)
datafile3.write(json_3)
datafile3.close()
