# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 13:50:18 2017

@author: Mike
"""
from os import path
from wordcloud import WordCloud
import pandas as pd
import re
import nltk
import matplotlib.pyplot as plt

def generatWordCloud():
    newStr = []
    rheumTextFile = open('rheum_text_file.txt', 'a+')
    rheumData = pd.read_csv('rheum_tweets_analysis_file.csv')
    
    for i in rheumData['Tweet']:
        splitTweetText = (str(i).strip('[]'))
        rheumTextFile.write(splitTweetText)
        newStr.append(splitTweetText)
    
    rheumTextFile.close()
    
    fh = open('rheum_text_file.txt', 'r+')
    rheum_cloud_text = fh.readlines()
    
    for line in rheum_cloud_text:
        words = line.split()
        
    x = nltk.FreqDist(words)
    z = nltk.FreqDist(rheumData['Username'])
    print(x.most_common(20), '\n')
    print(z.most_common(20))
    
#==============================================================================
#     rheum_cloud = WordCloud().generate(rheum_cloud_text)
#     plt.imshow(rheum_cloud, interpolation='bilinear')
#     plt.axis('off')
#     
#     rheum_cloud = WordCloud(max_font_size=40).generate(rheum_cloud_text)
#     plt.figure()
#     plt.imshow(rheum_cloud_text, interpolation='bilinear')
#     plt.axis('off')
#     plt.show()
#     
#==============================================================================
    
        
#==============================================================================
#         strings.append(spacingTweetText)
#         rheumTextFile.write(spacingTweetText)
#     rheumTextFile.close()
#==============================================================================
    
generatWordCloud()