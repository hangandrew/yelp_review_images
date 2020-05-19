#!/usr/bin/env python
# coding: utf-8


# COMMENTED OUT (Used jupyter notebook to set environment variable to where my API KEY was located)
# get_ipython().magic(u'set_env GOOGLE_APPLICATION_CREDENTIALS GOOGLE_API_KEY.json')

# FILEPATH to where the review image labels and data are locatied
FILEPATH = "FILELOCATION.csv"
# starting idx for which uri to begin with
idx = 0

# My computer set limits on how many files I needed to open, a hacky way to get around this to not allow so
import resource
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))


# Copied from GOOGLE VISION quick starts
def get_picture_labels_uri(content_uri):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = content_uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    labels_list = []

    for label in labels:
        labels_list.append(label.description.encode('utf-8'))

	# Set the function to print out errors that were not a large problem (MOST ERRORS are ERROR 3 unable to reach)
    if response.error.message:
        print("ERROR CODE", response.error.code)
        if response.error.code == 3 or response.error.code == 4:
            return None
        elif response.error.code == 503:
            return "ERROR"
        else:
            raise Exception('{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(response.error.message))
    return labels_list


# function to save current images and labels to CSV FILE (used incrementally incase of crashes)
def save_reviews(version):
    filename = "review_labels_idx"+ str(version) +".csv"
    print("Saving in", filename)
    with open(filename , "wb") as f:
        writer = csv.writer(f)
        writer.writerows(images)


with open(FILEPATH, "r") as f:
    import csv
    reader = csv.reader(f)
    images = list(reader)
images


import time
n = len(images)


last_save = 0
while idx != n:
    try:
        labels = get_picture_labels_uri(images[idx][1])
        images[idx].append(labels)
        idx += 1
        if idx % 1000 == 0:
            print("idx:", idx)
        if idx % 10000 == 0:
            save_reviews(idx)
    except:
        save_reviews(idx)
        # Created this since my computer overheats by this point and stops the program
        if idx - last_save < 10:
            break
        last_save = idx
        time.sleep(90)
