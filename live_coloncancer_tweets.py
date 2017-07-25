# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 16:19:05 2017

@author: Mike
"""
import tweepy 
from pymongo import MongoClient
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from datetime import datetime 
import time

consumer_key = "B0O6b0tyHMNTQe0KBh6VV2S6m"
consumer_secret = "BZX2vZKQX8eyL2jjvcpr6kXkqP9mPXrR1b26N54dz2hx6MUYb6"
access_token = "119014719-F7ne0FH2ntxRbllIzFvw3A44fYYyXPfJQfTGkb9d"
access_secret = "sA3jT2AT2wrIvahDB1Zkh8elX99I9urvBOVg6EShOowQi"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

clientConnect = MongoClient()
db = clientConnect.ABCi_twitter_analysis_DB

class diabetesStream(StreamListener):
    
    def on_data(self, data):
        try:
            diabetes_tweet_text = data.split(',"text":"')[1].split('","source')[0]
            diabetes_tweeter = data.split(',"name":"')[1].split('","screen_name')[0]
            diabetes_tweet_loc = data.split(',"location":"')[1].split('","url')[0]
            diabetes_tweet_time = datetime.now().time()
            diabetes_tweet_date = datetime.now().date()
            cleanedTime = diabetes_tweet_time.strftime('%H:%M:%S')
            cleanedDate = diabetes_tweet_date.strftime('%d/%m/%Y')
            
            
            db.live_coloncancer_tweets.insert_many([{
                "User-Name":diabetes_tweeter,
                "Location": diabetes_tweet_loc,
                "Date":cleanedDate,
                "Time":cleanedTime,
                "Tweet":diabetes_tweet_text
                }])
            
            
            print ("succesfully stored")

            return True
        except (BaseException) as e:
            print ('Data not being collected', e)
            time.sleep(5)
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
tweet_Stream = Stream(auth, diabetesStream())
tweet_Stream.filter(track=['#coloncancer'], languages=["en"])
    