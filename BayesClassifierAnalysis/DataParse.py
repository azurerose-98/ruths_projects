#!/user/bin/python

import json
from io import StringIO
import string
import os.path
from os.path import dirname, abspath
from decimal import *
import operator
import sys
import unicodedata
import math
import random

# this script takes 7 command line arguments:
#       1. the name of the subreddit of the first dataset
#       2. the name of the subreddit of the second dataset
#       3. the name of the first dataset file
#       4. the name of the second dataset file
#       5. the name of the data file containing the test set
#       6. the actual class of the test set
#       7. the name of the file to write the results of the analysis to
# all arguments must be enetered or the program will NOT run



# a class that contains the data from one reddit post

class Post:

    def __init__(self, post_class, post_selftext, post_title):

        self.total_words = 0
        
        self.words = {}
        self.class_name = post_class
        self.selftext = post_selftext.lower()
        self.title = post_title.lower()

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

        elif option == 'A':
            self.training_set = self.posts

        elif option == 'T':
            self.test_set = self.posts
            
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

    def copy(self):

        newCopy = SubredditClass(self.class_name)
        
        newCopy.num_posts = self.num_posts
        newCopy.posts += self.posts
        newCopy.training_set += self.training_set
        newCopy.test_set += self.test_set
        newCopy.updateWords()

        return newCopy

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
        
        self.ClassA = class_A.copy()
        self.ClassB = class_B.copy()
        self.ClassA_name = self.ClassA.getName()
        self.ClassB_name = self.ClassB.getName()
        self.ClassA_words = self.ClassA.getWords()
        self.ClassB_words = self.ClassB.getWords()

        self.words.update(self.ClassA_words)
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
        

    def makeTestSet(self, option, new_test_data=None):
       
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
            
        elif option == 'N' and new_test_data != None: 

            self.test_set = new_test_data

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
            # for x in range(words[word]):
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

        #prob_A = raw_prob_A
        #prob_B = raw_prob_B

        #print 'prob_A: ' + str(prob_A) + '\t\t\tprob_B: ' + str(prob_B) + '\t\t\tdiff: ' + str(prob_A - prob_B)

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
            print result

    def AnalyzeAccuracy(self, output_file_name, header ):

        output_file = open(output_file_name, 'w')

        output_file.write(header + '\n') 

        total = 0
        true = 0
        false = 0

        for post in self.test_set:

            total += 1

            is_accurate = False
            
            true_answer = post.getClass()
            classifier_answer = self.classify(post)
            result = true_answer + '\t' + classifier_answer + '\n'

            output_file.write(result)

            if classifier_answer == true_answer:
                is_accurate = True
            else:
                pass

            if is_accurate == True:
                true += 1
            else:
                false += 1

        accuracy =  float(true) / float(total)
        output_file.write('total: ' + str(total) + '\t' )
        output_file.write('accuracy: ' + str(accuracy) + '\n' )

        output_file.close()

        return accuracy
        
                   


# main: processes data and runs analysis

def json_data_extract(jsonfile, subreddit_class, this_class):

    POST_INDEX = 0
    post = jsonfile[POST_INDEX]
    
    while post != None and POST_INDEX < len(jsonfile):

        #print post

        title = post['title'].lower()
        text = post['text'].lower()

        new_post = Post(this_class, text, title)
        new_post.extractWords()

        subreddit_class.addPost(new_post)

        POST_INDEX += 1

        if POST_INDEX < len(jsonfile):

            comment = jsonfile[POST_INDEX]

            #print comment

            while 'title' not in comment.keys():

                this_title = ''
                this_text = comment['text'].lower()

                new_com = Post(this_class, this_text, this_title)
                new_com.extractWords()

                subreddit_class.addPost(new_com)

                POST_INDEX += 1

                if POST_INDEX < len(jsonfile):
                    comment = jsonfile[POST_INDEX]
                else:
                    break
            
            if POST_INDEX < len(jsonfile):
                post = jsonfile[POST_INDEX]
            else:
                break

        else:
            break

def main():

    if len(sys.argv) < 8:
        print 'ERROR: MISSING COMMAND LINE ARGUMENTS'
        exit
    elif len(sys.argv) > 8:
        print 'ERROR: TOO MANY COMMAND LINE ARGUMENTS'
        exit
    else:
        pass

    jsonfile1 = '/' + sys.argv[3]
    path1 = os.getcwd() + jsonfile1
    jsonfile2 = '/' + sys.argv[4]
    path2 = os.getcwd() + jsonfile2
    jsonfile3 = '/' + sys.argv[5]
    path3 = os.getcwd() + jsonfile3

    json_file1 = open(path1,'r+').read()
    rawdata1 = json.loads(json_file1)
    json_file2 = open(path2,'r+').read()
    rawdata2 = json.loads(json_file2)
    json_file3 = open(path3,'r+').read()
    rawdata3 = json.loads(json_file3)

    print 'RAW DATA RETRIEVED'

    statistics_file = '/' + sys.argv[7]
    path4 = os.getcwd() + statistics_file

    Class_A = SubredditClass(sys.argv[1])
    Class_B = SubredditClass(sys.argv[2])
    Test_Class = SubredditClass(sys.argv[6])

    json_data_extract(rawdata1, Class_A, Class_A.getName())
    json_data_extract(rawdata2, Class_B, Class_B.getName())
    json_data_extract(rawdata3, Test_Class, Test_Class.getName())

    print 'JSON DATA EXTRACTED'

    Class_A.splitData('A')
    Class_A.updateWords()
    Class_B.splitData('A')
    Class_B.updateWords()
    Test_Class.splitData('T')

    print len(Class_A.getWords())
    print len(Class_B.getWords())

    diff = set(Class_A.getWords().keys()) - set(Class_B.getWords().keys())
    print len(list(diff))

    new_test_set = Test_Class.getTestSet()

    print 'TEST SET TO BE CLASSIFIED DESIGNATED'

    this_header = 'trained on: ' + sys.argv[3] + ', ' + sys.argv[4] + '\n tested on: ' + sys.argv[5] + '\n'

    Classifier = StatisticSet(Class_A, Class_B)
    Classifier.buildProbabilityData()
    Classifier.makeTestSet('N', new_test_set)
    Classifier.AnalyzeAccuracy(path4, this_header)

    print 'TEST SET CLASSIFIED'
    print 'ANALYSIS OF CLASSIFIER PRINTED TO ' + sys.argv[7]

if __name__ == '__main__':
    main()
