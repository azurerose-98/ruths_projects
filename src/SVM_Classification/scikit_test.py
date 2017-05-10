#!/user/bin/python3

import numpy as np
import scipy
from scipy import sparse
import matplotlib.pyplot as plt
import pandas as pd

from sklearn import svm
import sklearn.svm
from sklearn.preprocessing import LabelBinarizer
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import CCA
from sklearn.datasets import make_multilabel_classification
from sklearn.multiclass import OneVsRestClassifier
from sklearn import datasets

from data_formatting import Bag_of_Words
from data_formatting import Text_Object
from data_formatting import Index_Dictionary
import sys
import os.path
import pickle



#   This script takes at least 4 and up to 6 arguments:
#
#       1. the name of the first training pickled object
#       2. the name of the second training pickled object
#       3. the name of the pickled object to be tested
#       4. the desired type of SVM to be utilized
#       5. an optional parameter specification for the classifier
#       6. an additional optional parameter specification for the classifier
#
#   The options for types of SVM, their argument codes, and optional parameters are as follows:
#
#       1. C-Support - SVC
#           * 5th argument options for kernel types:
#               - linear
#               - poly
#               - rbf
#               - sigmoid
#           * if poly is selected: an integer polynomial degree can be specified as the 6th argument
#       2. Linear - Linear
#           * 5th argument option: floating point penalty parameter C
#       3. Nu-Support - NuSVC
#           * 5th argument option: a floating point number nu on the interval (0,1]
#
#   If an invalid argument code is entered, the script will terminate



def main():



    # initializes global objects and classifier with specifications

    Class1 = sys.argv[1].split('-')[0]
    Class2 = sys.argv[2].split('-')[0]
    Class3 = sys.argv[3].split('-')[0]
    categories = [Class1, Class2]

    ctype = str(sys.argv[4])
    print(ctype)

    if ctype == 'Linear':
        if len(sys.argv) == 6:
            Classifier = svm.LinearSVC(C=float(sys.argv[5]))
        else:
            Classifier = svm.LinearSVC()
    elif ctype == 'SVC':
        if len(sys.argv) > 5:
            kernel_type = sys.argv[5]
            if kernel_type == 'linear':
                Classifier = svm.SVC(kernel='linear')
            elif kernel_type == 'poly':
                if len(sys.argv) == 7:
                    deg = int(sys.argv[6])
                    Classifier = svm.SVC(kernel='poly', degree=deg)
                else:
                    Classifier = svm.SVC(kernel='poly')
            elif kernel_type == 'rbf':
                Classifier = svm.SVC(kernel='rbf')
            elif kernel_type == 'sigmoid':
                Classifier = svm.SVC(kernel='sigmoid')
            else:
                print('INVALID OPTIONAL SPECIFICATION')
                exit()                
        else:
            Classifier = svm.SVC()
    elif ctype == 'NuSVC':
        if len(sys.argv) == 6:
            nu = float(sys.argv[5])
            Classifier = svm.NuSVC(nu)
        else:
            Classifier = svm.NuSVC()
    else:
        print('INVALID SVM CODE')
        exit()
        


    # reads pickles Bag_of_Words objects and extracts data

    fp1 = open(sys.argv[1],'rb')
    WordBag1 = pickle.load(fp1)
    raw_data1 = WordBag1.getDataArray()
    fp1.close()
    
    fp2 = open(sys.argv[2],'rb')
    WordBag2 = pickle.load(fp2)
    raw_data2 = WordBag2.getDataArray()
    fp2.close()

    fp3 = open(sys.argv[3],'rb')
    WordBag3 = pickle.load(fp3)
    raw_data3 = WordBag3.getDataArray()
    fp3.close()

    test_data = raw_data3



    # organizes data for sparse.csr formating and classifier training

    raw_data = []
    raw_data.extend(raw_data1)
    raw_data.extend(raw_data2)

    rowspace = len(raw_data)
    columnspace = len(raw_data[0])
    #print(''+str(rowspace)+','+str(columnspace))

    DataArray = np.array(raw_data,dtype=float)
    SparseData = sparse.csr_matrix(DataArray)

    TestArray = np.array(test_data,dtype=float)
    SparseTest = sparse.csr_matrix(TestArray)

    targets = []
    answers = []
    
    i = 0
    while i < len(raw_data1):
        targets.append(categories[0])
        i += 1
    while i < len(raw_data):
        targets.append(categories[1])
        i += 1

    i = 0
    while i < len(test_data):
        answers.append(Class3)
        i += 1
        


    # trains classifier

    X, y = SparseData, targets
    Classifier.fit(X,y)



    # classifies test data and reports accuracy of classifier

    accuracy = Classifier.score(SparseTest, answers)
    print(accuracy)
    results = Classifier.predict(SparseTest)
    print(results)



if __name__ == '__main__':
    main()
