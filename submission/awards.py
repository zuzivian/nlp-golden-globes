# -*- coding: utf-8 -*-
import json
import nltk
import re
from nltk.corpus import stopwords

# Winner:
# Some point of view:
# Get the former word of  ‘wins’ ‘won’
# Get the latter word of ‘goes to’

# However, if the awards winner is a single word, it will work.For example, ‘Argo’ ‘skyfall’ etc..

# If the awards winner is a people’s name, usually two words(such as ‘ben afflick’ ‘anny hathway’),
# it won’t work.

# The way to solve this problem is to still get the single word, and then at the same time,
# I create a name list which saves all of the possible names.
# And then use the single word to compare with those possible names,
#if the single word is a substring of one of the possible names, then take it. The result seems good by using this method.


#And now it's very important to classify award into two types:
#1.the award whose winner names are single word
#2.the award whose winner names are two words(usually people's name)

def ie_preprocess(document):
	stop = stopwords.words('english')
	document = ' '.join([i for i in document.split() if i not in stop])
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	return sentences

def IsRepeatedName(l1,l2):
	a=l1.split()
	b=l2.split()
	if len(a)==2 and len(a)==len(b):
		if a[0]==b[1] and a[1]==b[0]:
			return True
	return False

#(Amy,Tina) and (Tina,Amy) are repeated.They can't be our result.
#Those situations should be excluded

def IsInblacklist(blacklist,l):
	for i in blacklist:
		if i in l:
			return True
	return False

#we assume that only names with lenth equals to 2 are legal.

def IsLegalName(l1):
	if len(l1.split())!=2:
		return False
	return True

def RemovePunctuation(line):
	s="!#$%&()*+,-./:;<=>?@[\]^_`{'~}"
	s+='"1234567890'
	for x in s:
		line=line.replace(x,'')
	return line

def GetFormerWord(sen1,w1):
	word_list=nltk.word_tokenize(sen1)
	for i in range(1,len(word_list)):
		if word_list[i]==w1:
			return RemovePunctuation(word_list[i-1]).lower()
	return None

def EndAndStart(result,tweet,startlist,endlist):
	for i in startlist:
		for j in endlist:
			l=tweet.lower().split()
			if  i in l and j in l:
				temp1=l.index(i)
				temp2=l.index(j)
				if temp1>temp2:
					continue
				txt=l[temp1:temp2+1]
				if '-' in txt:
					if len(l[temp1:temp2+1])>=4:
						key1=" ".join(i for i in l[temp1:temp2+1])
						if key1 not in result:
							result[key1]=1
						else:
							result[key1]+=1
	return result


def GetLatterWord(sen1,w1):
	word_list=nltk.word_tokenize(sen1)
	for i in range(0,len(word_list)-2):
		if word_list[i].lower()==w1:
			return RemovePunctuation(word_list[i+2]).lower()
	return None



def extract_names(document):
    names = []

    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
                    temp=' '.join([c[0] for c in chunk[0:2]])
                    #A little bit change, set length to 2 which shows in [0:2]
                    if temp in namesdic:
                    	namesdic[temp]+=1
                    else:
                    	namesdic[temp]=1
    return names

def judge(document):
	sentences = ie_preprocess(document)
	for tagged_sentence in sentences:
		sum=0
		uses=[]
		for chunk in nltk.ne_chunk(tagged_sentence):
			if type(chunk) == nltk.tree.Tree:
				if chunk.label() == 'PERSON':
					temp=' '.join([c[0] for c in chunk[0:2]])

					if len(temp.split())==2:
						uses.append(temp)
						sum+=1
		if sum>3:
			return True

	return False


def SearchName(NameDic,segment):
	RealNames=[]
	for j in NameDic.keys():
		if segment in j.lower():
			RealNames.append(j.lower())
	return RealNames


def generate_awards(year):
	j_file=open('gg%s.json' % year)
	j_str=j_file.read()
	j_data=json.loads(j_str)
	result={}
	#tokens=nltk.word_tokenize(j_data[1]['text'])
	blacklist=['olden','lobes']
	name_list = {}

	for i in j_data:
		result = EndAndStart(result, i['text'],['best'],['picture','television','drama','comedy','musical', 'animated', 'language'])

	temp = sorted(result.items(), key=lambda x: x[1], reverse=True)
	temp = sorted(temp, key=lambda x: len(x[0]), reverse=True)

	award_tuples = []
	for i in temp:
		contained = False
		for j in award_tuples:
			if i[0] in j[0]:
				contained = True
		if not contained:
			award_tuples.append(i)

	award_tuples = sorted(award_tuples, key=lambda x: x[1], reverse=True)

	awards = []
	for item in award_tuples:
		if item[1] < 10:
			continue
		awards.append(item[0])

	for i in awards:
		print(i.encode('ascii', 'ignore'))

	return awards
