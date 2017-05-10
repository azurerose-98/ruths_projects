#!/user/bin/python

import requests
import urllib.request
import praw
import json
from io import StringIO
import string
import os.path
from os.path import dirname, abspath
from decimal import *
import operator
import unicodedata
import math

reddit = praw.Reddit(client_id='z73mnLBFLFS1Jg',
                     client_secret='c5OtReBzJrCXIdKeB1pwXno-qT4',
                     password='Oracle1998',
                     user_agent='collects data for analysis by /u/azurerose98',
                     username='azurerose98')

jfile = "/AnimeData.json"
path = os.getcwd() + jfile
datafile = open(path,'w')

datafile.truncate()

count = 0
POST_COUNT = 1000
after = ''
data_dict = {}

hdr = {'User-Agent': 'collects data for analysis by /u/azurerose98'}
url = 'https://www.reddit.com/r/anime/.json'
req = urllib.request.Request(url, headers=hdr)
text_data = urllib.request.urlopen(req).read()
data = json.loads(text_data)
data_dict[count] = data

while count < POST_COUNT and after != None:

    count+=25
    after = data['data']['after']
    if after != None:
        add = '?count=' + str(count) + '&after=' + after
        new_url = url + add
        req = urllib.request.Request(new_url, headers=hdr)
        text_data = urllib.request.urlopen(req).read()
        data_dict[count] = data
        
json.dump(data_dict, datafile)
datafile.close()
print( count )
