# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:22:36 2017

@author: Mike
"""
from pymongo import MongoClient
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from operator import itemgetter
import itertools
import re
import pandas as pd
import numpy as np
import collections
import matplotlib.pyplot as plt


class retweetExtract:

    def __init__(self, client, db, dbItems):
        self.__client = client
        self.__db = db
        self.__dbItems = dbItems
          
        
    def retweet_extraction(self):
        retweets = []
        rtFrame = self.process()
        rtFrameList = np.array(rtFrame).tolist()
        tuple_list_users_tweets = [(i[0], i[1]) for i in rtFrameList]
            
        for a,b in itertools.combinations(tuple_list_users_tweets, 2):
            if((a[1] == b[1]) and (a[0] != b[0])):
                if ((a not in retweets) and (b not in retweets)):
                    retweets.append(a)
                    retweets.append(b)
                    
        t = pd.DataFrame({'Retweets':retweets})
        t.set_index('Retweets', inplace=True)
        t.to_csv('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\diabetes\\new_set\\retweets.csv')
        print (len(retweets))    
        
    def process(self):
        #lists to hold filtered tweets and usernames
        filtered_tweet = []
        userNames =[]
        #pre-processing the tweets, filter out special characters, non-words, stemming and duplicates
        try:
            unwanted_char = [ "\n","(\\n)", "#\w+", "http.{1,30}", "[.,;'!?$#&=\+\-\*\/\(\)\|]", 
                             "\nhttps:.{1,30}",  "\u2026", "(&amp)", "("")", "('')"]
            print (type(self.__dbItems))
            for tweet in self.__dbItems:
                cleaned_tweet = tweet['Tweet'].split(' https')[0]
                cleaned_tweet.replace('\n', '')
                unwanted_twitter_users = re.search('(Dr.{1,30})', tweet['User-Name'])
             
                for reg_exp in unwanted_char:
                    x = re.compile(reg_exp, re.VERBOSE | re.IGNORECASE)
                    cleaned_tweet = x.sub("", cleaned_tweet)
                    
                if (unwanted_twitter_users is None):           
                    userNames.append(tweet['User-Name']) 
                    filtered_tweet.append(cleaned_tweet)
                
            cleanedFrame = pd.DataFrame({'Tweets':filtered_tweet, 'Username':userNames}, columns = ['Username', 'Tweets'])
            return cleanedFrame
        
        except Exception as e:
            print(str(e))

#most retweeted tweet
def most_retweeted_tweet():
    retweetFrame = pd.read_csv('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\diabetes\\new_set\\retweets.csv')
    retweet_list = []
    for tupleitem in retweetFrame['Retweets']:
        searchText = tupleitem.split(", '")[1]
        retweet_list.append(searchText[0:-2])
    most_popular_tweets = (dict(collections.Counter(retweet_list).most_common(10)))
    
    plt.bar(range(len(most_popular_tweets)), most_popular_tweets.values(), align='center')
    plt.xticks(range(len(most_popular_tweets)), most_popular_tweets.keys())
    plt.show()
    
#==============================================================================
#     word_count = {} 
#     for word in retweet_list:
#         if word in word_count:
#             word_count[word] += 1
#         else:
#             word_count[word] = 1
#     
#     popular_words = (sorted(word_count.items(), key=itemgetter(1), reverse=True)[:5])
#     print(popular_words)
#==============================================================================
        
#==============================================================================
#         x = re.compile(r"(RT.*)")
#         searchText = re.search(x, tupleitem)
#         if searchText is not None:
#             searchText = re.sub(r"[')]", "", searchText.group(0))
#             retweet_list.append(searchText)
#         
#     print (len(retweet_list))    
#==============================================================================
        

    
#removing stop words and steming text from tweet
def nltk_stop_stem(tweet):
    filtered_sentence = []
    stop_words = set(stopwords.words("english"))
    tokenized_tweet = word_tokenize(tweet)
    for word in tokenized_tweet:
        if word not in stop_words:
            filtered_sentence.append(nltk_lemmatize(word))
    return filtered_sentence

#retreiving a generic term that can represent sever synonyms (lemmatizing)
def nltk_lemmatize(tweet):
    ls = WordNetLemmatizer()
    return (ls.lemmatize(tweet))

#==============================================================================
# #creating a connection to the database 
# db_client = MongoClient()
# db_connect = db_client.ABCi_twitter_analysis_DB
# db_items = db_connect.live_diabetes_tweets.find()
# 
# #exectuion of the class
# tweetfilter = retweetExtract(db_client, db_connect, db_items)
# tweetfilter.retweet_extraction()
#==============================================================================
most_retweeted_tweet()