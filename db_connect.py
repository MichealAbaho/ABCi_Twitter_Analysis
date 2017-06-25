# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 18:37:30 2017

@author: Mike
"""

from pymongo import MongoClient
import pymongo

class dbConnection:
    
    def connecting(self):
        clientConnect = MongoClient()
        db = clientConnect.ABCi_twitter_analysis_DB
        return db


