#!/user/bin/python

import json
from io import StringIO
import os
from os.path import dirname, abspath
import string
import sys
import unicodedata
import math

def main():

    Class = sys.argv[1]
    os.mkdir(Class)

    filename1 = Class + '-Nov'
    filename2 = Class + '-Dec'
    filename3 = Class + '-Jan'

    jsonfile1 = '/' + filename1 + '.json'
    path1 = os.getcwd() + jsonfile1 
    jsonfile2 = '/' + filename2 + '.json'
    path2 = os.getcwd() + jsonfile2
    jsonfile3 = '/' + filename3 + '.json'
    path3 = os.getcwd() + jsonfile3

    json_file1 = open(path1,'r+').read()
    rawdata1 = json.loads(json_file1)
    json_file2 = open(path2,'r+').read()
    rawdata2 = json.loads(json_file2)
    json_file3 = open(path3,'r+').read()
    rawdata3 = json.loads(json_file3)

    text1 = ''
    for obj in rawdata1:
        
        if obj.has_key('title')
            title = obj['title']
        else:
            title = ''
        text = obj['text']
        
        full_text = text + ' ' + title
        full_text = full_text.encode('ascii','ignore')

        text1 = text1 + ' ' + full_text

    text2 = ''
    for obj in rawdata2:
        
        if obj.has_key('title')
            title = obj['title']
        else:
            title = ''
        text = obj['text']
        
        full_text = text + ' ' + title
        full_text = full_text.encode('ascii','ignore')

        text2 = text2 + ' ' + full_text

    text3 = ''
    for obj in rawdata3:
        
        if obj.has_key('title')
            title = obj['title']
        else:
            title = ''
        text = obj['text']
        
        full_text = text + ' ' + title
        full_text = full_text.encode('ascii','ignore')

        text3 = text3 + ' ' + full_text

    path1 = os.getcwd() + '/' + Class + '/' + filename1 + '.txt'
    path2 = os.getcwd() + '/' + Class + '/' + filename2 + '.txt'
    path3 = os.getcwd() + '/' + Class + '/' + filename3 + '.txt'

    fp1 = open(path1,'w')
    fp1.write(text1)
    fp1.close()

    fp2 = open(path2,'w')
    fp2.write(text2)
    fp2.close()
    
    fp3 = open(path3,'w')
    fp3.write(text3)
    fp3.close()

if __name__ == '__main__':
    main()
