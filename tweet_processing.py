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

client = MongoClient()
db = client.ABCi_twitter_analysis_DB
def processTweets():

    dbItems = db.live_diabetes_tweets.find()
    filtered_tweet = []
    userNames =[]
    
    try:
        unwanted_char = [ "\n","(\\n)", "#\w{1,10}", "http.{1,30}", "[.,;:'!?$#&\+\-\*\/\(\)\|\d{1,3}]", "@[\w]{1,15}",
                         "\nhttps:.{1,30}",  "\u2026", "RT", "(&amp)", "("")", "('')"]
        
        other_hastags_file = open('Other_hashtags.txt', 'a+')
        for tweet in dbItems:
            cleaned_tweet = tweet['Tweet'].split(' https')[0]
            cleaned_tweet.replace('\n', '')
            unwanted_twitter_users = re.search('(Dr.{1,30})', tweet['User-Name'])
            other_hastags_file.write(otherthemes(cleaned_tweet))
            for reg_exp in unwanted_char:
                x = re.compile(reg_exp, re.VERBOSE | re.IGNORECASE)
                cleaned_tweet = x.sub("", cleaned_tweet)
                
            tweet_broken_down = nltk_stop_stem(cleaned_tweet)
            if ((tweet_broken_down not in filtered_tweet) and (unwanted_twitter_users is None) and (len(tweet_broken_down) < 200)):           
                userNames.append(tweet['User-Name']) 
                filtered_tweet.append(tweet_broken_down)
            
        rheum_analysisFrame = pd.DataFrame({'Username': userNames, 'Tweet':filtered_tweet})
        rheum_analysisFrame.set_index('Username', inplace=True)
        rheum_analysisFrame.to_csv('diabetes_tweets_test_file.csv')      
            
    except Exception as e:
        print(str(e))

#removing stop words and steming text from tweet
def nltk_stop_stem(tweet):
    filtered_sentence = []
    stop_words = set(stopwords.words("english"))
    tokenized_tweet = word_tokenize(tweet)
    for word in tokenized_tweet:
        if word not in stop_words:
            filtered_sentence.append(nltk_lemmatize(word))
    return filtered_sentence

#getting the root version of specific terms
def nltk_stemming(token):
    ps = PorterStemmer()
    return ps.stem(token)

def nltk_lemmatize(tweet):
    ls = WordNetLemmatizer()
    return (ls.lemmatize(tweet))

def otherthemes(tweet):
    hashtags = (r'#\w+')
    other_mentioned_hashtags = re.findall(hashtags, tweet)
    other_mentioned_hashtags = str(other_mentioned_hashtags).strip('[]')
    return other_mentioned_hashtags
    

processTweets()



    

    