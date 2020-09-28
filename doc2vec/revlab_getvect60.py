#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import pandas as pd
import numpy
import logging
import gensim
import random
import sklearn
import collections
import os
from multiprocessing import Pool
import itertools
from gensim.models.doc2vec import Doc2Vec
import random

class generate_vect:

  def __init__(self):
    
    self.count = 0
    self.model60= Doc2Vec.load("d2v60/d2v60.model")
    print('Model with Vector size 60 loaded')
    self.model60.random.seed(0)


    result1 = pd.read_pickle('results1.pkl') 
    chunks = [result1[0:20000],result1[20000:40000],result1[40000:60000],result1[60000:80000],result1[80000:100000],
            result1[100000:120000],result1[120000:140000],result1[140000:160000],result1[160000:180000],result1[180000:200000],
            result1[200000:220000],result1[220000:240000],result1[240000:260000],result1[260000:280000],result1[280000:300000],
            result1[300000:320000],result1[320000:340000],result1[340000:360000],result1[360000:380000],result1[380000:400000],
            result1[400000:420000],result1[420000:440000],result1[440000:460000],result1[460000:480000],result1[480000:500000],
            result1[500000:520000],result1[520000:540000],result1[540000:560000],result1[560000:580000],result1[580000:600000],
            result1[600000:640000],result1[640000:681526]]

    # number of reviews = 681526
    pool = Pool(processes = 32) # number of processes = 32, since there are 32 chunks
    self.results = pool.map(self.parse_reviews, chunks) # pass these 32 chunks to parse_reviews to parallelly process the chunks
    self.result_flat = list(itertools.chain(*self.results))
  
  def parse_reviews(self, test_subjects):
    result = []
    for id_, review in zip(test_subjects.rid, test_subjects.text):
      print(self.count,id_)
      self.count = self.count + 1
      result.append([id_, self.model60.infer_vector(review)])
    
    return result
    
    
  def print_vect(self):
    df = pd.DataFrame(self.result_flat, columns=('review_id','vectors'))
    df.to_pickle('revlab_vect_reviews.pkl')
    df.to_csv('revlab_vect_reviews.csv')
   

if __name__ == "__main__":
  obj = generate_vect()
  obj.print_vect()
  print('Done')
    

