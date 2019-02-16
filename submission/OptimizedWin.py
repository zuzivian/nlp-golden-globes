# -*- coding: utf-8 -*-
import json
import nltk
import re
from nltk.corpus import stopwords
from classifier import *
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter


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




def GetWinner(tweet_dic,awardType,final):

	namesdic={}
	text = tweet_dic[awardType]
	counter = 0
	result = {}
	str1=""

	if 'actor' in awardType or 'actress' in awardType or 'performance' in awardType or 'director' in awardType or 'award' in awardType:
#award of people'name

		for i in text:

			try:
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
			if counter>2000:
				break
		topOccur = sorted(result.items(), key=lambda x: x[1], reverse=True)

		for i in topOccur:
			if i[0] in awardType.lower().split():
				continue
			for j in namesdic.keys():
				if i[0] in RemovePunctuation(j.lower()):
					if len(j.split()) == 2 and i[0] in RemovePunctuation(j.lower().split()[1]):
						final[awardType]=j.lower()
						return j.lower()

		#return topOccur[0][0]
		#print(topOccur[0][0])
		final[awardType]=topOccur[0][0]


	else:
		for i in text:
			str1 += RemovePunctuation(i)
		black = awardType.lower().split()  + ['the','musical', 'feature', 'film', 'goldenglobes', 'common', 'tv',
													'miniseries', 'a', 'movie','golden','globes']
		token = nltk.word_tokenize(str1)
		unigram = ngrams(token, 1)
		bigrams = ngrams(token, 2)
		# trigram = ngrams(token, 4)
		GG = Counter(bigrams) + Counter(unigram)  # + Counter(trigram)
		# print(GG.most_common(10))
		x = FilterCounter(black, GG)
		final[awardType] = x


# return None
def FilterCounter(black,C):
	marker=0
	for i in C.most_common(20):
		if len(i[0])==1 and len(i[0][0])<=3:
			continue
		marker=0
		#print(i)
		for j in i[0]:
			#print(j)
			if j.lower() in black:
				marker=1
				break
		if marker==1:
			continue
		return ' '.join(k for k in i[0]).lower()
	return None


# if __name__ == '__main__':
# 	#print(GetWinner(u"Best Original Song - Motion Picture"))
# 	#m=tweet_dic["Best Television Series - Musical or Comedy"]
# 	for i in gg2013_categories:
# 		print(i, ':',GetWinner(i))
# 		print('\n')
# 	#GetWinner("Best Television Series - Musical or Comedy")
