#!/usr/bin/python

import json
from io import StringIO
import string
import os.path
from os.path import dirname, abspath
from decimal import *

# a class to store all the attributes of each question
class Question:

    category = ""
    attributes = {}

    def __init__( self, category ):
        self.category = category
    
    def add( self, key, d ):
        self.attributes[key] = d

    def get( self, key ):
        return self.attributes.get(key)

    def copy( self ):
        new = Question( self.category )
        new.attributes = self.attributes.copy()
        return new

# a class to store the frequency of each association
class Category:

    category = ""
    instances = 0
    jaigeo = 0
    jaipasgeo = 0

    def __init__( self, category ):
        self.category = category
        self.instances+=1

    def increment( self ):
        self.instances+=1

    def incrementjai( self ):
        self.jaigeo+=1
    
    def incrementpas( self ):
        self.jaipasgeo+=1

# organizes the raw data  
jfile = "/JEOPARDY_QUESTIONS1.json"
path = dirname(os.getcwd()) + jfile
jsonfile = open(path,'r+').read()
rawdata = json.loads(jsonfile)
geography = open("geographywords.txt").read()
rgeo = geography.split("\n")
geo = []

# extracts the geography words from the raw data file
g = 0
while ( g<len(rgeo) ):
    j = rgeo[g].lower()
    geo.append(j)
    g+=1
num_geo = len(geo)

questions = []
x = 0
while ( x<len(rawdata) ):
    k = rawdata[x].keys()
    v = rawdata[x].values()
    i = Question( v[0] )
    y = 1
    while ( y<len(rawdata[x])):
        i.add( k[y], v[y] )
        y += 1
    questions.append(i.copy())
    x += 1
num_questions = len(questions)

# counts instances of categories and geography questions
associations = {}
categories = []
total_jai = 0
total_pas = 0

a = 0
while ( a<len(questions) ):
    cat = questions[a].category
    if ( associations.has_key(cat) == False ):
        associations[cat] = Category(cat) # adds new category to associations
        categories.append(cat)
    else:
        associations[cat].increment() # increments instance of category
    # determines if question contains a geography word
    quest = questions[a].get("question")
    lqwords = quest.lower()
    qwords = lqwords.split(" ")
    t = 0
    found = False
    while ( t<num_geo and found == False ):
        if ( geo[t] in qwords ):
            associations[cat].incrementjai()
            total_jai+=1
            found = True
        t+=1
    # determines if answer contains a geography word
    answer = questions[a].get("answer")
    lawords = answer.lower()
    awords = lawords.split(" ")
    s = 0
    while ( s<num_geo and found == False ):
        if ( geo[s] in awords ):
            associations[cat].incrementjai()
            total_jai+=1
            found = True
        s+=1
    if ( found == False ):
        associations[cat].incrementpas()
        total_pas+=1
    a+=1

# calculates Naive Bayes probability of a question of each category being a geography question
results = open("results.txt", "w")
results.truncate()

count = 0
while ( count<len(associations) ):
    categ = categories[count]
    freq_categ = Decimal(associations[categ].instances) / Decimal(num_questions)
    freq_geo = Decimal(total_jai) / Decimal(num_questions)
    freq_positive = Decimal(associations[categ].jaigeo) / Decimal(total_jai)
    if ( freq_categ > 0 ):
        nbprob = ( freq_positive * freq_geo ) / freq_categ
    else:
        nbprob = 0
    results.write( (categ + ":   " + str(nbprob) + "\n").encode("utf-8") )
    count+=1

results.close()
