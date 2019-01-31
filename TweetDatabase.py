import os
import json


class TweetDatabase:
    def __init__(self, db_path, max_count):
        print('Initializaing database...')
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + '/' + db_path) as f:
            data = json.load(f)
        self.tweets = []
        counter = 0
        for tweet in data:
            self.tweets.append(tweet['text'])
            if counter > max_count:
                break
            counter += 1
        print('Database initialized with ' + str(len(self.tweets)) + ' tweets.')


    # returns total number of words in db
    def get_num_words(self):
        word_count = 0
        for text in self.tweets:
            word_count += len(text)
        return word_count

    # returns tweets
    def get_tweets(self):
        return self.tweets

    # returns specified tweet string
    def get_tweet_by_index(self, index):
        return self.tweets[index]

    # returns unprocessed list of words in db
    def get_words(self):
        words = []
        for tweet in self.tweets:
            words_in_tweet = tweet.split()
            words.extend(words_in_tweet)
        return words
