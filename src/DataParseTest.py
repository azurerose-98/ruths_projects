#!/user/bin/python

import json
from io import StringIO
import string
import os.path
from os.path import dirname, abspath
from decimal import *
import operator
import unicodedata
import math
import random



# a class that contains the data from one redit post

class Post:

    def __init__(self, post_class, post_selftext, post_title):

        self.total_words = 0
        
        self.words = {}
        self.class_name = post_class
        self.selftext = post_selftext
        self.title = post_title

    def extract(self, string):

        i = 0
        
        while i<len(string):
            
            word = ''
            char = string[i]
            while ord(char) > 96 and ord(char) < 123:
                word = word + char
                i += 1
                if i < len(string):
                    char = string[i]
                else:
                    char = ' '
                
            word_key = str(word)
        
            if word_key == '':
                pass
            elif word_key in self.words.keys():
                self.words[word_key] = self.words[word_key] + 1
                self.total_words += 1
            else:
                self.words[word_key] = 1
                self.total_words += 1
                
            i += 1

    def extractWords(self):
        
        self.extract(self.selftext)
        self.extract(self.title)

    def getWords(self):

        return self.words

    def getClass(self):

        return self.class_name

    def getTitle(self):

        return self.title



# a class that contains data of many posts from one subreddit

class SubredditClass:

    def __init__(self, subredditName):

        self.total_words = 0
        self.training_set = []
        self.test_set = []

        self.words = {}
        self.posts = []
        self.num_posts = 0
        self.class_name = subredditName

    def addPost(self, post):

        self.posts.append(post)
        self.num_posts += 1

    def splitData(self, option='S', section_int=0):

        test_num = int(len(self.posts)/10)
        training_num = len(self.posts) - test_num

        if option == 'R':

            section_int = random.randrange(0,10)
            section_index = section_int * test_num
            end_index = section_index + test_num

            i = 0
            while i < section_index:
                self.training_set.append(self.posts[i])
                i += 1
            while i < end_index:
                self.test_set.append(self.posts[i])
                i += 1
            while i < len(self.posts):
                self.training_set.append(self.posts[i])
                i += 1
        
        elif option == 'I':

            section_index = section_int * test_num
            end_index = section_index + test_num

            i = 0
            while i < section_index:
                self.training_set.append(self.posts[i])
                i += 1
            while i < end_index:
                self.test_set.append(self.posts[i])
                i += 1
            while i < len(self.posts):
                self.training_set.append(self.posts[i])
                i += 1

        else:
            
            i = 0
            while i < training_num:
                self.training_set.append(self.posts[i])
                i += 1
            while i < len(self.posts):
                self.test_set.append(self.posts[i])
                i += 1

    def updateWords(self):

        for post in self.training_set:

            word_dict = post.getWords()
            
            for key in word_dict.keys():
                if key in self.words.keys():
                    self.words[key] = self.words[key] + word_dict[key]
                    self.total_words += word_dict[key]
                else:
                    self.words[key] = word_dict[key]
                    self.total_words += word_dict[key]

    def getWords(self):
        
        return self.words

    def getName(self):

        return self.class_name

    def getTestSet(self):

        return self.test_set

    def TotalWordSum(self):

        return self.total_words

    def getTrainingSize(self):

        return len(self.training_set)



# a class that analyzes and compares two subreddit classes

class StatisticSet:

    def __init__(self, class_A, class_B):

        self.test_set = []
        self.words = {}
        self.word_prob_A = {}
        self.word_prob_B = {}
        self.total_word_prob = {}
        self.total_words = 0
        
        self.ClassA = class_A
        self.ClassB = class_B
        self.ClassA_name = class_A.getName()
        self.ClassB_name = class_B.getName()
        self.ClassA_words = class_A.getWords()
        self.ClassB_words = class_B.getWords()

        self.words = self.ClassA_words
        for key in self.ClassB_words:
            if key in self.words.keys():
                self.words[key] = self.words[key] + self.ClassB_words[key]
            else:
                self.words[key] = self.ClassB_words[key]

        self.total_words = self.ClassA.TotalWordSum() + self.ClassB.TotalWordSum()

    def buildProbabilityData(self):

        self.totalTrainingSize = self.ClassA.TotalWordSum() + self.ClassB.TotalWordSum()
        self.num_ClassA = self.ClassA.TotalWordSum()
        self.num_ClassB = self.ClassB.TotalWordSum()
        self.prob_ClassA = math.log1p(self.num_ClassA/float(self.totalTrainingSize))
        self.prob_ClassB = math.log1p(self.num_ClassB/float(self.totalTrainingSize))

        for key in self.ClassA_words:
            self.word_prob_A[key] = math.log1p(self.ClassA_words[key]/float(self.ClassA.TotalWordSum()))

        for key in self.ClassB_words:
            self.word_prob_B[key] = math.log1p(self.ClassB_words[key]/float(self.ClassB.TotalWordSum()))   

        for key in self.words:
            self.total_word_prob[key] = math.log1p(self.words[key]/float(self.total_words))   
        

    def makeTestSet(self, option):
       
        if option == 'A':
            self.test_set = self.ClassA.getTestSet()
        elif option == 'B':
            self.test_set = self.ClassB.getTestSet()
        elif option == 'C':
            self.test_set = self.ClassA.getTestSet()
            
            i = 0
            while i < len(self.ClassB.getTestSet()):
                self.test_set.append(self.ClassB.getTestSet()[i])
                i += 1
            
        else:
            pass
        
    def classify(self, post):

        words = post.getWords()
        word_keys = words.keys()

        raw_prob_A = 0
        raw_prob_B = 0
        chosen_class = ''
        
        for word in word_keys:

            x = 0
            while x < words[word]:
            
                if word in self.word_prob_A.keys():
                    raw_prob_A = raw_prob_A + self.word_prob_A[word]
                else:
                    pass
            
                if word in self.word_prob_B.keys():
                    raw_prob_B = raw_prob_B + self.word_prob_B[word]
                else:
                    pass

                x += 1

        #raw_prob_A = raw_prob_A + self.prob_ClassA
        #raw_prob_B = raw_prob_B + self.prob_ClassB

        e_prob_A = math.pow(math.e, raw_prob_A)
        e_prob_B = math.pow(math.e, raw_prob_B)

        prob_A = e_prob_A
        prob_B = e_prob_B

        if prob_A > prob_B:
            chosen_class = self.ClassA_name
        elif prob_B > prob_A:
            chosen_class = self.ClassB_name
        else:
            chosen_class = 'UNDETERMINED'

        return chosen_class

    def classifyTestData(self):
        
        for post in self.test_set:
            
            answer = post.getClass()
            result = answer + '\t' + self.classify(post)
            #print post.getTitle()
            print result

    def AnalyzeAccuracy(self):

        total = 0
        true = 0
        false = 0

        for post in self.test_set:

            total += 1

            is_accurate = False
            
            answer = post.getClass()
            result = answer + '\t' + self.classify(post)

            if result == post.getTitle():
                is_accurate = True

            if is_accurate == True:
                true += 1
            else:
                false += 1

        return ( true / total )
        
                   


# processes data and runs analysis

jsonfile1 = "/AnimeData.json"
path1 = os.getcwd() + jsonfile1
jsonfile2 = "/SciFiData.json"
path2 = os.getcwd() + jsonfile2

jsonfile1 = open(path1,'r+').read()
rawdata1 = json.loads(jsonfile1)
jsonfile2 = open(path2,'r+').read()
rawdata2 = json.loads(jsonfile2)

Anime_Class_Data = SubredditClass('anime')
SciFi_Class_Data = SubredditClass('scifi')

for key in rawdata1.keys():
    
    page = rawdata1[key]
    page_data = page['data']['children']
    
    for p in page_data:

        d = p['data']

        if 'selftext' in d.keys():
        
            this_class = d['subreddit'].encode('ascii','ignore').lower()
            this_selftext = d['selftext'].encode('ascii','ignore').lower()
            this_title = d['title'].encode('ascii','ignore').lower()
            
            new_post = Post(this_class, this_selftext, this_title)
            new_post.extractWords()

            Anime_Class_Data.addPost(new_post)

        else:
            pass

for key in rawdata2.keys():
    
    page = rawdata2[key]
    page_data = page['data']['children']
    
    for p in page_data:

        d = p['data']

        if 'selftext' in d.keys():
        
            this_class = d['subreddit'].encode('ascii','ignore').lower()
            this_selftext = d['selftext'].encode('ascii','ignore').lower()
            this_title = d['title'].encode('ascii','ignore').lower()
            
            new_post = Post(this_class, this_selftext, this_title)
            new_post.extractWords()

            SciFi_Class_Data.addPost(new_post)

        else:
            pass

Anime_Class_Data.splitData('I', 5)
Anime_Class_Data.updateWords()
SciFi_Class_Data.splitData('I', 5)
SciFi_Class_Data.updateWords()

Anime_SciFi_Classifier = StatisticSet(Anime_Class_Data, SciFi_Class_Data)
Anime_SciFi_Classifier.buildProbabilityData()
Anime_SciFi_Classifier.makeTestSet('C')
Anime_SciFi_Classifier.classifyTestData()























