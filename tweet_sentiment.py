# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 11:13:42 2017

@author: Mike
"""
from nltk.corpus import wordnet
from operator import itemgetter
from tweet_processing import tokens_to_list
import pandas as pd

class tweet_opinion:
    
    def __init__(self, file, key_term):
        self.__file = file
        self.__key_term = key_term
        
    def opinion(self):
        # declare variables lists and dictionaries as repositories for data manipulated     
        advise_associated_items = []
        set_of_TF = []
        word_weight = {}
        tweets = []
        original_tweets = []
        Usernames = []
        
        #access just usernames and tweet tokens         
        for user,tweet in zip(self.__file['Username'], self.__file['Tweet']):
            tweet = tokens_to_list(tweet)
            word_weight.clear()       
            for word in tweet:
                '''checks synonyms of a word in a tweet from wordnet corpus, and compares each synonym to the advise key word, then retains
                the maximum textual similarity weight, then adds the word and this weight as key value for a dictionary'''
                word_syns = wordnet.synsets(word)                               
                if ((len(word_syns)) != 0):                                     
                    word_syns = word_syns[0].name()
                    x = wordnet.synset(self.__key_term)
                    y = wordnet.synset(word_syns)
                    sim_weight = (x.wup_similarity(y))
                    word_weight[word] = round(sim_weight, 4)
            
            #re-arranges obtained dictionary from above and retains the top three keys with largest values
            advise_associated_items = sorted(list(word_weight.values()))
            top_three_words = dict(sorted(word_weight.items(), key=itemgetter(1), reverse=True)[:3]) 
            top_three_words = dict((k.lower(), v) for k,v in top_three_words.items())
            top_three_words = list(top_three_words.values())  
            
            '''each traversed tweet must contain a minumum of two words otherwise, it's dropped from the set, then the Term Frequency(TF-IDF) of the 
            top three values is obtained by dividing the number of times they appear by the length of tweet. A thresh hold of two is used
            to filter out the weights that are below 0.20, thus final three words are considered most similar to the key term advise'''
            if(len(advise_associated_items) >= 2):
                term_list = [x for x in advise_associated_items if x >= 0.20]
                term_frequency_weight = (len(term_list)/len(advise_associated_items))
                term_frequency_weight = round(term_frequency_weight, 2)
                set_of_TF.append(term_frequency_weight)
                tweets.append(top_three_words)
                Usernames.append(user)
                original_tweets.append(tweet)
                
        #classify the tweets into four separate weights
        for i, weight in enumerate(set_of_TF):
            if (weight < 0.25):
                set_of_TF[i] = "not_advise"
            elif (0.25 <= weight < 0.5):
                set_of_TF[i] = "moderately_advise"
            elif (0.5 <= weight < 0.75):
                set_of_TF[i] = "mostly_advise"
            elif (0.75 <= weight <= 1):
                set_of_TF[i] = "purely_advise"
        
        #output a frame containing each tweet, the assigned TF-IDF weights, the class and original tweet for cross checking                
        d = pd.DataFrame({'Username': Usernames, 'Weights':tweets, 'Original_tweets': original_tweets, 'Class':set_of_TF}) 
        d.set_index('Username', inplace=True)
        d.to_csv('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\rheumatoid-training-set.csv')     
            
fh = pd.read_csv('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\rheumatoid-tweets-analysis.csv')
syns_advise = wordnet.synsets('advise')[1].name()
sentiment = tweet_opinion(fh, syns_advise)
sentiment.opinion()