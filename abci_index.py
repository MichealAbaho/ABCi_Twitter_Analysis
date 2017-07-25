# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:23:35 2017

@author: Mike
"""
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from datetime import datetime 
from pymongo import MongoClient
import time

consumer_key = "U7Tn8KhB97G91D748zGTfqK0Z"
consumer_secret = "1iIxxiQESAacaUy0vn3Git9D5MDP9WJtiwlmI5zYl06NU2dZK3"
access_token = "119014719-V9cE1ukf008v6eUSAmfN0LDEIUpMs9wEKJcHdznH"
access_secret = "qshdRpZ2jKq7CCYkCarr5ZYjqtxGnAZhwyNPFn010b0a4"

clientConnect = MongoClient()
db = clientConnect.ABCi_twitter_analysis_DB

class diseaseCommListener(StreamListener):
    
    def on_data(self, data):
        try:
            rheum_tweet_text = data.split(',"text":"')[1].split('","source')[0]
            rheum_tweeter = data.split(',"name":"')[1].split('","screen_name')[0]
            rheum_tweet_loc = data.split(',"location":"')[1].split('","url')[0]
            rheum_tweet_time = datetime.now().time()
            rheum_tweet_date = datetime.now().date()
            cleanedTime = rheum_tweet_time.strftime('%H:%M:%S')
            cleanedDate = rheum_tweet_date.strftime('%d/%m/%Y')
            
            
            db.live_rheum_tweets.insert_many([{
                "User-Name":rheum_tweeter,
                "Location": rheum_tweet_loc,
                "Date":cleanedDate,
                "Time":cleanedTime,
                "Tweet":rheum_tweet_text
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
tweet_Stream = Stream(auth, diseaseCommListener())
tweet_Stream.filter(track=['#rheum, #ra, #rheumatoid'], languages=["en"])


    


