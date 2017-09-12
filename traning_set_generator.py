# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 16:21:00 2017

@author: Mike
"""
import pandas as pd
import numpy as np
from tweet_processing import tokens_to_list, working_directory
from sklearn.datasets.samples_generator import make_blobs

class tweet_training_network_sets:
    
    def __init__(self, training_set):
        self.__training_set = training_set
        
    def training_set(self):
        text1_similarity = []
        text2_similarity = []
        text3_similarity = []
        classes = []
        working_directory()
        #original_tweet = []
        rdToArray = np.array(self.__training_set)
        
        for i in rdToArray:
            tweet_weights = tokens_to_list(i[1])
            if (len(tweet_weights) > 2):
                text1_similarity.append(float(tweet_weights[0]))
                text2_similarity.append(float(tweet_weights[1]))
                text3_similarity.append(float(tweet_weights[2]))
                classes.append(i[3])
                #original_tweet.append(i[1])
            elif (len(tweet_weights) == 2):
                text1_similarity.append(float(tweet_weights[0]))
                text2_similarity.append(float(tweet_weights[1]))
                text3_similarity.append(0)
                classes.append(i[3])
                #original_tweet.append(i[3])
        
        pg = pd.DataFrame({'Class': classes,
                           'text1_similarity':text1_similarity,
                           'text2_similarity':text2_similarity, 
                           'text3_similarity':text3_similarity
                           })
        pg = pg[['text1_similarity', 'text2_similarity', 'text3_similarity', 'Class']]
        pg.set_index('text1_similarity', inplace = True)
        pg.to_csv('diabetes\\weka_diabetes_trainset.csv')
    
    
    def user_opinion(self):
        advise = {}
        none_advise = {}
        
        for user,opinion in zip(self.__training_set['Username'], self.__training_set['Class']):
            if (opinion == 'moderately_advise' or opinion == 'mostly_advise' or opinion == 'purely_advise'):
                if user in advise:
                    advise[user] += 1
                else:
                    advise[user] = 1
            else:
                if user in none_advise:
                    none_advise[user] += 1
                else:
                    none_advise[user] = 1
        
        usernames_1 = [i for i in advise.keys()]
        advise_values = [j for j in advise.values()]
        usernames_2 = [i for i in none_advise.keys()]
        none_advise_values = [j for j in none_advise.values()]
        
        adviseframe = pd.DataFrame({'Username': usernames_1, 'Advice': advise_values})
        adviseframe.set_index('Username', inplace = True)
        none_advise_frame = pd.DataFrame({'Username': usernames_2, 'None-Advise':none_advise_values})
        none_advise_frame.set_index('Username', inplace = True)

        user_network_frame_concat = pd.concat([adviseframe, none_advise_frame], axis=1)
        user_network_frame_concat.to_csv('diabetes\\usernetwork.csv')
       
      
   
training_set = pd.read_csv('diabetes\\diabetes-training-set-numeric.csv')
classify = tweet_training_network_sets(training_set)
classify.training_set()