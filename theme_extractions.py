# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 11:17:13 2017

@author: Mike
"""
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import state_union
from textblob import TextBlob
import pandas as pd
import numpy as np
import nltk
import re
import io
import rake   

class theme_extraction:
    
    def __init__(self, file, advise_file, non_advise_file, rhemu_corpus):
        self.file = file
        self.advise_file = advise_file
        self.rhemu_corpus = rhemu_corpus
        self.non_advise_file = non_advise_file
    '''Combining all the tweets in their different clusters, advise and non-advise tweets'''
    def combine_tweets(self):
        
        fileConverted = np.array(self.file)
        fileConverted = fileConverted.tolist()
   
        for item in fileConverted:
            unwanted_ctrs = re.compile("[',]")
            text = item[2].strip('[]')
            text = unwanted_ctrs.sub('', text)
            text = text.replace('\\\\', '')
            self.rhemu_corpus.write(text)
            self.rhemu_corpus.write('.')
            self.rhemu_corpus.write(' ')
            if((item[1] == 'purely_advise') or (item[1] == 'mostly_advise') or (item[1] == 'moderately_advise')):
                self.advise_file.write(text) 
                self.advise_file.write('.')
                self.advise_file.write(' ')
               
            else:
                self.non_advise_file.write(text)
                self.non_advise_file.write('.')
                self.non_advise_file.write(' ')
                
        self.rhemu_corpus.close()
        self.advise_file.close()
        self.non_advise_file.close()
    
def themes(): 
    #using the Rake module to extract key themes     
    stoppath = "SmartStoplist.txt"
    
    keythemes_file = open('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\key_themes.txt', 'a+')
    rake_object = rake.Rake(stoppath, 4,4,4)    # A key theme has to have a minimum of 4 characters, It can be 4 separate phrases, and it has to appear atleast 4 times in the entire corpus
    advise_file = io.open('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\advise.txt', 'r', encoding='iso-8859-1')
    none_advise_file = io.open('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\none_advise.txt', 'r', encoding='iso-8859-1')
    kph = io.open('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\key-rheumatoid-noun-phrases.txt', 'r', encoding='iso-8859-1')
    
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
           chunkParser = nltk.ne_chunk(tagged)
           chunked = chunkParser.parse(tagged)
           chunkParser.draw()
           
           print (tagged)
           
    except Exception as e:
        print (str(e))

#Using Textblob to extract noun phrases from the carge corpus containing tweets
def extract_noun_phrases():
    diabetes_text = open('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\rheumatoid-corpus.txt', 'r').read()
    blob = TextBlob(diabetes_text)
    
    key_phrases = open('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\key-rheumatoid-noun-phrases.txt', 'a+')
    for phrase in blob.noun_phrases:
        key_phrases.write(phrase)
        key_phrases.write(',') 
        key_phrases.write(' ')
    key_phrases.close()
        

               
#==============================================================================
# tdf = pd.read_csv('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\rheumatoid-training-set.csv')
# rheum_corpus = open('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\rheumatoid-corpus.txt', 'w+')
# advise_text = open('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\advise.txt', 'w+')
# none_advise_text = open('C:\\Users\\Mike\\Documents\\Github\\ABCi_Twitter_Analysis\\rheum\\new_set\\none_advise.txt', 'w+')
# th = theme_extraction(tdf, advise_text, none_advise_text, rheum_corpus)
# th.combine_tweets()
#==============================================================================
themes()
#entities()
#extract_noun_phrases()
