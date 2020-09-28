#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import pandas as pd
import numpy
import logging
import gensim
import random
import sklearn
import collections
from gensim.models.doc2vec import Doc2Vec
from multiprocessing import Pool
import itertools


class Test:
    def __init__(self):
        
        self.model60= Doc2Vec.load("d2v60/d2v60.model")
        print('Model with Vector size 60 loaded')
        self.model60.random.seed(0)

        df = pd.read_csv('train_data.csv')
        print(df.head())
        print('Number of reviews:',len(df))
    
        test = df.review_text[0:50000]
        test = [str(review) for review in test]
        
        self.testd = list(self.read_data(test))
        self.run_test()
    
    def read_data(self, data, tokens_only = False):
        for i, review in enumerate(data):
              tokens = gensim.utils.simple_preprocess(review)
              if tokens_only:
                  yield tokens
              else:
                  # print(gensim.models.doc2vec.TaggedDocument(tokens, [i])) TaggedDocument([list of words],[document_td/tag])
                  yield gensim.models.doc2vec.TaggedDocument(tokens, [i])
                  
    def run_test(self):
      
      correct = 0
      for doc in self.testd:
        print('Testing Document:', doc.tags[0])
        inferred_vector = self.model60.infer_vector(doc.words)
        sims = self.model60.docvecs.most_similar([inferred_vector], topn = 1)
        if sims[0][0] == doc.tags[0]:
            correct += 1
      print('Correct:', correct)
      print('Accuracy:',correct/len(self.testd))
      

if __init__ == '__main__':
    obj = Test()
    