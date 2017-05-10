#!/user/bin/python

import unittest
import json
import DataParse
from DataParse import Post
from DataParse import SubredditClass
from DataParse import StatisticSet
import math

class Test_json_data_extract(unittest.TestCase):

    def setUp(self):

        self.Animals_Nov = open('Animals-Nov.json', 'r+').read()
        self.Animals_Dec = open('Animals-Dec.json', 'r+').read()
        self.Animals_Jan = open('Animals-Jan.json', 'r+').read()
        self.Food_Nov = open('Food-Nov.json', 'r+').read()
        self.Food_Dec = open('Food-Dec.json', 'r+').read()
        self.Food_Jan = open('Food-Jan.json', 'r+').read()

        self.animals1 = json.loads(self.Animals_Nov)
        self.animals2 = json.loads(self.Animals_Dec)
        self.animals3 = json.loads(self.Animals_Jan)
        self.food1 = json.loads(self.Food_Nov)
        self.food2 = json.loads(self.Food_Dec)
        self.food3 = json.loads(self.Food_Jan)

        self.Animals = SubredditClass('Animals')
        self.Food = SubredditClass('Food')

    def tearDown(self):

        print '\nEND OF json_data_extract Test'

    def test_json_data_extract(self):

        DataParse.json_data_extract(self.animals1, self.Animals, 'Animals')
        DataParse.json_data_extract(self.animals2, self.Animals, 'Animals')
        DataParse.json_data_extract(self.animals3, self.Animals, 'Animals')
        DataParse.json_data_extract(self.food1, self.Food, 'Food')
        DataParse.json_data_extract(self.food2, self.Food, 'Food')
        DataParse.json_data_extract(self.food3, self.Food, 'Food')

        assert len(self.Food.posts) == 30
        assert self.Food.posts[0].getClass() == 'Food'
        assert self.Food.posts[29].getClass() == 'Food'
        assert self.Food.posts[0].getTitle() == 'banana'
        assert self.Food.posts[29].getTitle() == 'cracker'
        assert self.Food.posts[0].selftext == 'apple'
        assert self.Food.posts[29].selftext == 'apple'

        assert len(self.Animals.posts) == 30
        assert self.Animals.posts[0].getClass() == 'Animals'
        assert self.Animals.posts[29].getClass() == 'Animals'
        assert self.Animals.posts[0].getTitle() == 'cat'
        assert self.Animals.posts[29].getTitle() == 'octopus'
        assert self.Animals.posts[0].selftext == 'dog'
        assert self.Animals.posts[29].selftext == 'dog'

       

class TestPostMethods(unittest.TestCase):

    def setUp(self):

        self.title = 'Star Trek Theme'
        self.text = 'Space: the final frontier. These are the voyages of the starship Enterprise. Its continuing mission: to explore strange new worlds, to seek out new life and new civilizations, to boldly go where no one has gone before.'
        self.this_class = 'SciFi'
        
        self.post = Post(self.this_class, self.text, self.title)

    def tearDown(self):

        print '\nEND OF Post TEST'

    def test_extractWords(self):

        self.post.extractWords()
        
        assert 'frontier' in self.post.words
        assert 'star' in self.post.words
        assert 'trek' in self.post.words
        assert '.' not in self.post.words
        
        

class TestSubredditClass(unittest.TestCase):

    def setUp(self):

        self.subreddit1 = SubredditClass('Food1')
        self.subreddit2 = SubredditClass('Food2')
        self.subreddit3 = SubredditClass('Food3')
        
        self.Food_Nov = open('Food-Nov.json', 'r+').read()
        self.Food_Dec = open('Food-Dec.json', 'r+').read()
        self.Food_Jan = open('Food-Jan.json', 'r+').read()
        
        self.food1 = json.loads(self.Food_Nov)
        self.food2 = json.loads(self.Food_Dec)
        self.food3 = json.loads(self.Food_Jan)
        
        DataParse.json_data_extract(self.food1, self.subreddit1, 'Food1')
        DataParse.json_data_extract(self.food2, self.subreddit2, 'Food2')
        DataParse.json_data_extract(self.food3, self.subreddit3, 'Food3')        

    def tearDown(self):

        print '\nEND OF SubredditClass TEST'        

    def test_splitData(self):

        assert len(self.subreddit1.posts) == 10
        assert len(self.subreddit2.posts) == 10
        assert len(self.subreddit3.posts) == 10

        self.subreddit1.splitData('A')
        self.subreddit2.splitData('T')
        self.subreddit3.splitData('I', 3)

        assert len(self.subreddit1.test_set) == 0
        assert len(self.subreddit1.training_set) == 10
        assert len(self.subreddit2.test_set) == 10
        assert len(self.subreddit2.training_set) == 0
        assert len(self.subreddit3.test_set) == 1
        assert len(self.subreddit3.training_set) == 9

    def test_updateWords(self):

        self.subreddit1.splitData('A')
        self.subreddit2.splitData('T')
        self.subreddit3.splitData('I', 3)        
        
        self.subreddit1.updateWords()
        self.subreddit2.updateWords()
        self.subreddit3.updateWords()

        assert self.subreddit1.total_words == 20
        assert self.subreddit2.total_words == 0
        assert self.subreddit3.total_words == 18

    def test_copy(self):

        copy1 = self.subreddit1.copy()

        assert cmp(copy1.getWords(), self.subreddit1.getWords()) == 0



class TestStatisticSet(unittest.TestCase):
       
    def setUp(self):

        self.Animals_Nov = open('Animals-Nov.json', 'r+').read()
        self.Animals_Dec = open('Animals-Dec.json', 'r+').read()
        self.Animals_Jan = open('Animals-Jan.json', 'r+').read()
        self.Food_Nov = open('Food-Nov.json', 'r+').read()
        self.Food_Dec = open('Food-Dec.json', 'r+').read()
        self.Food_Jan = open('Food-Jan.json', 'r+').read()

        self.animals1 = json.loads(self.Animals_Nov)
        self.animals2 = json.loads(self.Animals_Dec)
        self.animals3 = json.loads(self.Animals_Jan)
        self.food1 = json.loads(self.Food_Nov)
        self.food2 = json.loads(self.Food_Dec)
        self.food3 = json.loads(self.Food_Jan)

        self.Animals = SubredditClass('Animals')
        self.Food = SubredditClass('Food')
        self.AnimalsTestClass = SubredditClass('Animals')
        self.FoodTestClass = SubredditClass('Food')

        DataParse.json_data_extract(self.animals1, self.Animals, 'Animals')
        DataParse.json_data_extract(self.animals2, self.Animals, 'Animals')
        DataParse.json_data_extract(self.animals3, self.AnimalsTestClass, 'Animals')
        
        DataParse.json_data_extract(self.food1, self.Food, 'Food')
        DataParse.json_data_extract(self.food2, self.Food, 'Food')
        DataParse.json_data_extract(self.food3, self.FoodTestClass, 'Food')

        self.Food.splitData('A')
        self.Food.updateWords()
        self.Animals.splitData('A')
        self.Animals.updateWords()
        self.FoodTestClass.splitData('T')
        self.AnimalsTestClass.splitData('T')

        self.FoodControl = self.Food.copy()
        self.AnimalControl = self.Animals.copy()

        self.Classifier = StatisticSet(self.Food, self.Animals)

    def tearDown(self):

        print '\nEND OF StatisticSet TEST'

    def test__init__(self):

        assert cmp(self.Classifier.ClassA.getWords(), self.Food.getWords()) == 0
        assert cmp(self.Classifier.ClassB.getWords(), self.Animals.getWords()) == 0
        assert cmp(self.Classifier.ClassA_words, self.Food.getWords()) == 0
        assert cmp(self.Classifier.ClassB_words, self.Animals.getWords()) == 0
        assert cmp(self.Classifier.ClassA.getWords(), self.FoodControl.getWords()) == 0
        assert cmp(self.Classifier.ClassB.getWords(), self.AnimalControl.getWords()) == 0
        assert cmp(self.Classifier.ClassA_words, self.FoodControl.getWords()) == 0
        assert cmp(self.Classifier.ClassB_words, self.AnimalControl.getWords()) == 0
        assert cmp(self.Food.getWords(), self.FoodControl.getWords()) == 0
        assert cmp(self.Animals.getWords(), self.AnimalControl.getWords()) == 0

    def test_build_probability_data(self):

        self.Classifier.buildProbabilityData()
        
        for key in self.Classifier.word_prob_A.keys():
            assert self.Classifier.word_prob_A[key] == math.log1p(1/float(20))
        for key in self.Classifier.word_prob_B.keys():
            assert self.Classifier.word_prob_B[key] == math.log1p(1/float(20))

    def test_make_test_set(self):

        self.foodTestSet = self.FoodTestClass.getTestSet()
        self.Classifier.makeTestSet('N', self.foodTestSet)

        assert cmp(self.Classifier.test_set, self.FoodTestClass.test_set) == 0

    def test_classification_accuracy_food_test_set(self):

        self.Classifier.buildProbabilityData()
            
        self.foodTestSet = self.FoodTestClass.getTestSet()
        self.Classifier.makeTestSet('N', self.foodTestSet)

        assert cmp(self.Classifier.test_set, self.FoodTestClass.test_set) == 0

        accuracy = self.Classifier.AnalyzeAccuracy('UnitTestOutput1.txt', 'Unit Test Output on food_test_set')

        assert accuracy == 1.0

    def test_classification_accuracy_animals_test_set(self):

        self.Classifier.buildProbabilityData()

        self.animalsTestSet = self.AnimalsTestClass.getTestSet()
        self.Classifier.makeTestSet('N', self.animalsTestSet)

        assert cmp(self.Classifier.test_set, self.AnimalsTestClass.test_set) == 0

        accuracy = self.Classifier.AnalyzeAccuracy('UnitTestOutput2.txt', 'Unit Test Output on animals_test_set')

        assert accuracy == 1.0




if __name__ == '__main__':
    unittest.main()
