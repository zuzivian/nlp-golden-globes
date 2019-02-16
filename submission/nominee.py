# -*- coding: utf-8 -*-
import json
import nltk
import re
from nltk.corpus import stopwords
from classifier import *
import re
from collections import Counter
from nltk.util import ngrams


stop = stopwords.words('english')

def ie_preprocess(document):
	document = ' '.join([i for i in document.split()])
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

def Achive_names(tweet,winner,threshhold):
    blacklist=['golden','best','globe','motion','actor','actress','hero','picture','drama']
    sum=0
    names={}
    sentences = ie_preprocess(tweet)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    #names.append(' '.join([c[0] for c in chunk]))
                    l=[]
                    for c in chunk[0:4]:
                        if c[0].lower() in blacklist:
                            break
                        else:
                            l.append(c[0])
                    
                    temp = ' '.join(l)
                    if len(temp.split())==2:
                        if temp not in names:
                            sum+=1
                            names[temp.lower()]=1
                        else:
                            names[temp.lower()]+=1
    if sum>=threshhold:
        return names
    return []


def getNominee(award,winner,j_data,winnerlist):
        res=[]
        sum=0
        if 'actor'in award or 'actress'in award or 'performance' in award or 'director'in award or'award'in award:
            for i in j_data:
                Final={}

                if winner in i['text'].lower():
                    result1=Achive_names(i['text'],winner,5)
                    if result1:
                        a=list(result1.keys())
                        if winner in a:
                            a.remove(winner)
                            return a
            return []
        #print(Final.keys())
        else:
            res=getMovieNom(winner)
            return res

def FilterCounter(black,C):
    res=[]
    for i in C.most_common(10):
        marker=0
        for j in i[0]:
            if j.lower() in black:
                marker=1
                break
        if marker==0:
            res.append(' '.join(k for k in i[0]).lower())
    return res


def getMovieNom(winner,file):
        f=open('MovieDatabase.txt',encoding='utf-16')
        moviedic={}
        for i in f.read().split('\n'):
            try:
                k=i
                if k:
                    moviedic[k.lower()]=1
            except:
                continue
        f.close()

        j_file=open(file)

        j_str=j_file.read()
        j_data=json.loads(j_str)
        sum=0
        movies = {}
        movies[winner]=1
        sum=0
        for i in j_data:
            names=[]

            if winner in i['text'].lower():
                token = nltk.word_tokenize(RemovePunctuation(i['text'].lower()))
                bigrams = ngrams(token,2)
                trigrams=ngrams(token,3)
                GG=Counter(bigrams)+Counter(trigrams)
                for i in GG.most_common(50):
                    #print(i)
                    xx=' '.join(k for k in i[0]).lower()
                    if 'the' in xx and len(xx.split())<3:
                        continue
                    #print(xx)
                    if xx in moviedic.keys():
                            movies[xx]=1
                            sum+=1
            if sum>10:
                break

        j_file.close()
        a=list(movies.keys())[0:6]
        if winner in a:
            a.remove(winner)
        return a
def filterNominee(l1,l2):
    counter=0
    for i in l1:
        if i in l2:
            counter+=1
        if counter>2:
            return False
    return True

def Nominee(file,awards,winnerDic):
    j_file=open(file)

    j_str=j_file.read()
    j_data=json.loads(j_str)
    res={}
    for i in awards:
        temp=getNominee(i,winnerDic[i],j_data,list(winnerDic.values()))
        res[i]=temp
    res['cecil b. demille award']=[]
    j_file.close()
    print(res)
    return res


