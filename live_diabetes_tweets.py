# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 15:08:57 2017

@author: Mike
"""
from pymongo import MongoClient
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from datetime import datetime 
import time

consumer_key = "LhYrTXI16wFmjHe1S8ETRClYF"
consumer_secret = "LggyxddfiaWAermrHJ35VYc4p8Fve7QajVpN6WvsM5V61S0MnG"
access_token = "119014719-aAtMNFuvLgf49wd6CukwfmEgXJgRGrNICyZPAyuA"
access_secret = "CX9GdbgCovWKS5xB8D2Nxbpt6xWhYOEQjBn1brwaWBSu1"


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
            
            
            db.live_diabetes_tweets.insert_many([{
                "User-Name":diabetes_tweeter,
                "Location": diabetes_tweet_loc,
                "Date":cleanedDate,
                "Time":cleanedTime,
                "Tweet":diabetes_tweet_text
                }])
            
            
            print ("succesfully stored")
#             rheumFile.write(data)
#             rheumFile.close()
#==============================================================================
            return True
        except (BaseException) as e:
            print ('Data not being collected', e)
            time.sleep(5)
    
    def on_error(self, status):
    	if(status == 420):
    		print ("Just encountered an error on connection")
    		return False
        	
        
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
tweet_Stream = Stream(auth, diabetesStream())
tweet_Stream.filter(track=['#diabetes, #diabetic, #diabetics'], languages=["en"], async=True)
    