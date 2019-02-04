# -*- coding: utf-8 -*-
import json
import nltk
import re
from nltk.corpus import stopwords
from classifier import *

# Nat's code for classifiying tweets
# Usage: tweet_dic['Best Screenplay - Motion Picture'] : returns a list of strings (unicode)

tweet_dic = get_and_classify_tweets('./data/gg2013.json', 1000000, gg2013_categories)
test=tweet_dic[]

stop = stopwords.words('english')
namesdic={}

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

def SearchName(NameDic,segment):
	RealNames=[]
	for j in NameDic.keys():
		if segment in j.lower():
			RealNames.append(j.lower())
	return RealNames

#Both json file has been tested and can successfully obtained the result
j_file=open('gg2013.json')
#j_file=open('gg2015.json')
j_str=j_file.read()
j_data=json.loads(j_str)
x=[]
#tokens=nltk.word_tokenize(j_data[1]['text'])
counter=0
blacklist=['olden','lobes']
#we can update the blacklist later
name_list={}
result={}
#xxx wins
#xxx awards goes to
#"awardname"-
for i in j_data:
	#print(i['text'].encode('ascii', 'ignore'))
	if 'Best Motion Picture drama'.lower() in i['text'].lower():
		try:
			# print(i['text'])
			temp=GetFormerWord(i['text'],'wins')

			temp1=GetLatterWord(i['text'],'to')
			temp2=GetFormerWord(i['text'],'won')
			extract_names(i['text'])
			if temp:
				if temp in result:
					result[temp]+=1
				else:
					result[temp]=1
			if temp1:
				if temp1 in result:
					result[temp1]+=1
				else:
					result[temp1]=1
			if temp2:
				if temp2 in result:
					result[temp2]+=1
				else:
					result[temp2]=1

			counter+=1

		except:
			continue
	if counter>=20000:
		break
print(result)

#find name in the namelist

# for i in result:
# 	try:
# 		print(i,result[i])
# 	except:
# 		continue
# for i in result:
# 	for j in namesdic.keys():
# 		if i in j.lower():
# 			print(j)
