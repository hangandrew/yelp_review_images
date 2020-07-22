#!/usr/bin/env python3

import pandas as pd
import os
from multiprocessing import Pool
import itertools
from gensim.models.doc2vec import Doc2Vec


class generate_vect:

  def __init__(self):
    
    self.count = 0
    # load data
    df = pd.read_csv('finald2v.csv')
    chunks = [df[0:20000],df[20000:40000],df[40000:60000],df[60000:80000],df[80000:100000],
            df[100000:120000],df[120000:140000],df[140000:160000],df[160000:180000],df[180000:200000],
            df[200000:220000],df[220000:240000],df[240000:260000],df[260000:280000],df[280000:300000],
            df[300000:320000],df[320000:340000],df[340000:360000],df[360000:380000],df[380000:400000],
            df[400000:420000],df[420000:440000],df[440000:460000],df[460000:480000],df[480000:500000],
            df[500000:520000],df[520000:540000],df[540000:560000],df[560000:580000],df[580000:600000],
            df[600000:640000],df[640000:681526]]

    # load model
    self.model= Doc2Vec.load("d2v.model")
    print('Model loaded')
    self.model.random.seed(0)

    # number of reviews = 681526
    # call the test_funct() using multiprocessor module
    pool = Pool(processes = 32) # number of processes = 5, since there are 5 chunks
    self.result1 = pool.map(self.parse_reviews, chunks) # pass these 5 chunks to run_create to parallelly process the chunks
    self.result_flat = list(itertools.chain(*self.result1))
    
    
  def print_vect(self):
    df = pd.DataFrame(self.result_flat, columns=('review_id', 'review_text', 'vectors'))
    df.to_pickle('final_vect.pkl')
    df.to_csv('final_vect.csv')
   
  def parse_reviews(self, reviews):
    result = []
    for id_, review in zip(reviews.review_id, reviews.review_text):
      print(self.count,id_, review)
      self.count = self.count + 1
      result.append([id_, review, self.model.infer_vector(review)])
    
    return result
    
  
if __name__ == '__main__':
  obj = generate_vect()
  obj.print_vect()
  print('Done')
  
  


