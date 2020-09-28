#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import pandas as pd
import numpy
import logging
import gensim
import random
import sklearn
import collections
from nltk.tokenize import word_tokenize, stopwords


def get_vect60():
  dfr = pd.read_csv('drive/My Drive/mshr/all_reviews.csv')
  print(dfr.head())




if __name__ == '__main__':
  get_vect60()


