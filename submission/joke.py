# -*- coding: utf-8 -*-
import json
import nltk
import re
from nltk.corpus import stopwords
from classifier import *
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
from nltk.corpus import stopwords

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

def extract_names(document,namesdic):
	sentences = ie_preprocess(document)
	for tagged_sentence in sentences:
		for chunk in nltk.ne_chunk(tagged_sentence):
			if type(chunk) == nltk.tree.Tree:
				if chunk.label() == 'PERSON':
					# names.append(' '.join([c[0] for c in chunk]))
					temp = ' '.join([c[0] for c in chunk[0:2]])
					# A little bit change, set length to 2 which shows in [0:2]
					if len(temp.split())==2:

						if temp in namesdic:
							namesdic[temp] += 1
						else:
							namesdic[temp] = 1

def GetJoker(file):

	j_file=open(file)
	j_str=j_file.read()
	j_data=json.loads(j_str)
	namesdic={}
	jokeword = ['joke', 'lmao', 'lol', 'hhh', 'funny', '233','haha']
	for i in j_data:
		for j in jokeword:
			if j in i['text'].lower():
				extract_names(i['text'],namesdic)
	temp = sorted(namesdic.items(), key=lambda x: x[1], reverse=True)
	for i in temp[0:20]:
		if 'golden' in i[0].lower():
			continue
		print('The person who always said joke was ',i[0])
		return i[0]	
	j_file.close()
	return temp




def getJoke(file):
	j_file=open(file)

	j_str=j_file.read()
	j_data=json.loads(j_str)
	str1=''
	jokeword = ['joke', 'lmao', 'lol', 'hhh', 'funny', '233','haha']
	for i in j_data:
		for j in jokeword:
			if j in i['text'].lower():
				str1 += RemovePunctuation(i['text'].lower())
				token = nltk.word_tokenize(str1)
				tengram = ngrams(token, 10)
				elegram = ngrams(token, 11)
	# trigram = ngrams(token, 4)
				GG = Counter(tengram) + Counter(elegram)  # + Counter(trigram)
	print(GG.most_common(30))

