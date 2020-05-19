#!/usr/bin/env python
# coding: utf-8

# In[ ]:
FILEPATH = ""

# OPEN FILE
with open(FILEPATH, "r") as f:
    import csv
    reader = csv.reader(f)
    images = list(reader)
images


########################### REFORTMATTING DATA ###########################
n = len(images)
removed_errors = []

for i in range(n):
    i_id, _, labels = images[i]
    if labels != "" and labels != "[]":
        removed_errors.append([i_id[2:], [label.strip() for label in labels[1:-1].split(",")]])

removed_errors



formatted_images = []
n = len(removed_errors)
for i in range(n):
    clean_labels = []
    for label in removed_errors[i][1]:
        if label[:2] == "u'":
            clean_labels.append(label[2:-1])
        else:
            clean_labels.append(label[1:-1])
    formatted_images.append((removed_errors[i][0], ";".join(clean_labels)))

formatted_images

########################### REFORTMATTING DATA ###########################


############################# UPLOADING DATA #############################

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



stmt = "INSERT INTO review_images_labels (image_id, labels) VALUES " + ",".join("(%s, %s)" for _ in formatted_images)
flattened_images = [item for image in formatted_images for item in image]



cursor.execute(stmt, flattened_images)



conn.commit()

############################# UPLOADING DATA #############################