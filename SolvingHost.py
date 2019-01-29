# -*- coding: utf-8 -*-
import json
import nltk
import re
from nltk.corpus import stopwords
stop = stopwords.words('english')
namesdic={}

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




def extract_names(document):
    names = []
    
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
                    temp=' '.join([c[0] for c in chunk])
                    if temp in namesdic:
                    	namesdic[temp]+=1
                    else:
                    	namesdic[temp]=1
    return names


j_file=open('gg2013.json')
#j_file=open('gg2015.json')
j_str=j_file.read()
j_data=json.loads(j_str)
x=[]
#tokens=nltk.word_tokenize(j_data[1]['text'])
counter=0
blacklist=['olden','lobes']
#we can update the blacklist later
for i in j_data:
	if 'host' in i['text']:
		try:
			x+=extract_names(i['text'])
			
			counter+=1
		except:
			continue
	if counter>2000:
		break

#select the top20 names(according how often they occur) 
temp=sorted(namesdic.items(),key = lambda x:x[1],reverse = True)[0:20]


#exclude the names which are in blacklist such as golden globes...blablabla
result=[]
for i in temp:
	if not IsInblacklist(blacklist,i[0]):
		result.append(i)


#exlude the repeated ones and get our host result

FinalResult=[]
marker=0
for i in result:
	for j in result:
		if IsRepeatedName(i[0],j[0]):
			marker=1
			break
	if marker==1:
		marker=0
		continue
	if IsLegalName(i[0]):
		FinalResult.append(i[0])


print(FinalResult[0:2])





