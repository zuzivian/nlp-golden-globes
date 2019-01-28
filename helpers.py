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
    twitterwords = ["http", "rt", "golden", "goldenglobes", "globes"]
    return stop_words + twitterwords

def remove_stopwords(words):
    processed_list = []
    stop_words = get_stopwords()
    for w in words:
        if w not in stop_words:
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
    for w in words:
        w.translate(translate_table)
    return words


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
def print_dict_of_word_frequencies(dict):
    date = datetime.datetime.now()
    file = open(dir_path + '/output/' + str(date) + ".txt", "w")

    file.write("--------------\n")
    file.write("Word Frequency\n")
    file.write("--------------\n")
    d_view = [ (v,k) for k,v in dict.iteritems() ]
    d_view.sort(reverse=True) # natively sort tuples by first element
    for v,k in d_view:
        file.write("%s: %d\n" % (k.encode('ascii', 'ignore'),v))

    file.close()
