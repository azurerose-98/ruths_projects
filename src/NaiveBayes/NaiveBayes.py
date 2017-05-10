#!/usr/bin/python

import json
from io import StringIO
import string
import os.path
from os.path import dirname, abspath
from decimal import *
import operator
import unicodedata
import math

# helper methods to assist in calculations

def learn( q, d ):
    newq = q["question"].lower()
    newa = q["answer"].lower() 
    new = newq + " " + newa + " "
    h = 0
    while ( h<len(new) ):
        word = ""
        char = new[h]
        while ( ord(char) > 96 and ord(char) < 123 ):
            word = word + char
            h+=1
            char = new[h]
        word_key = str(word)
        if ( word == "" ):
            pass
        elif ( d.has_key(word_key) == False ):
            d[word_key] = 1
        else:
            d[word_key] = d[word_key] + 1
        h+=1

def nb_prob( word_list, categ_words, categ_count, word_count, total ):

    k = categ_words.keys()
    prob_dict = {}
    for w in word_list:
        for g in k:
            if ( w in categ_words[g].keys() ):
                if ( prob_dict.has_key(g) == False ):
                    prob_dict[g] = math.log1p(categ_count[g]/total) + math.log1p(categ_words[g][w]/word_count[w])
                else:
                    prob_dict[g] += math.log1p(categ_words[g][w]/word_count[w])

    current_max = 0
    nb_max_prob = "NO ANSWER FOUND"
    for b in prob_dict.keys():
        if ( math.pow( math.e, prob_dict[b] ) > current_max ):
            currentmax = pow( math.e, prob_dict[b] )
            nb_max_prob = b

    return nb_max_prob

def parse( string ):
    wordcount = {}
    i = 0
    while i<len(string):
        word = ""
        char = string[i]

        while ( ord(char) > 96 and ord(char) < 123 ):
            word = word + char
            i += 1
            char = string[i]
        word_key = str(word)
        if ( word == "" ):
            pass
        elif ( wordcount.has_key(word_key) == False ):
            wordcount[word_key] = 1
        else:
            wordcount[word_key] = wordcount[word_key] + 1
        i += 1

    return wordcount

# organization of the raw data / training set analysis 

jfile = "/JEOPARDY_QUESTIONS1.json"
path = dirname(os.getcwd()) + jfile
jsonfile = open(path,'r+').read()
rawdata = json.loads(jsonfile)

strings = {}
counter = {}
word_counter = {}
total_qs = 0

x = 0
TRAINING_SIZE = 200000
while ( x <= TRAINING_SIZE ):
    total_qs+=1
    categ = rawdata[x]['category'].encode('ascii','ignore')
    quest = rawdata[x]['question'].lower()
    answ = rawdata[x]['answer'].lower()
    if ( categ in strings ):
        strings[categ] = strings[categ] + quest + ' ' + answ + ' '
        counter[categ] = counter[categ] + 1
    else:
        strings[categ] = quest + ' ' + answ + ' '
        counter[categ] = 1
    x+=1

string_keys = sorted( strings, key=strings.__getitem__, reverse=True )

words = {}

y = 0
while ( y<len(string_keys) ):
    string_key = string_keys[y]
    words[string_key] = parse( strings[string_key] )
    for s in words[string_key]:
        if ( word_counter.has_key(s) == False ):
            word_counter[s] = 1
        else:
            word_counter[s] += 1
    y+=1

print 'ORGANIZATION COMPLETE\n'

# naive-bayes analysis of the leftover questions

while ( x<len(rawdata) ):
    new_q_words = {}
    learn( rawdata[x], new_q_words )
    new_words = new_q_words.keys()
    categ_guess = nb_prob( new_words, words, counter, word_counter, total_qs )
    print rawdata[x]["question"]
    print categ_guess + "\t" + rawdata[x]["category"].encode('ascii','ignore')
    x+=1

#results = open("results.txt", "w")
#results.truncate()

# stop words
