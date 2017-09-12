# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:17:13 2017

@author: Mike
"""
from tweet_processing import working_directory
from nltk.tokenize import PunktSentenceTokenizer
from textblob import TextBlob
import pandas as pd
import numpy as np
import nltk
import re
import io
import os
import rake   

class theme_extraction:
    
    def __init__(self, file, advise_file, non_advise_file, corpus):
        self.file = file
        self.advise_file = advise_file
        self.corpus = corpus
        self.none_advise_file = non_advise_file
    '''Combining all the tweets in their different clusters, advise and non-advise tweets'''
    def combine_tweets(self):
        
        fileConverted = np.array(self.file)
        fileConverted = fileConverted.tolist()
        try:
            for item in fileConverted:
                unwanted_ctrs = re.compile("[',]")
                text = item[2].strip('[]')
                text = unwanted_ctrs.sub('', text)
                text = re.sub(r'(\\\\\w*)','', text)
                self.corpus.write(text)
                self.corpus.write('.')
                self.corpus.write(' ')
                if((item[3] == 'purely_advise') or (item[3] == 'mostly_advise') or (item[3] == 'moderately_advise')):
                    self.advise_file.write(text) 
                    self.advise_file.write('.')
                    self.advise_file.write(' ')
                   
                else:
                    self.none_advise_file.write(text)
                    self.none_advise_file.write('.')
                    self.none_advise_file.write(' ')
        except Exception as e:
            print (str(e))
            
        self.corpus.close()
        self.advise_file.close()
        self.none_advise_file.close()
    
def themes(): 
    
    #using the Rake module to extract key themes     
    stoppath = "SmartStoplist.txt"
    
    keythemes_file = open('diabetes\\diabetes_key_themes.txt', 'a+')
    rake_object = rake.Rake(stoppath, 4,4,4)    # A key theme has to have a minimum of 4 characters, It can be 4 separate phrases, and it has to appear atleast 4 times in the entire corpus
    advise_file = io.open('diabetes\\advise.txt', 'r', encoding='iso-8859-1')
    none_advise_file = io.open('diabetes\\none_advise.txt', 'r', encoding='iso-8859-1')
    kph = io.open('diabetes\\key-rheumatoid-noun-phrases.txt', 'r', encoding='iso-8859-1')
    
    advise_text = advise_file.read()
    none_advise_text = none_advise_file.read()
    kph_text = kph.read()
    
    keywords1 = rake_object.run(advise_text)
    keywords2 = rake_object.run(none_advise_text)
    kph_keywords = rake_object.run(kph_text)
    
    keythemes_file.write('Advise-key-words')
    keythemes_file.write('\n')
    keythemes_file.write(str(keywords1))
    keythemes_file.write('\n\n')
    keythemes_file.write('None-Advise-key-words')
    keythemes_file.write('\n')
    keythemes_file.write(str(keywords2))
    keythemes_file.write('\n\n')
    keythemes_file.write('key-phrases from noun phrases')
    keythemes_file.write('\n')
    keythemes_file.write(str(kph_keywords))
    
    keythemes_file.close()

def entities():
    train_text = open('none_advise.txt', 'r').read()
    diabetes_text = open('advise.txt', 'r').read()
    custom_tokenizer = PunktSentenceTokenizer(train_text)
    diabeste_tokens = custom_tokenizer.tokenize(diabetes_text)
    try:
        for i in diabeste_tokens:
           word = nltk.word_tokenize(i)
           tagged = nltk.pos_tag(word)
           chunkGram = r"""Chunk: {<RB.?>*<NNP>+<NN>?}"""
           chunkParser = nltk.ne_chunk(chunkGram)
           chunked = chunkParser.parse(tagged)
           chunked.draw()
           
           print (tagged)       
    except Exception as e:
        print (str(e))

#Using Textblob to extract noun phrases from the carge corpus containing tweets
def extract_noun_phrases():
    working_directory()
    diabetes_text = open('diabetes\\diabetes-corpus.txt', 'r').read()
    blob = TextBlob(diabetes_text)
    
    key_phrases = open('diabetes\\key-diabetes-noun-phrases.txt', 'a+')
    for phrase in blob.noun_phrases:
        print (phrase)
        break
        key_phrases.write(phrase)
        key_phrases.write(',') 
        key_phrases.write(' ')
    key_phrases.close()
        

               
tdf = pd.read_csv('diabetes\\diabetes-training-set-text.csv')
diabetes_corpus = open('diabetes\\diabetes-corpus.txt', 'w+')
advise_text = open('diabetes\\diabetes_advise.txt', 'w+')
none_advise_text = open('diabetes\\diabetes_none_advise.txt', 'w+')
th = theme_extraction(tdf, advise_text, none_advise_text, diabetes_corpus)
th.combine_tweets()
#themes()
#entities()
#extract_noun_phrases()
