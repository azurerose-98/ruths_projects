#!/user/bin/python

import json
from io import StringIO
import os.path
import string
import sys
import unicodedata
import math
import pickle
import copy

#   This script takes multiple arguments
#
#   The first is either "All" or an integer
#       - "All" will use all the data from all the files
#       - An integer argument will
#           a) force the script to only take that many posts from each file
#           b) if there aren't enough posts in any file, program will terminate
#
#   Each subsequent argument is the class name of a 3-set of json files to be proccessed
#
#   Example:
#
#   >>> python data_formatting.py All Animals Food
#
#   This will output:
#       - Animals-Nov.pickle
#       - Animals-Dec.pickle
#       - Animals-Jan.pickle
#       - Food-Nov.pickle
#       - Food-Dec.pickle
#       - Food-Jan.pickle


# an object that contains the data from one reddit post

class Text_Object:

    def __init__(self, raw_obj):

        self.words = {}
        self.num_words = 0
        self.total_words = 0

        self.obj = raw_obj

        self.process_obj()
        self.word_freq = self.make_frequencies()

    def process_obj(self):

        if self.obj.has_key('title'):
            title = self.obj['title'].lower()
        else:
            title = ''
        text = self.obj['text'].lower()

        full_text = text + ' ' + title
        full_text = full_text.encode('ascii','ignore')

        self.extract(full_text)

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
                self.num_words += 1
                self.total_words += 1
                
            i += 1

    def make_frequencies(self):

        new_dict = {}
        
        for word in self.words.keys():
            new_dict[word] = self.words[word] / float(self.num_words)
            
        return new_dict

    def getWords(self):

        return self.words.keys()

    def getWordFreq(self):

        new_dict = {}

        for word in self.word_freq:
            new_dict[word] = self.word_freq[word]

        return new_dict

    

# an object that serves as an index dictionary for the various features ( in this case, words )

class Index_Dictionary:

    def __init__(self):

        self.dictionary = {}
        self.num_words = 0
        self.current_index = 0

    def add_word(self, word):

        if word not in self.dictionary:
            self.dictionary[word] = self.current_index
            self.current_index += 1
        else:
            pass

    def getDict(self):

        new_dict = {}

        for word in self.dictionary:
            new_dict[word] = self.dictionary[word]

        return new_dict



# an object that builds and stores the raw frequency matrix of features

class Bag_of_Words:

    def __init__(self, index_dict):

        self.data_array = []
        
        self.WordDict = index_dict.getDict()
        self.objects = []
        self.num_features = len(self.WordDict.keys())
        self.num_objects = 0

    def add_object(self, new_object):

        self.objects.append(new_object)
        self.num_objects += 1

    def allocate_array_size(self, array, size):

        s = 0
        while s < size:
            array.append(float(0))
            s += 1

    def build_data_array(self):

        for obj in self.objects:

            obj_array = []
            self.allocate_array_size(obj_array, self.num_features)
            
            words = obj.getWordFreq().keys()
            word_freq = obj.getWordFreq()
            
            for word in words:
            
                word_index = self.WordDict[word]
                obj_array[word_index] = word_freq[word]

            self.data_array.append(copy.copy(obj_array))

    def getDataArray(self):

        return copy.copy(self.data_array)



def main():



    # initializes global objects

    if sys.argv[1] != 'All':
        balance = int(sys.argv[1])
    else:
        balance = 'All'

    Classes = sys.argv[2:]
    Class_Files = {}

    IndexDict = Index_Dictionary()



    # loads json data

    for Class in Classes:
    
        text_objects_1 = []
        text_objects_2 = []
        text_objects_3 = []

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

        # extracts and converts data from json format to Text_Object objects

        if balance != 'All':

            i = 0
            for data in rawdata1:
                
                new_obj = Text_Object(data)
                text_objects_1.append(new_obj)
                
                for word in new_obj.getWords():
                    IndexDict.add_word(word)

                i += 1

                if i >= balance:
                    break
                
            if i < balance:
                print('ERROR: NOT ENOUGH POSTS')
                exit()

            i = 0
            for data in rawdata2:
                
                new_obj = Text_Object(data)
                text_objects_2.append(new_obj)
                
                for word in new_obj.getWords():
                    IndexDict.add_word(word)

                i += 1

                if i >= balance:
                    break

            if i < balance:
                print('ERROR: NOT ENOUGH POSTS')
                exit()

            i = 0
            for data in rawdata3:
                
                new_obj = Text_Object(data)
                text_objects_3.append(new_obj)
                
                for word in new_obj.getWords():
                    IndexDict.add_word(word)

                i += 1

                if i >= balance:
                    break

            if i < balance:
                print('ERROR: NOT ENOUGH POSTS')
                exit()

        else:

            for data in rawdata1:
                
                new_obj = Text_Object(data)
                text_objects_1.append(new_obj)
                
                for word in new_obj.getWords():
                    IndexDict.add_word(word)

            for data in rawdata2:
                
                new_obj = Text_Object(data)
                text_objects_2.append(new_obj)
                
                for word in new_obj.getWords():
                    IndexDict.add_word(word)

            for data in rawdata3:
                
                new_obj = Text_Object(data)
                text_objects_3.append(new_obj)
                
                for word in new_obj.getWords():
                    IndexDict.add_word(word)

        Class_Files[filename1] = text_objects_1
        Class_Files[filename2] = text_objects_2
        Class_Files[filename3] = text_objects_3

    

    # builds Bag_of_Words objects and frequency arrays and pickles Bag_of_Words objects

    for cfile in Class_Files.keys():

        text_objects = Class_Files[cfile]
        filename = cfile

        WordBag = Bag_of_Words(IndexDict)

        for obj in text_objects:
            WordBag.add_object(obj)

        WordBag.build_data_array()

        out_filename = filename + '.pickle'

        fp = open(out_filename, 'w')
        pickle.dump(WordBag, fp)
        fp.close()



if __name__ == '__main__':
    main()
