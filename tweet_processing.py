# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 13:50:58 2017

@author: Mike
"""

from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import pandas as pd
import re
import os


class processTweets:

    def __init__(self, client, db, dbItems):
        self.__client = client
        self.__db = db
        self.__dbItems = dbItems
    
    def process(self):
        #lists to hold filtered tweets and usernames
        filtered_tweet = []
        userNames =[]     
        working_directory()
        #pre-processing the tweets, filter out special characters, non-words, stemming and duplicates
        try:
            unwanted_char = [ "\n", "(\\n)", "#\w+", "http.{1,30}", "[.,;:'!?$#&=\+\-\*\/\(\)\|\d{1,3}]", "@\w+",
                             "\nhttps:.{1,30}",  "\u2026", "RT", "(&amp)", "("")", "('')"]
            
            #file tostore all hash tags
            other_hastags_file = open('diabetes\\diabetes-hashtags.txt', 'a+')
            unwanted_hasthtags = ['#diabetes', '#diabetics', "#diabetic"]
            for tweet in self.__dbItems:
                cleaned_tweet = tweet['Tweet'].split(' https')[0]
                unwanted_twitter_users = re.search('(Dr.{1,30})', tweet['User-Name'])
                hashtags_mentions = otherthemes(cleaned_tweet)
                for hashtag in hashtags_mentions:
                    if (hashtag.lower() not in unwanted_hasthtags):
                        other_hastags_file.write(hashtag)
                        other_hastags_file.write(' ')
                for reg_exp in unwanted_char:
                    x = re.compile(reg_exp, re.VERBOSE | re.IGNORECASE)
                    cleaned_tweet = x.sub("", cleaned_tweet)
                    
                tweet_broken_down = nltk_stop_stem(cleaned_tweet)
                if ((tweet_broken_down not in filtered_tweet) and (unwanted_twitter_users is None)):           
                    userNames.append(tweet['User-Name']) 
                    filtered_tweet.append(tweet_broken_down)
            
            #other_hastags_file.close()
            analysisFrame = pd.DataFrame({'Username': userNames, 'Tweet':filtered_tweet})
            analysisFrame.set_index('Username', inplace=True)
            analysisFrame.to_csv('diabetes\\diabetes-tweets-analysis.csv')      
            #other_hastags_file.close()        
        except Exception as e:
            print(str(e))

#changing default working directory to a directory easily accessed
def working_directory():
    current_wd = os.getcwd()
    return current_wd

#removing stop words and steming text from tweet
def nltk_stop_stem(tweet):
    filtered_sentence = []
    stop_words = set(stopwords.words("english"))
    tokenized_tweet = word_tokenize(tweet)
    for word in tokenized_tweet:
        if nltk_stemming(word).lower() not in stop_words:
            filtered_sentence.append(nltk_lemmatize(word))
    return filtered_sentence

#getting the root version of specific terms
def nltk_stemming(token):
    ps = PorterStemmer()
    return ps.stem(token)

#retreiving a generic term that can represent sever synonyms (lemmatizing)
def nltk_lemmatize(tweet):
    ls = WordNetLemmatizer()
    return (ls.lemmatize(tweet))

#extracting all hastags that are mentioned in a tweet
def otherthemes(tweet):
    hashtags = (r'(#\w+)')
    other_mentioned_hashtags = re.findall(hashtags, tweet)
    return other_mentioned_hashtags

#creating a list of tokens by to allow independent token manipulation
def tokens_to_list(tweettokens):
    tweet = (str(tweettokens).strip('[]'))
    app_comma = re.compile("[',]")
    tweet = app_comma.sub('', tweet)
    tweet = tweet.split()
    return tweet

#creating a connection to the database 
db_client = MongoClient('localhost', 27017)
db_connect = db_client['ABCi_twitter_analysis_DB']
db_items = db_connect['live_diabetes_tweets'].find()
tweetfilter = processTweets(db_client, db_connect, db_items)
tweetfilter.process()



    

    