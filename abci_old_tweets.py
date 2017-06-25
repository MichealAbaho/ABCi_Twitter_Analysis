# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:23:35 2017

@author: Mike
"""

import tweepy 
import pandas as pd
import pymongo
from pymongo import MongoClient

consumer_key = "U7Tn8KhB97G91D748zGTfqK0Z"
consumer_secret = "1iIxxiQESAacaUy0vn3Git9D5MDP9WJtiwlmI5zYl06NU2dZK3"
access_token = "119014719-V9cE1ukf008v6eUSAmfN0LDEIUpMs9wEKJcHdznH"
access_secret = "qshdRpZ2jKq7CCYkCarr5ZYjqtxGnAZhwyNPFn010b0a4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
#==============================================================================
# instantiating a conection to the db
#==============================================================================
#==============================================================================
# clientConnect = MongoClient()
# db = clientConnect.ABCi_twitter_analysis_DB
#==============================================================================

api = tweepy.API(auth)
try:
    public_tweets = api.search(q="#rheum", count=1000, lang="en", result_type="recent", until="2017-06-20")
    userName = []
    location = []
    tweet_date = []
    tweet_time = []
    tweetText = []
    
    for tweets in public_tweets:
        userName.append(tweets.user.name)
        location.append(tweets.user.location)
        tweet_date.append(str((tweets.created_at).date()))
        tweet_time.append(str((tweets.created_at).time()))
        tweetText.append(tweets.text)
        print ((tweets.text))
#==============================================================================
#     creatin a collection and storing tweets by username, location, time and text   
#==============================================================================
#==============================================================================
#     db.rheum_tweets.drop()  
#     oldRheumTweets = {
#         "User-Name":userName,
#         "Location":location,
#         "Date":tweet_date,
#         "Time":tweet_time,
#         "Tweet":tweetText
#     }   
#     db.rheum_tweets.insert_many([oldRheumTweets])
#     clientConnect.close()
#==============================================================================
#==============================================================================
#     storing the tweets in a local file
#==============================================================================
    oldTweetsFrame = pd.DataFrame({'User-Name': userName, 'Location': location, 'Date':tweet_date, 'Time':tweet_time, 'Tweet':tweetText})
    oldTweetsFrame.set_index('User-Name', inplace=True)
    oldTweetsFrame.to_csv('rheum_tweets2.csv')
    
except (BaseException, IOError, ValueError, TypeError) as e:
    print ("cannot retreive tweets", e)

 


    


