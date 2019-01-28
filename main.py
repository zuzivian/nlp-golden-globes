import nltk
import json
from pprint import pprint
import os

# load json data
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + '/data/gg2013.json') as f:
    data = json.load(f)

counter = 0
common_words = {}


# common words
for tweet in data:
    pprint(tweet['text'])
    counter+=1
    words_in_tweet = tweet['text'].split()
    for word in words_in_tweet:
        if word in common_words.keys():
            common_words[word] += 1
        else:
            common_words[word] = 1
    if counter > 100:
        break


# Ideas to work on, feel free to choose one and explore nltk

# tokenize

# group similar words? ie spelling errors, slang

# noise reduction

# stop lists

# punctuation

# n-grams

# tags?

# check capitalization

# tfidf


d_view = [ (v,k) for k,v in common_words.iteritems() ]
d_view.sort(reverse=True) # natively sort tuples by first element
for v,k in d_view:
    pprint("%s: %d" % (k,v))
