# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 18:42:53 2017

@author: Mike
"""
import tweepy 
import db_connect
from db_connect import dbConnection
from pymongo import MongoClient

consumer_key = "LhYrTXI16wFmjHe1S8ETRClYF"
consumer_secret = "LggyxddfiaWAermrHJ35VYc4p8Fve7QajVpN6WvsM5V61S0MnG"
access_token = "119014719-aAtMNFuvLgf49wd6CukwfmEgXJgRGrNICyZPAyuA"
access_secret = "CX9GdbgCovWKS5xB8D2Nxbpt6xWhYOEQjBn1brwaWBSu1"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
#==============================================================================
# instantiating a conection to the db
#==============================================================================
clientConnect = MongoClient()
db_Connection = clientConnect.ABCi_twitter_analysis_DB

api = tweepy.API(auth)
try:
    public_tweets = api.search(q="#diabetes", count=400, lang="en", result_type="recent", until="2017-06-22")
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
    
    oldDiabetesTweets = {
         "User-Name":userName,
         "Location":location,
         "Date":tweet_date,
         "Time":tweet_time,
         "Tweet":tweetText
     } 
    db_Connection.diabetes_tweets.insert_many([oldDiabetesTweets])
    
#==============================================================================
#   
#==============================================================================
#==============================================================================
#     oldTweetsFrame = pd.DataFrame({'User-Name': userName, 'Location': location, 'Date':tweet_date, 'Time':tweet_time, 'Tweet':tweetText})
#     oldTweetsFrame.set_index('User-Name', inplace=True)
#     oldTweetsFrame.to_csv('diabetes_tweets.csv')
#==============================================================================
    
except (BaseException, IOError, ValueError, TypeError) as e:
    print ("cannot retreive tweets", e)