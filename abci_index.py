# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:23:35 2017

@author: Mike
"""
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time

consumer_key = "U7Tn8KhB97G91D748zGTfqK0Z"
consumer_secret = "1iIxxiQESAacaUy0vn3Git9D5MDP9WJtiwlmI5zYl06NU2dZK3"
access_token = "119014719-V9cE1ukf008v6eUSAmfN0LDEIUpMs9wEKJcHdznH"
access_secret = "qshdRpZ2jKq7CCYkCarr5ZYjqtxGnAZhwyNPFn010b0a4"

#==============================================================================
# api = tweepy.API(auth)
# 
# public_tweets = api.home_timeline()
# for tweets in public_tweets:
#     print (t.text)
#==============================================================================

class diseaseCommListener(StreamListener):
    
    def on_data(self, data):
        try:
            rheumTweets = data.split(',"text":"')[1].split('","source')[0]
            print (rheumTweets)
            rheumCleanedTweets = str(time.time())+'::'+rheumTweets
            rheumFile = open('rheum_tweets1.csv', 'a')
            rheumFile.write(rheumCleanedTweets)
            rheumFile.close()
            return True
        except (BaseException) as e:
            print ('Data not being collected', e)
            time.sleep(5)
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
tweet_Stream = Stream(auth, diseaseCommListener())
tweet_Stream.filter(track=['#rheum'])

    


