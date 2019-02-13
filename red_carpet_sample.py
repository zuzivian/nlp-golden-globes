from classifier import *

'''
A sample script that  analyzes red carpet tweets
'''

# returns a dictionary containing tweets classified by award categories
other_categories = [u"red carpet"]
tweet_dict_by_award = get_and_classify_tweets('./data/gg2013.json', 10000, gg2013_categories, other_categories)


red_carpet_tweets = tweet_dict_by_award[other_categories[0]]
d = analyze_sentiment_of_tweets(red_carpet_tweets)

print("Printing results to file...")
date = datetime.datetime.now()
file = open(dir_path + '/output/' + str(date) + ".txt", "w")
sorted = [(k, d[k]) for k in sorted(d, key=d.get, reverse=True)]
for p,s in sorted:
        file.write("%s: %f\n" % (p.encode('ascii', 'ignore'), s))
file.close()
