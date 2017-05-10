#!/user/bin/python3

import numpy as np
import scipy
from scipy import sparse
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os

from sklearn import svm
from sklearn.svm import SVC
from sklearn.preprocessing import LabelBinarizer
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import CCA
from sklearn.datasets import make_multilabel_classification
from sklearn.multiclass import OneVsRestClassifier
from sklearn import datasets



class SubredditClass:

    def __init__(self, ClassName):

        Class = ClassName
        
        filename1 = Class + '-Nov'
        filename2 = Class + '-Dec'
        filename3 = Class + '-Jan'

        jsonfile1 = '/' + filename1 + '.json'
        path1 = os.getcwd() + jsonfile1
        jsonfile2 = '/' + filename2 + '.json'
        path2 = os.getcwd() + jsonfile2
        jsonfile3 = '/' + filename3 + '.json'
        path3 = os.getcwd() + jsonfile3

        file1 = pd.read_json(path1)
        file2 = pd.read_json(path2)
        file3 = pd.read_json(path3)

        data1 = file1.split()
        data2 = file2.split()
        data3 = file3.split()

        

def main():



    ClassA = sys.argv[1]
    ClassB = sys.argv[2]

    ClassA_Data = SubredditClass(ClassA)
    ClassB_Data = SubredditClass(ClassB)



if __name__ == '__main__':
    main()
