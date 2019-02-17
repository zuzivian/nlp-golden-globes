# -*- coding: utf-8 -*-
import json
import nltk
import re
from nltk.corpus import stopwords

stop = stopwords.words('english')
result={}

def RemovePunctuation(line):
	s="!#$%&()*+,-./:;<=>?@[\]^_`{'~}"
	s+='"1234567890'
	for x in s:
		line=line.replace(x,'')
	return line


def EndAndStart(tweet,startlist,endlist):
	for i in startlist:
		for j in endlist:
			l=tweet.lower().split()
			if  i in l and j in l:
				temp1=l.index(i)
				temp2=l.index(j)
				if i<j:
					txt=l[temp1:temp2+1]
					if '-' in txt:
						if len(l[temp1:temp2+1])>=4:
							key1=" ".join(i for i in txt)
							if key1 not in result:
								result[key1]=1
							else:
								result[key1]+=1

								
								

def getawards(year):
	j_file=open('gg%s.json' % year)
	j_str=j_file.read()
	j_data=json.loads(j_str)

	for i in j_data:
		EndAndStart(i['text'],['best'],['picture','tv','drama','musical','animated'])

	temp = sorted(result.items(), key=lambda x: x[1], reverse=True)[0:28]
	res=[]
	for i in temp:
		length=len(RemovePunctuation(i[0]).split())
		if length<=3:
			continue
		s=i[0].replace('tv', 'television')
		if 'comedy' in s and 'musical' not in s:
			res.append(s.replace('comedy','comedy or musical'))
		elif 'musical' in s and 'comedy' not in s:
			res.append(s.replace('musical', 'comedy or musical'))
		else:
			res.append(s)


	return res
