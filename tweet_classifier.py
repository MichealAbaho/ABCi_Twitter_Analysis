# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:21:00 2017

@author: Mike
"""
import pandas as pd
import numpy as np
import re
import nltk

def tweet_classification():
    text1_similarity = []
    text2_similarity = []
    text3_similarity = []
    classes = []
    rd = pd.read_csv('adv_weka_test_set_file.csv')
    
    rdToArray = np.array(rd)
    rdToList = rdToArray.tolist()
    features = {}
    classifier = []
    for i in rdToArray:
        x = (i[0].strip('[]'))
        app_comma = re.compile("[',]")
        x = app_comma.sub('', x)
        x = x.split()
        if (len(x) > 2):
            text1_similarity.append(float(x[0]))
            text2_similarity.append(float(x[1]))
            text3_similarity.append(float(x[2]))
            classes.append(i[1])
        else:
            text1_similarity.append(float(x[0]))
            text2_similarity.append(float(x[1]))
            text3_similarity.append(0)
            classes.append(i[1])
    
    pg = pd.DataFrame({'text1_similarity':text1_similarity,
                       'text2_similarity':text2_similarity, 
                       'text3_similarity':text3_similarity,
                       'Advise-type':classes
                       })
    pg.set_index('text1_similarity', inplace = True)
    pg.to_csv('weka_test_set.csv')
    
#==============================================================================
#     features[feature] = i[1] 
#     feature = (tuple(x))
#     classifier.append(features)
#             
#     class_alg = nltk.NaiveBayesClassifier.train(classifier)
#     prnt ("Naive Bayes Algo accuracy:", (nltk.classify.accuracy(class_alg, )))
#==============================================================================
tweet_classification()