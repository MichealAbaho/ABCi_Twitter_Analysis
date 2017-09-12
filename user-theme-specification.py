# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 15:40:07 2017

@author: Mike
"""
import re
import pandas as pd
import numpy as np
import itertools
import jellyfish as jf
from operator import itemgetter
import matplotlib.pyplot as plt
from matplotlib import style


style.use('ggplot')


def match_users_to_themes():
    key_terms = open('diabetes\\diabetes_key_themes.txt', 'r').read()
    key_terms_list = re.findall(r"('.*?')", key_terms)
    print(len(key_terms_list))
    key_terms_list = list(set(key_terms_list))
    print (len(key_terms_list))
    
    related_terms = match_key_terms(key_terms_list)
    
    for duplicate in key_terms_list:
        if duplicate in related_terms:
            key_terms_list.remove(duplicate)
    
    print (len(key_terms_list))
    
    entire_corpus = pd.read_csv('diabetes\\diabetes-training-set-text.csv')
    entire_corpus = np.array(entire_corpus)
    entire_corpus.tolist()
    
    top_ten_dictionary = top_users_and_terms(key_terms_list, entire_corpus)
    top_ten_dict_frame = matrix_users_topic(top_ten_dictionary)
    top_ten_dict_frame.to_csv('diabetes\\diabetes_key_term_twitters.csv')
         
    print (len(top_ten_dictionary))
        
    top_ten_dict_frame['user_total_tweets'] = top_ten_dict_frame.sum(axis = 1)
    sort_top_ten_dict_frame = top_ten_dict_frame.sort_values(['user_total_tweets'], ascending=False)
    summarisedFrame = sort_top_ten_dict_frame.head(n=15)
    
    print (summarisedFrame['user_total_tweets'])
    
    try:
   
        matrix_of_toptwitters_topics = pd.DataFrame()
        
        matrix_of_toptwitters_topics['Diabetes-Research'] = (summarisedFrame[['clinical trial','diabetes research', 
                       'recent study','durable versatile wearable diabetes','bioengineers','fact','research','researchers','scientists']].sum(axis=1))
        
        matrix_of_toptwitters_topics['Diabetes-social-networks'] = (summarisedFrame[['dblog', 'great blog', 'diabetes blog','digitalhealth','facebook',
                                    'instagram','share story','video','youtube']].sum(axis=1))
        
        matrix_of_toptwitters_topics['Manage-Diabetes'] = (summarisedFrame[['yoga','tips','team cured diabetes mice','suppo','reverse diabetes',
                       'diet','fight diabetes','manage']].sum(axis=1))
    
        matrix_of_toptwitters_topics['Diabetes_Educative_Information'] = (summarisedFrame[['study','awareness diabetes','diabetes tech','diabetes educator','diabetic neuropathy',
                       'learn','medical news','news','prediabetes','prevention','diabetes prediabetes','diabetes prevention','diabetes prevention program', 'aade'
                       ]].sum(axis=1))
        
        matrix_of_toptwitters_topics['Diabetes_Medication_Treatment'] = (summarisedFrame[['vitamin','viagra','treat type diabetes','pharma','onetouch ultra',
                       'metformin','afrezza','aificial pancreas','blue diabetic','broccoli','diabetes permanent cure','cure diabetes',
                       'team cured diabetes mice','diabetes doc','diabetes drug','drug','device','diabetes medication']].sum(axis=1))
        
        matrix_of_toptwitters_topics['Diabetes_campaigns_programmes'] = (summarisedFrame[['urgent international mobilization diabetes',
                       'thursdaythoughts','protection people diabetes state','lions','languagematters','diagnosis care amp',
                       'commission diabetes subsaharan','bcra']].sum(axis=1))
    
        matrix_of_toptwitters_topics['Diabetes_disease'] = (summarisedFrame[['type type diabetes','people type diabetes','type diabetes',
                       'type diabetes risk','symptoms','blood sugar','blood sugar level','stick diabetes','risk diabetes','obesity',
                       'obesity diabetes','lose eyesight','insulin resistance','adult diabetes','bone health','diabetic retinopathy',
                       ]].sum(axis=1))
    
        matrix_of_toptwitters_topics['Diabetes-Miscellaneous'] = (summarisedFrame[['roche','phoenix','novo nordisk','alzheimers','cancer',
                       'chemo','glooko','investor', 'investor profit']].sum(axis=1))
    
        matrix_of_toptwitters_topics['Diabetes_Community'] = (summarisedFrame[['life diabetes','diabetes africa','diabetes breakthrough','diabetes community',
                       'diabetes hero','diabetes uk','great news','happy','proud','amazing']].sum(axis=1))
        
        
        matrix_of_toptwitters_topics.to_csv('diabetes\\matrix_of_top_twitters_topics.csv')
            
        my_plot = matrix_of_toptwitters_topics.plot(kind='bar',stacked=True)
        my_plot.set_xlabel("Top twitters")
        my_plot.set_ylabel("Tweet occurrences")
        plt.legend(loc='upper left')
        plt.title('Popular Tweeters and their key themes')
        plt.gca().invert_xaxis()
        plt.show()
    
    except Exception as e:
        print(str(e))
    
#creating a matrix of top terms and the top users returns it as a dictionary with terms as keys and values as dictioneries of users and the number of mentions of the key term
def top_users_and_terms(keyterms, corpus):
    user_dict = {}
    unwanted_ctrs = re.compile("[',]")
    
    '''checks a tweet for a key term, if key term found in tweet, that user is added to a list.
     then creates a dictionary of all key terms and lists of their respective tweeters. {keyterm: [list of keyterm tweeters]'''
    for key_term in keyterms:
        for tweet in corpus: 
            text = tweet[2].strip('[]')
            text = unwanted_ctrs.sub('', text)
            text = re.sub(r'(\\\\\w*)', '', text)
            key_term = key_term.strip("''").lower()
            if key_term in text.lower():
                user_dict.setdefault(key_term , []).append(tweet[0])
    print (len(user_dict))
    
    #creating a dictionary of key terms containing values which are dictionaries of the twitters and the number of times they tweet the key term
    x = dict()  
    top_ten_common_terms = dict() 
    for i in user_dict.keys():
        x.clear()
        for j in user_dict[i]:
            if j in x:
                x[j] += 1
            else:
                x[j] = 1
        top_ten_common_terms[i] = dict(sorted(x.items(), key=itemgetter(1), reverse=True)[:10]) 
    
    return top_ten_common_terms
    
#identifying similar items in the key term list using levenshtein distance and then returning a list of the terms (which are considered to be duplicate)
def match_key_terms(key_term_list):
    similar_items_list = []
    for m,n in itertools.combinations(key_term_list, 2):
        sim1 = jf.levenshtein_distance(m.strip("''"),n.strip("''"))
        if (sim1 <= 1):
            print ('%s, %s : %d' %(m,n,sim1))
            similar_items_list.append(m)  
    return similar_items_list 

#function returning a data frame which is a matrix of all the key terms and the top ten twitters for each key term, as well as the number of tweets 
def matrix_users_topic(dict_of_terms_users):
    
    s = []
    for i in dict_of_terms_users:
        d = dict()
        d[i] = dict_of_terms_users[i]
        dict_frame = pd.DataFrame.from_dict(d)
        dict_frame = dict_frame.sort_values([i], ascending=False)
        s.append(dict_frame)
   
    dict_of_terms_users_frame = pd.concat(s, axis=1)
    dict_of_terms_users_frame .index.name = 'Username'
    return dict_of_terms_users_frame 
    
match_users_to_themes()
