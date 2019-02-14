from nltk import tokenize
import nltk
from nltk.tokenize import TweetTokenizer, RegexpTokenizer
import datetime
import string
import os

# define globals
dir_path = os.path.dirname(os.path.realpath(__file__))

# stop words
def get_stopwords():
    stop_words = nltk.corpus.stopwords.words('english')
    twitter_words = ["http", "rt"]
    return stop_words + twitter_words

def get_replacewords():
    return {
        u'television': u'tv',
        u'picture': u'movie',
        'miniseries': 'limited',
    }

def remove_stopwords(words, stop_words, replace_words=[]):
    processed_list = []
    for w in words:
        if w not in stop_words and w not in processed_list:
            if w in replace_words.keys():
                processed_list.append(replace_words[w])
            processed_list.append(w)
    return processed_list


def content_fraction(words):
    stop_words = get_stopwords()
    content = [w for w in words if w.lower() not in stop_words]
    return len(content) / len(words)


# tokenize
def twitter_tokenize(text, preserve_case=False):
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=preserve_case)
    return tknzr.tokenize(text)

def tokenize_multiple_texts(listof_texts):
    tokenized_words = []
    for text in listof_texts:
        tokenized_words.extend(twitter_tokenize(text))
    return tokenized_words

def strip_punctuation(words):
    translate_table = dict((ord(char), None) for char in string.punctuation)
    new_words = []
    for w in words:
        new_word = w.translate(translate_table)
        if new_word:
            new_words.append(new_word)
    return new_words


# returns a dict containing frequency of words in list
def get_word_freq_dict(words):
    words_sorted_by_freq = {}
    for word in words:
        if word in words_sorted_by_freq.keys():
            words_sorted_by_freq[word] += 1
        else:
            words_sorted_by_freq[word] = 1
    return words_sorted_by_freq

# printing
def print_dict(dict):
    date = datetime.datetime.now()
    file = open(dir_path + '/output/' + str(date) + ".txt", "w")

    d_view = [ (v,k) for k,v in dict.iteritems() ]
    d_view.sort(reverse=True) # natively sort tuples by first element
    for v,k in d_view:
        file.write("%s: %s\n" % (k.encode('ascii', 'ignore'),str(v)))

    file.close()
