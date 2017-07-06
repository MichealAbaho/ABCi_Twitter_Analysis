# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 13:10:42 2017

@author: Mike
"""
from nltk.corpus import wordnet, opinion_lexicon
from nltk.tokenize import word_tokenize
from itertools import product
from operator import itemgetter
import numpy as np
import re
import pandas as pd
import math as mt

def user_exp_opinion():
    fh = pd.read_csv('diabetes_tweets_test_file.csv')

    tweets = []
    Usernames = []
    
    interested_characters = ['dr', 'doc', 'nhs', 'gp', 'hospital', 'covered', 'trumpcare', 'doctor', "doctor's"]
    for user,tweet in zip(fh['Username'], fh['Tweet']):
        tweet = (str(tweet).strip('[]'))
        app_comma = re.compile("[',]")
        tweet = app_comma.sub('', tweet)
        tweet = tweet.split()
        tweet = [i.lower() for i in tweet]
        
        shared_items = [x for x in tweet if x in interested_characters]

        if(len(shared_items) != 0):
            tweets.append(tweet)
            
    return (pd.DataFrame({'Tweets': tweets}))      

def comp_satisfied():
    exp_tweets = []
    set_of_exp = []
    satisfy_word_weight = {}
    dissap_word_weight = {}
    syns_satisfy = wordnet.synsets('satisfy')[0].name()
    syns_disapointment = wordnet.synsets('disappointment')[0].name()
    
    
    for tweet in user_exp_opinion()['Tweets']:
        satisfy_word_weight.clear()
        dissap_word_weight.clear()
        for j in tweet:
            j_syns = wordnet.synsets(j)
            
            if (len(j_syns) != 0):
                j_syns = j_syns[0].name()
                x = wordnet.synset(syns_satisfy)
                y = wordnet.synset(syns_disapointment)
                z = wordnet.synset(j_syns)
                
                s_sim_weight = (x.wup_similarity(z))
                d_sim_weight = (y.wup_similarity(z))
                
                if ((s_sim_weight is not None) and (d_sim_weight is not None)):
                    satisfy_word_weight[j] = round(s_sim_weight, 4)
                    dissap_word_weight[j] = round(d_sim_weight, 4)
                        
        if((np.sum([len(satisfy_word_weight), len(dissap_word_weight)])) >= 6):
            top_three_satisfy = dict(sorted(satisfy_word_weight.items(), key=itemgetter(1), reverse=True)[:3]) 
            top_three_disappoint = dict(sorted(dissap_word_weight.items(), key=itemgetter(1), reverse=True)[:3])
            sum_satisfy = mt.fsum(list(top_three_satisfy.values()))    
            sum_disapoint = mt.fsum(list(top_three_disappoint.values()))
            
            if (sum_satisfy > sum_disapoint):
                set_of_exp.append('satisfied')
                exp_tweets.append(list(top_three_satisfy.keys()))
            elif (sum_disapoint > sum_satisfy):
                set_of_exp.append('dissapointed')
                exp_tweets.append(list(top_three_disappoint.keys()))
                    
    d = pd.DataFrame({'Tweet':exp_tweets, 'Experience':set_of_exp}) 
    d.set_index('Tweet', inplace=True)
    d.to_csv('User_exp_set_file.csv')     


comp_satisfied()
        


                
                     
    