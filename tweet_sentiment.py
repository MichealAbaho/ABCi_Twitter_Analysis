# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 11:13:42 2017

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

def tweet_opinion():
    fh = pd.read_csv('diabetes_tweets_test_file.csv')
    
    advise_associated_items = []
    set_of_TF = []
    word_weight = {}
    tweets = []
    Usernames = []
    
    syns_advise = wordnet.synsets('advise')[1].name()
    
    for user,tweet in zip(fh['Username'], fh['Tweet']):
        tweet = (str(tweet).strip('[]'))
        app_comma = re.compile("[',]")
        tweet = app_comma.sub('', tweet)
        tweet = tweet.split()
        word_weight.clear()       
        for j in tweet:
            j_syns = wordnet.synsets(j)       
            if ((len(j_syns)) != 0):
                j_syns = j_syns[0].name()
                x = wordnet.synset(syns_advise)
                y = wordnet.synset(j_syns)
                sim_weight = (x.wup_similarity(y))
                word_weight[j] = round(sim_weight, 4)
        
        advise_associated_items = sorted(list(word_weight.values()))
        top_three_words = dict(sorted(word_weight.items(), key=itemgetter(1), reverse=True)[:3]) 
        top_three_words = dict((k.lower(), v) for k,v in top_three_words.items())
        top_three_words = list(top_three_words.values())                  
        if(len(advise_associated_items) >= 2):
            term_list = [x for x in advise_associated_items if x >= 0.20]
            term_frequency_weight = (len(term_list)/len(advise_associated_items))
            term_frequency_weight = round(term_frequency_weight, 2)
            set_of_TF.append(term_frequency_weight)
            tweets.append(top_three_words)
            Usernames.append(user)
    
    for i, weight in enumerate(set_of_TF):
        if (weight < 0.25):
            set_of_TF[i] = "not_advise"
        elif (0.25 <= weight < 0.5):
            set_of_TF[i] = "moderately_advise"
        elif (0.5 <= weight < 0.75):
            set_of_TF[i] = "mostly_advise"
        elif (0.75 <= weight <= 1):
            set_of_TF[i] = "purely_advise"
                     
    d = pd.DataFrame({'Username': Usernames,'Tweet':tweets, 'TF-weight':set_of_TF}) 
    d.set_index('Tweet', inplace=True)
    d.to_csv('adv_weka_test_set_file.csv')     
            
#==============================================================================
#             term_frequency_weight = mt.fsum([advise_associated_items[-1], advise_associated_items[-2]])
#             term_frequency_weight = round(term_frequency_weight, 2)
#             if (term_frequency_weight >= 0.45):
#         most_similar_word = max(word_weight, key=word_weight.get)  # Just use 'min' instead of 'max' for minimum.
#            
#         TF = tweet.count(most_similar_word)/len(tweet)
#         p.append(most_similar_word)
#         set_of_TF.append(TF)
#==============================================================================
    
    

#==============================================================================
# def pos_neg_opinion():
#     fh = pd.read_csv('rheum_tweets_analysis_file.csv')
#     neg_words = word_tokenize(opinion_lexicon.raw('negative-words.txt'))
#     pos_words = word_tokenize(opinion_lexicon.raw('positive-words.txt'))
#     positive_tweets = []
#     negative_tweets = []
#     
#     p = []
#     n = []
#     weight = []
#     
#     for tweet in fh['Tweet']:
#         tweet = (str(tweet).strip('[]'))
#         current_p_length = len(p)
#         current_n_length = len(n)
#         app_comma = re.compile(r"[',]")
#         tweet = app_comma.sub('', tweet)
#         tweet = tweet.split()
# 
#         for j in tweet:
#             if j in pos_words:
#                 p.append(j)
#             elif j in neg_words:
#                 n.append(j)
#         pos_word_length = len(p) - current_p_length
#         neg_word_length = len(n) - current_n_length
#        
#         if(pos_word_length > neg_word_length):
#             weight.append('positive')
#             positive_tweets.append(tweet)
#         elif(neg_word_length > pos_word_length):
#             weight.append('negative')
#             positive_tweets.append(tweet)
#     
#     px = pd.DataFrame({'positive-tweets': positive_tweets, 'Weight':weight})
#     px.set_index('positive-tweets', inplace = True)
#     px.to_csv('positive-tweets1.csv')
#==============================================================================
    
#==============================================================================
#     for tweet in fh['Tweet']:
#         tweet = (str(tweet).strip('[]'))
#         current_p_length = (len(p))
#         app_comma = re.compile(r"[',]")
#         tweet = app_comma.sub('', tweet)
#         tweet = tweet.split()
# 
#         for j in tweet:
#             if j in pos_words:
#                 p.append(j)
#         new_length = (len(p) - current_p_length)
#        
#         if((new_length) == 1):
#             weight.append(1)
#             positive_tweets.append(tweet)
#         elif((new_length) == 2):
#             weight.append(2)
#             positive_tweets.append(tweet)
#         elif((new_length) >= 3):
#             weight.append(3)
#             positive_tweets.append(tweet)
#     
#     px = pd.DataFrame({'positive-tweets': positive_tweets, 'Weight':weight})
#     px.set_index('positive-tweets', inplace = True)
#     px.to_csv('positive-tweets.csv')
#==============================================================================
        
    

def themes_synonyms():
    advice = []
    complain = []

    theme1 = wordnet.synsets('Advice')
    theme2 = wordnet.synsets('Complain')
    theme3 = wordnet.synsets('Unhappy')
    
    for syn in theme1:
        for x in syn.lemmas():
            advice.append(x.name())
    for syn in theme2:
        for x in syn.lemmas():
            complain.append(x.name())
    for syn in theme3:
        for x in syn.lemmas():
            complain.append(x.name())
    
    return (advice, complain)
    
def similarity():
    w1.wup_similarity(w2rt)
    print (themes_synonyms()[1])

tweet_opinion()