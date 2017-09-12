# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:22:36 2017

@author: Mike
"""
from tweet_processing import working_directory
from pymongo import MongoClient
import itertools
import re
import pandas as pd
import numpy as np
import collections
import matplotlib.pyplot as plt
working_directory()

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
        #comparing the tweet text and username to identify a retweet, a tweet is a retweet is the text is similar but usernames are differnet    
        for a,b in itertools.combinations(tuple_list_users_tweets, 2):
            if((a[1] == b[1]) and (a[0] != b[0])):
                if ((a not in retweets) and (b not in retweets)):
                    retweets.append(a)
                    retweets.append(b)
                    
        t = pd.DataFrame({'Retweets':retweets})
        t.set_index('Retweets', inplace=True)
        t.to_csv('diabetes\\retweets.csv')
        print (len(retweets))    
        
    def process(self):
        #lists to hold filtered tweets and usernames
        filtered_tweet = []
        userNames =[]
        #pre-processing the tweets, filter out special characters, non-words characters, duplicates and tweets from doctors
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

#plotting the tweets with the most number of retweets
def most_retweeted_tweet():
    retweetFrame = pd.read_csv('diabetes\\retweets.csv')
    retweet_list = []
    twitter_handles = []
    proc = [r'(RT.*:)', r'(\\\\u\w+)', r'(\\\\n)']
    for tupleitem in retweetFrame['Retweets']:
        searchText = tupleitem.split(", '")[1]
        retweet_list.append(searchText[0:-2])
    most_popular_tweets = (dict(collections.Counter(retweet_list).most_common(9)))
    retweet_list.clear()
    for i in list(most_popular_tweets.keys()):
        search_twitter_handle = re.search(r'(@.+:)', i)
        search_twitter_handle = re.sub(r':', '', search_twitter_handle.group())
        twitter_handles.append(search_twitter_handle)
        for exp in proc:
            i = re.sub(exp, '', i)
        retweet_list.append(i)
        print(i)
        
    most_popular_tweets_file = pd.DataFrame({'Tweeter-Handle': twitter_handles, 
                                             'Tweet':retweet_list, 
                                             'Number of retweets': list(most_popular_tweets.values())})
    most_popular_tweets_file.set_index('Tweeter-Handle', inplace=True)
    #most_popular_tweets_file.to_csv('/Volumes/MYKEL/ABCi_Twitter_Analysis/diabetes/new_set/most_popular_tweets.csv')
    
    tweet_keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    bax = plt.subplot2grid((10,1), (0,0), colspan=1, rowspan=10) 
    bax.bar(range(len(most_popular_tweets)), most_popular_tweets.values(), align='center', color='#363363')
    plt.xticks(range(len(most_popular_tweets)), tweet_keys, fontsize=13, color='k')
    bax.set_title('Most Popular Tweets', fontsize=15, color='k')   
    plt.ylabel('No of retweets', fontsize=14, color='k')
    plt.xlabel('Tweet', fontsize=14, color='k')
    j = 250
    
    font = {
        'color':  '#483DEF',
        'size': 12,
        'style': 'italic'
        }
    
    for x,y,z in zip(tweet_keys, twitter_handles, retweet_list):
        plt.text(9, j, 'twitter_handle'+': '+y, fontsize=12  )
        plt.text(9, j-15, x+': '+z, fontdict=font) 
        j -= 30
    
    plt.show()
    

#creating a connection to the database 
db_client = MongoClient()
db_connect = db_client.ABCi_twitter_analysis_DB
db_items = db_connect.live_diabetes_tweets.find()

#exectuion of the class
tweetfilter = retweetExtract(db_client, db_connect, db_items)
tweetfilter.retweet_extraction()
most_retweeted_tweet()