#!/usr/bin/env python3.7

import pandas as pd
import logging
import gensim
import random

def read_data(data, tokens_only = False):
  for i, review in enumerate(data):
        tokens = gensim.utils.simple_preprocess(review)
        if tokens_only:
            yield tokens
        else:
            # print(gensim.models.doc2vec.TaggedDocument(tokens, [i])) TaggedDocument([list of words],[document_td/tag])
            yield gensim.models.doc2vec.TaggedDocument(tokens, [i])

def run_doc2vec():
  df = pd.read_csv('finald2v.csv')
  print(df.head())
  print('Number of reviews:',len(df))

  train = df.review_text[0:550000]
  train = [str(review) for review in train]
  test = df.review_text[550000:681526]
  test = [str(review) for review in test]

  logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)

  traind = list(read_data(train))
  testd = list(read_data(test))

  # train model

  model = gensim.models.doc2vec.Doc2Vec(vector_size = 16, min_count = 1, window = 10, epochs = 100, workers = 32)
  model.build_vocab(traind)
  print('----------------------Built Vocabulary-----------------------------')
  model.train(traind, total_examples=model.corpus_count, epochs= model.epochs)
  print('----------------------Model Trained--------------------------------')
  model.save('d2v.model')
  print('----------------------Model Saved----------------------------------')

  # test model
  doc_id = random.randint(0, len(testd) - 1)
  inferred_vector = model.infer_vector(testd[doc_id].words)
  sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))

  # Compare and print the most/median/least similar documents from the train corpus
  print('Test Document ({}): «{}»\n'.format(doc_id, ' '.join(testd[doc_id].words)))
  print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
  for label, index in [('MOST', 0), ('MEDIAN', len(sims)//2), ('LEAST', len(sims) - 1)]:
    print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(traind[sims[index][0]].words)))
  

if __name__ == '__main__':
  run_doc2vec()