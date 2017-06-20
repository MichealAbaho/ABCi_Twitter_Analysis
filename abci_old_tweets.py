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
import pandas as pd

consumer_key = "U7Tn8KhB97G91D748zGTfqK0Z"
consumer_secret = "1iIxxiQESAacaUy0vn3Git9D5MDP9WJtiwlmI5zYl06NU2dZK3"
access_token = "119014719-V9cE1ukf008v6eUSAmfN0LDEIUpMs9wEKJcHdznH"
access_secret = "qshdRpZ2jKq7CCYkCarr5ZYjqtxGnAZhwyNPFn010b0a4"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
try:
    public_tweets = api.search(q="#rheum", count=1000, lang="en", result_type="recent", until="2017-06-19")
    userName = []
    location = []
    date_time = []
    tweetText = []
    
    for tweets in public_tweets:
        userName.append(tweets.user.name)
        location.append(tweets.user.location)
        date_time.append(tweets.created_at)
        tweetText.append(tweets.text)
        print (tweets.text)
    
    oldTweetsFrame = pd.DataFrame({'User-Name': userName, 'Location': location, 'Date_Time':date_time, 'Tweet':tweetText})
    oldTweetsFrame.set_index('User-Name', inplace=True)
    oldTweetsFrame.to_csv('d.csv')

except (BaseException) as e:
    print ("cannot retreive tweets", e)

        


    


