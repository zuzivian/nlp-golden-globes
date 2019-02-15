from helpers import *
from dressed import *
from TweetDatabase import TweetDatabase

def award_classifier(tweet_tokens, award_categories, token_dict):
    best_score = 0
    best_category = ""
    for award in award_categories:
        score = num_matches(token_dict[award], tweet_tokens)
        if score > best_score and score > 1:
            best_score = score
            best_category = award
    return best_category

def num_matches(list1, list2):
    matches = 0
    for item in list1:
        matches += list2.count(item)
    return matches

# file_path: path to json database
# max_tweets: maximum number of tweets to process
# award_list: list of string containing award name
def get_and_classify_tweets(file_path, max_tweets, award_list, other_categories=[]):
    db = TweetDatabase(file_path, max_tweets)
    tweets = db.get_tweets()
    stop_words = get_stopwords()
    replace_words = get_replacewords()

    print("Parsing awards...")
    tweet_dict_by_award = {}
    award_token_dict = {}
    award_list.extend(other_categories)
    for award in award_list:
        tweet_dict_by_award[award] = []
        award_token = award.lower().split()
        award_token = strip_punctuation(award_token)
        award_token = remove_stopwords(award_token, stop_words, replace_words)
        award_token_dict[award] = award_token
    print("Classifying tweets...")
    counter = 0
    for tweet in tweets:
        tokens = twitter_tokenize(tweet)
        tokens = strip_punctuation(tokens)
        tokens = remove_stopwords(tokens, stop_words, replace_words)
        category = award_classifier(tokens, award_list, award_token_dict)
        counter += 1
        if (counter % 10000 is 0):
            print(str(counter) + " tweets classified...")
        if category:
            tweet_dict_by_award[category].append(tweet)
    return tweet_dict_by_award
