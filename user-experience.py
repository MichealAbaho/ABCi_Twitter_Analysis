# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 13:10:42 2017

@author: Mike
"""
from nltk.corpus import opinion_lexicon
from nltk.tokenize import word_tokenize
import re
import pandas as pd

def user_exp_opinion():
    fh = pd.read_csv('diabetes-tweets-analysis.csv')

    tweets = []
    usernames = []
    
    interested_characters = ['dr', 'doc', 'nhs', 'gp', 'hospital', 'doctor', "doctor's"]
    for user,tweet in zip(fh['Username'], fh['Tweet']):
        tweet = (str(tweet).strip('[]'))
        app_comma = re.compile("[',]")
        tweet = app_comma.sub('', tweet)
        tweet = tweet.split()
        tweet = [i.lower() for i in tweet]
        
        shared_items = [x for x in tweet if x in interested_characters]

        if(len(shared_items) != 0):
            tweets.append(tweet)
            usernames.append(user)
            
    return (pd.DataFrame({'Username': usernames, 'Tweets': tweets}))      

def comp_satisfied():
    
    users_series = user_exp_opinion()['Username']
    tweet_series = user_exp_opinion()['Tweets']
    set_of_pos = word_tokenize(opinion_lexicon.raw('positive-words.txt'))
    set_of_neg = word_tokenize(opinion_lexicon.raw('negative-words.txt'))
    tweet_positive_words = []
    tweet_negative_words = []
    tweets = []
    Username = []
    sentiment = []

    try:
        for user,tweet in zip(users_series, tweet_series):
            current_tpw_length = len(tweet_positive_words)
            current_tnw_length = len(tweet_negative_words)
            for word in tweet:
                if word in set_of_pos:
                    tweet_positive_words.append(word)
                elif word in set_of_neg:
                    tweet_negative_words.append(word)
            
            new_tpw_length = len(tweet_positive_words) - current_tpw_length
            new_tnw_length = len(tweet_negative_words) - current_tnw_length                    
            
            if (new_tpw_length >= 2):
                sentiment.append('Pos')
            elif(new_tnw_length >= 3):
                sentiment.append('Neg')
            else:
                sentiment.append('Neutral')
            tweets.append(tweet)
            Username.append(user)
        
        sentiFrame = pd.DataFrame({'Username':Username, 'Tweet':tweets,'Sentiment':sentiment})
        sentiFrame.set_index('Username', inplace=True)
        sentiFrame.to_csv('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\diabetes\\new_set\\user-experience2.csv')                        
    except Exception as e:
        print (str(e))    


comp_satisfied()
        


                
                     
    