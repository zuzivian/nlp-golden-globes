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
tokenized_words = tokenize_multiple_texts(tweets)
print("Removing Punctuation...")
alphanumeric_words = strip_punctuation(tokenized_words)
print("Removing stopwords...")
stripped_words = remove_stopwords(alphanumeric_words)
print("Counting word frequency of " + str(len(stripped_words)) + " words ...")
freq_dict = get_word_freq_dict(stripped_words)
print("Processing Complete.")
print("Total number of words: " + str(db.get_num_words()))
#print("Content fraction: " + str(content_fraction(alphanumeric_words)))
print_dict_of_word_frequencies(freq_dict)
