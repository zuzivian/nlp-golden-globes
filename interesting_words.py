from helpers import *
from TweetDatabase import TweetDatabase


'''
A simple interesting word extracting script (no n-grams)
'''
# nltk.download('stopwords')
db = TweetDatabase('./data/gg2013.json', 1000)
print("Extracting tweets...")
tweets = db.get_tweets()
print("Tokenizing...")
tokens = tokenize_multiple_texts(tweets)
print("Removing punctuation...")
alpha_tokens = strip_punctuation(tokens)
print("Removing stopwords...")
useful_tokens = remove_stopwords(alpha_tokens)
print("Counting word frequency of " + str(len(useful_tokens)) + " words ...")
freq_dict = get_word_freq_dict(useful_tokens)
print("Processing Complete.")
print("Total number of words: " + str(db.get_num_words()))
print("Content fraction: " + str(float(len(useful_tokens)) / db.get_num_words()))
print_dict(freq_dict)
