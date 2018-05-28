# -*- coding:utf-8

from requests_oauthlib import OAuth1Session
import re
import json
import csv
import sys

sys.path.append("../")

import dataprocesser.accounts
import dataprocesser.keys

class TweetData(object):

    # Constructor
    def __init__(self):
        key = dataprocesser.keys.KEY
        self.twitter = OAuth1Session(key.CK, key.CS, key.AT, key.AS)

    # Request
    def __get_request(self, url, params=[]):
        req = self.twitter.get(url, params=params)
        if req.status_code == 200:
            # JSON parse
            info = json.loads(req.text)
            return info
        else:
            return []

    # api statuses/user_timeline
    def get_user_timeline(self, screenName, count=200):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        param = {"screen_name": screenName, "count": count}
        return self.__get_request(url, param)

    # Remove tab, newline, url, mention
    def format_text(self, text):
        lst = ['\t', '\n', '\r', ' ', '　' ]
        delete4str = str.maketrans(dict.fromkeys(lst, " "))
        re_text = text.translate(delete4str)
        re_text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', " ", re_text)
        return re.sub(r'@[0-9a-zA-Z_]{1,15}', "", re_text)

    #
    def get_tweets(self, screenName, count=200):
        tweets = []
        info = self.get_user_timeline(screenName, count)
        i = 0
        count = 0
        for tweet in info:
            #  and tweet["in_reply_to_screen_name"] is None
            if "retweeted_status" not in tweet and "quoted_status" not in tweet:
                text = tweet["text"]
                text = self.format_text(text)
                if len(text) >= 7:
                    tweets.append([screenName, text])
                    count += 1
            i += 1
            sys.stdout.write('\r>> (@%s) tweets %d / %d' % (screenName, i, len(info)))
            sys.stdout.flush()
        sys.stdout.write('\r>> (@%s) tweets %d / %d (total %d)\n' % (screenName, i, len(info), count))
        sys.stdout.flush()
        return tweets

    # write tsv
    def write(self, filename, data):
        with open(filename, "a", newline="")as f:
            writer = csv.writer(f, delimiter="\t", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for screenName, text in data:
                writer.writerow([screenName, text])
            print("output to %s , all %d records." % (filename, len(data)) )

    # trans_unicode code
    def trans_unicode(self, comments, max_length=100, min_length=7):
        unicode_comments = []
        for comment in comments:
            comment = [ord(x) for x in comment.strip() if ord(x) <= 0xffff]
            comment = comment[:max_length]
            comment_len = len(comment)
            if comment_len < min_length:
            # 短すぎるのは除外
                continue
            if comment_len < max_length:
            # 足りない部分を0パディング
                comment += ([0] * (max_length - comment_len))
            unicode_comments.append(comment)
        return unicode_comments

if __name__ == '__main__':
    # write Data
    object = TweetData()
    list = dataprocesser.accounts.targets + dataprocesser.accounts.no_targets
    tweets = []
    for screenName in list:
        tweets.extend(object.get_tweets(screenName))
    object.write("sample.tsb", tweets)
