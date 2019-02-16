# -*- coding: utf-8 -*-
import json
import nltk
import re
from nltk.corpus import stopwords
from classifier import *
import re
from collections import Counter

from textblob import TextBlob





def sentiAnalyzer(keyword,file):
	j_file=open(file)
	#j_file=open('gg2015.json')
	j_str=j_file.read()
	j_data=json.loads(j_str)
	userid={}
	counter=0
	neutral=0
	positive=0
	negative=0

	for i in j_data:
		for j in keyword:

				if j in i['text'].lower():
					counter+=1
					analysis=TextBlob(i['text']).sentiment[0]
					if analysis>0:
						positive+=1
					elif analysis<0:
						negative+=1
					else:
						neutral+=1
	# print('negative',negative)
	# print('positive',positive)
	# print('neutral',neutral)

	# print(maxmax)
	maxmax=max(negative,positive,neutral)
	ratio=(maxmax-neutral)/maxmax

	if ratio<=0.2:
		return 'neutral'
	elif max==negative:
		return 'negative'
	else:
		return 'positive'
