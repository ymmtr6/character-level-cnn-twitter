# -*- coding:utf-8 -*-

import numpy as np
import sys

from tensorflow.python.keras.models import *
from dataprocesser.clcnn_data import TweetData

args = sys.argv
model = load_model("model.h5")

def predict(comments, model_filepath="model.h5"):
    ret = model.predict(comments)
    return ret

if __name__ == "__main__":
    if(len(args) != 2):
        print("USAGE:python clcnn_api.py [screenName]")
    screenName = args[1]
    tweetData = TweetData()

    raw_comments = tweetData.get_tweets(screenName, 20)
    raw_comments = [text for ( id, text ) in raw_comments]

    if len(raw_comments) == 0:
        exit("no tweet")

    comments = tweetData.trans_unicode(raw_comments)
    vector = np.array(comments)

    print("predict start")
    ret = predict(vector)

    for comment, r in zip(raw_comments, ret):
        print("[{0:.2f}]{1}".format(r[0], comment))
    print("Average Score: {0:.2f}".format(np.mean(ret)))
