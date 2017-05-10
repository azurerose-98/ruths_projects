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

hdr = {'User-Agent': 'collects data for analysis by /u/azurerose98'}
url = 'https://www.reddit.com/r/anime/top/.json'
req = urllib.request.Request(url, headers=hdr)
text_data = urllib.request.urlopen(req).read()
data = json.loads(text_data)
list_data = data['data']['children']

count = 25
after = data['data']['after']

add = '?count=' + str(count) + '&after=' + after

x = 0
while( x < len(list_data) ):
    print( list_data[x]['data']['title'])
    x+=1

new_url = url + add
req = urllib.request.Request(new_url, headers=hdr)
text_data = urllib.request.urlopen(req).read()
data = json.loads(text_data)
list_data = data['data']['children']

x = 0
while( x < len(list_data) ):
    print( list_data[x]['data']['title'])
    x+=1
