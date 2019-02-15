# -*- coding: utf-8 -*-
import json
import re

from helpers import *


def extract_award_names(result, tweet, startlist, endlist):

	tweet_words = tweet.lower().split()

	for i in startlist:
		for j in endlist:
			if i not in tweet_words or j not in tweet_words:
				continue
			index_i = tweet_words.index(i)
			index_j = tweet_words.index(j)
			if index_i > index_j:
				continue
			award_tokens = tweet_words[index_i:index_j+1]
			if len(award_tokens) >= 3 and len(award_tokens) < 15:
				award = " ".join(award_tokens)
				if award not in result:
					result[award] = 1
				else:
					result[award] += 1
	return result


def generate_awards(year):
	result = {}
	start_words = ['best']
	end_words = ['picture', 'film', 'drama', 'comedy', 'musical', 'animated', 'miniseries', 'mini-series', 'score', 'song']
	stop_words = get_stopwords()
	replace_words = get_replacewords()

	j_file = open('gg%s.json' % year)
	j_str = j_file.read()
	j_data = json.loads(j_str)

	for i in j_data:
		result = extract_award_names(result, i['text'], start_words, end_words)

	temp = sorted(result.items(), key=lambda x: len(x[0]), reverse=True)

	award_tuples = []

	for item in temp:
		if item[1] < 50:
			continue
		award_tuples.append(item)

	awards = []
	for i in award_tuples:
		contained = False
		tokens_i = twitter_tokenize(i[0])
		tokens_i = remove_stopwords(tokens_i, stop_words, replace_words)
		tokens_i = strip_punctuation(tokens_i)
		for j in awards:
			tokens_j = twitter_tokenize(j)
			tokens_j = remove_stopwords(tokens_j, stop_words, replace_words)
			tokens_j = strip_punctuation(tokens_j)
			if j.find(i[0]) != -1 or set(tokens_i) == set(tokens_j) or  " ".join(tokens_j) in " ".join(tokens_i):
				contained = True
			differences = set(tokens_i).difference(tokens_j)
			if len(differences) <= 1 and 'actress' not in differences:
				contained = True
		if not contained:
			awards.append(i[0])
			print(i[0])

	return awards
