#!/usr/bin/env python
# coding: utf-8

# In[20]:


import gensim.models as g
import logging
from scipy import spatial


# In[8]:


#enable logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


#train doc2vec model
model = g.doc2vec.Doc2Vec.load("enwiki_dbow/doc2vec.bin")




def get_picture_labels_uri(content_uri):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = content_uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    labels_list = []

    for label in labels:
        labels_list.append(label.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return labels_list


def get_sql_review_imgs(start, n_rows):
    import mysql.connector
    server = 'mshresearch.marshall.usc.edu'
    server_ip = '10.103.7.66'
    db = 'yelp_michael_2'
    user = 'USERNAME'
    password = 'PASSWORD'

    conn = mysql.connector.connect(user=user, password=password,
                                   host=server_ip,
                                   database=db)
    cursor = conn.cursor()
    cursor.execute('USE yelp_michael_2')
    cursor.execute('''
        SELECT *
        FROM reviews 
            LEFT JOIN review_images
                ON reviews.review_id = review_images.review_id
        LIMIT {start}, {n_rows}
    '''.format(start=start, n_rows=n_rows))

    data = []
    current_review = {"r_id": None}
    for row in cursor:
        if current_review["r_id"] != row[0]:
            data.append(current_review)
            current_review = {"r_id": row[0],
                             "r_text": row[4],
                             "r_rating": int(row[5]),
                             "imgs": [row[13]]
                            }
        else:
            current_review["imgs"].append(row[13])
    
    if current_review["r_id"] != data[-1]["r_id"]:
        data.append(current_review)
    
    return data[1:]



def get_similarity(vec1, vec2):
    return spatial.distance.cosine(vec1, vec2)





def get_img_vec(imgs):
    all_labels = []
    for img in imgs:
        all_labels = all_labels + get_picture_labels_uri((img))
    return model.infer_vector(all_labels)




db_data = get_sql_review_imgs(0, 50)


similarities = []
for data in db_data:
    img_vec = get_img_vec(data['imgs'])
    text_vec = model.infer_vector(data['r_text'].split())
    similarities.append((data['r_id'], data['r_rating'], get_similarity(img_vec, text_vec)))
similarities





