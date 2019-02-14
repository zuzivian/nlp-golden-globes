from helpers import *
from SolvingHost import *

from TweetDatabase import TweetDatabase
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment_of_tweets(tweet_list):
    sid = SentimentIntensityAnalyzer()
    sentiments = {}
    for tweet in tweet_list:
        ss = sid.polarity_scores(tweet)
        names = extract_names(tweet)
        for name in names:
            if name not in sentiments.keys():
                sentiments[name] = 0
            sentiments[name] += ss['compound']
    return sentiments
