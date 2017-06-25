# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 13:50:58 2017

@author: Mike
"""
import nltk
import json
from pymongo import MongoClient
import pandas as pd


client = MongoClient()
db = client.ABCi_twitter_analysis_DB

dbItem = db.live_rheum_tweets.find()
userNames = []
tweetText = []

for tweet in dbItem:
    userNames.append(tweet['User-Name'])
    tweetText.append(tweet['Tweet'])
    words = nltk.word_tokenize(tweet['Tweet'])
    named_ent = nltk.ne_chunk(words)
    named_ent.draw()
    break

#==============================================================================
# list_of_tweets = pd.DataFrame({'User-Name': userNames, 'Tweet': tweetText})
# list_of_tweets.set_index('User-Name', inplace=True)
# list_of_tweets.to_csv('rheumanalysis1.csv')
#==============================================================================
    