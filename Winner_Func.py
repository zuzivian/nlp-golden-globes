# -*- coding: utf-8 -*-
import json
import nltk
import re
from nltk.corpus import stopwords
from classifier import *
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter

ListForOneword = [
	u"Best Motion Picture - Drama",
	u"Best Motion Picture - Animated",
	u"Best Motion Picture - Foreign Language",
	u"Best Original Song - Motion Picture",
	u"Best Television Series - Drama",
	u"Best Television Series - Musical or Comedy",
]

tweet_dic = get_and_classify_tweets('./data/gg2013.json', 1000000, gg2013_categories)
stop = stopwords.words('english')


def ie_preprocess(document):
	document = ' '.join([i for i in document.split() if i not in stop])
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	return sentences


def RemovePunctuation(line):
	s = "!#$%&()*+,-./:;<=>?@[\]^_`{'~}"
	s += '"1234567890'
	for x in s:
		line = line.replace(x, '')
	return line


def GetFormerWord(sen1, w1):
	word_list = nltk.word_tokenize(sen1)
	for i in range(1, len(word_list)):
		if word_list[i] == w1:
			return RemovePunctuation(word_list[i - 1]).lower()
	return None


def GetLatterWord(sen1, w1):
	word_list = nltk.word_tokenize(sen1)
	for i in range(0, len(word_list) - 2):
		if word_list[i].lower() == w1:
			return RemovePunctuation(word_list[i + 2]).lower()
	return None


def extract_names(document,namesdic):
	sentences = ie_preprocess(document)
	for tagged_sentence in sentences:
		for chunk in nltk.ne_chunk(tagged_sentence):
			if type(chunk) == nltk.tree.Tree:
				if chunk.label() == 'PERSON':
					# names.append(' '.join([c[0] for c in chunk]))
					temp = ' '.join([c[0] for c in chunk[0:2]])
					# A little bit change, set length to 2 which shows in [0:2]
					if temp in namesdic:
						namesdic[temp] += 1
					else:
						namesdic[temp] = 1


def SearchName(NameDic, segment):
	RealNames = []
	for j in NameDic.keys():
		if segment in j.lower():
			RealNames.append(j.lower())
	return RealNames


def GetWinner(awardType):
	# awardtype should be unicoded
	namesdic={}
	text = tweet_dic[awardType]

	counter = 0
	blacklist = ['olden', 'lobes']
	name_list = {}
	result = {}
	for i in text:
		try:
			# print(i['text'])
			temp = GetFormerWord(i, 'wins')

			temp1 = GetLatterWord(i, 'to')
			temp2 = GetFormerWord(i, 'won')

			extract_names(i,namesdic)
			if temp:
				if temp in result:
					result[temp] += 1
				else:
					result[temp] = 1
			if temp1:
				if temp1 in result:
					result[temp1] += 1
				else:
					result[temp1] = 1
			if temp2:
				if temp2 in result:
					result[temp2] += 1
				else:
					result[temp2] = 1

			counter += 1
		except:
			continue
		if counter >= 2000:
			break
	#print(namesdic)
	if awardType in ListForOneword:
#award of movie
		temp = sorted(result.items(), key=lambda x: x[1], reverse=True)[0:10]
		for x in temp:
			for j in namesdic:
				if x[0] in j.lower():
					# print(x[0].encode('ascii','ignore'))
					return x[0]

	else:
#award of people'name
		topOccur = sorted(result.items(), key=lambda x: x[1], reverse=True)
		#print(topOccur)
		max = 0
		maxName = ''
		for i in topOccur:
			for j in namesdic.keys():
				if i[0] in RemovePunctuation(j.lower()):
					if len(j.split()) == 2 and i[0] in RemovePunctuation(j.lower().split()[1]):
						return j.lower()

		return topOccur[0][0]


if __name__ == '__main__':
	#print(GetWinner(u"Best Original Song - Motion Picture"))
	# m=tweet_dic[u"Best Motion Picture - Drama"]
	# str1=""
	# for i in m:
	# 	i=RemovePunctuation(i)

	# 	str1+=i
	# counter=0

	# token = nltk.word_tokenize(str1)
	# bigrams = ngrams(token,3)
	# print(Counter(bigrams))
	for i in gg2013_categories:
		print(i, ':',GetWinner(i))
		print('\n')




