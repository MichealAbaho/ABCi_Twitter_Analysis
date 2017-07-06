# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 13:50:18 2017

@author: Mike
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import collections
style.use('ggplot')

def generatWordCloud():
    
    rd = pd.read_csv('advfinal_training_set_file.csv')
    counter = collections.Counter(rd['Username'])
    frequent_tweeters = (counter.most_common()[:20])
    font = {
        'color':  'black',
        'size': 13,
        'weight': 'normal'
        }
#==============================================================================
#     userplot = plt.subplot2grid((1,1), (0,0))
#     userplot.bar(range(len(frequent_tweeters)), [val[1] for val in frequent_tweeters])
#     userplot.set_title('Frequent Twitters under the topic #diabetes')
#     plt.ylabel('Occurrence')
#     userplot.set_xticklabels(range(len(frequent_tweeters)),[val[0] for val in frequent_tweeters])
#==============================================================================

    plt.bar(range(len(frequent_tweeters)), [val[1] for val in frequent_tweeters])
    plt.xticks(range(len(frequent_tweeters)),[val[0] for val in frequent_tweeters])
    plt.tick_params(axis='x', length=5, right='off', pad = -3)
    plt.xticks(rotation=70,ha='center')
    plt.ylabel('Occurrences')
    plt.title('Frequent Twitters under the topic #diabetes')
    plt.show()
    
generatWordCloud()