# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:21:00 2017

@author: Mike
"""
import pandas as pd
import numpy as np
from tweet_processing import tokens_to_list
from sklearn.cluster import MeanShift  as ms
from sklearn.datasets.samples_generator import make_blobs
import matplotlib.pyplot as plt

class tweet_classification:
    
    def __init__(self, training_set):
        self.training_set = training_set
        
    def tweet_classifier(self):
        text1_similarity = []
        text2_similarity = []
        text3_similarity = []
        classes = []
        original_tweet = []
        rdToArray = np.array(self.training_set)
        
        for i in rdToArray:
            tweet_weights = tokens_to_list(i[3])
            if (len(tweet_weights) > 2):
                text1_similarity.append(float(tweet_weights[0]))
                text2_similarity.append(float(tweet_weights[1]))
                text3_similarity.append(float(tweet_weights[2]))
                classes.append(i[2])
                original_tweet.append(i[1])
            else:
                text1_similarity.append(float(tweet_weights[0]))
                text2_similarity.append(float(tweet_weights[1]))
                text3_similarity.append(0)
                classes.append(i[2])
                original_tweet.append(i[1])
        
        pg = pd.DataFrame({'Original_tweets': original_tweet,
                           'text1_similarity':text1_similarity,
                           'text2_similarity':text2_similarity, 
                           'text3_similarity':text3_similarity,
                           'Advise-type':classes
                           })
        pg.set_index('Original_tweets', inplace = True)
        pg.to_csv('weka_coloncancer_trainset.csv')
    
   
training_set = pd.read_csv('coloncancer-training-set.csv')
classify = tweet_classification(training_set)
classify.tweet_classifier()