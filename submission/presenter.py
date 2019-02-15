from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk import bigrams, trigrams
import json
from pprint import pprint
import os
import timeit

from classifier import *
from helpers import *

def contains(a, b):
    a_set = set(a)
    b_set = set(b)
    if len(a_set.intersection(b_set)) > 0: 
        return True
    else:
        return False   

def tweetTokenRmStop(tweetdata, stopwords):
    tweetlist = []
    i = 0

    for i in range(len(tweetdata)):
        tweettextToken = []
        words = word_tokenize(tweetdata[i])
        words_clean = [token for token in words if token.lower() not in stopwords and token.isalpha()]
        tweetlist.append(words_clean)
        
        i += 1 
    return(tweetlist)   
    
def tweetTokenContain(tweetdata, keywords, stopwords):
    tweetnumber = []
    tweetlist = []
    i = 0

    for i in range(len(tweetdata) - 1):
        tweettextToken = []
        words = word_tokenize(tweetdata[i])
        words_clean = [token for token in words if token.lower() not in stopwords and token.isalpha()]
        
        if contains(words_clean, keywords) == True:
            tweetnumber.append(i)
            tweetlist.append(words_clean)
        
        i += 1
        
    return([tweetnumber, tweetlist])

def tweetPrint(tweetdata, tweetnumber):
    return [tweetdata[i] for i in tweetnumber]

def unigramsDict(tweetTokens):

    common_unigrams = {}
    
    for sentence in tweetTokens:
        for ug in sentence:
            if ug in common_unigrams.keys():
                common_unigrams[ug] += 1
            else:
                common_unigrams[ug] = 1
    
    d_view = [ (v,k) for k,v in common_unigrams.items() ]
    return d_view

def bigramsDict(tweetTokens):

    common_bigrams = {}
    
    for sentence in tweetTokens:
        bigrm_in_tweet = list(bigrams(sentence))
        for bg in bigrm_in_tweet:
            if bg in common_bigrams.keys():
                common_bigrams[bg] += 1
            else:
                common_bigrams[bg] = 1
    
    d_view = [ (v,k) for k,v in common_bigrams.items() ]
    return d_view

def printDictbyCount(dict_view, maximum = 200):
    dict_view.sort(reverse=True) # natively sort tuples by first element
    counter = 0
    
    for v,k in dict_view:
        pprint("%s: %d" % (k,v))
        counter+=1

        if counter > maximum:
            break
            
def checkFullNameFormat(inputTupleN):
    word1 = inputTupleN[0]
    word2 = inputTupleN[1]
    if len(word1) > 1 and len(word2) > 1:
        if word1[0].isupper() == True and word1[1].islower() == True and word2[0].isupper() == True and word2[1].islower() == True:
            return True
    else:
        return False
    
def extractPseudoNames(input_dict, lowbound = 10):

    pseudo_namelist = []
    
    for wordpair in input_dict:
        if wordpair[0] >= lowbound and checkFullNameFormat(wordpair[1]) == True:
            name_like = wordpair[1][0].lower() + " " + wordpair[1][1].lower()
            #name_like = wordpair[1][0] + " " + wordpair[1][1]
            pseudo_namelist.append(name_like)
        
    return(pseudo_namelist)

def namesValidate(tweetText, stopwords, threshold = 2):
    #tweet_present_tokenized = tweetTokenContain(tweetText, keyword, stopWords)
    #tweet_present_tokenized_list = tweet_present_tokenized[1]
    tweet_present_tokenized_list = tweetTokenRmStop(tweetText, stopwords)
    common_bigrams_dict = bigramsDict(tweet_present_tokenized_list)
    #printDictbyCount(common_bigrams_dict)
    nameslist = extractPseudoNames(common_bigrams_dict, threshold)
    #tct = tweet_present_tokenized[0]
    #tweet_present = tweetPrint(testdoc, tct)
    
    return nameslist

def tweetTextContain(tweetTextList, keywords):
    tweetnumber = set([])
    i = 0

    for i in range(len(tweetTextList) - 1):
        
        for keyword in keywords:
            if keyword in tweetTextList[i].lower():
                tweetnumber = tweetnumber.union([i])
        
        i += 1
        
    return list(tweetnumber)

def subjverb_tweets(tweetdata, names, keywordlist):
    nameslist = []
    additionalNamesParsing = []
    i = 0

    for i in range(len(tweetdata)):
        tweetsentence = "OT: " + tweetdata[i].lower()
        for name in names:
            tweetsplit = tweetsentence.split(name)
            if len(tweetsplit) > 1:
                for part in tweetsplit:
                    if len(part) > 1:
                        parttoken = word_tokenize(part)
                        if len(parttoken) > 1:
                            immediateWords = [parttoken[0], parttoken[1]]
                        else:
                            immediateWords = [parttoken[0]]
                        
                        if contains(immediateWords, keywordlist) == True:
                            nameslist.append(name)
                            sentenceB4 = tweetsplit[0]
                            additionalNamesParsing.append(sentenceB4)
        i += 1
        
    for b4string in additionalNamesParsing:
        for name in names:
            if name in b4string:
                nameslist.append(name)
    
    #return nameslist
    return nameslist

def nameCountValidate(inputList):
    freqDict = {x:inputList.count(x) for x in inputList}
    #print(freqDict)
    names = freqDict.keys()
    numCounts = len(inputList)
    numNames = len(names)
    names_del_list = []
    
    # Odd occurence deletion
    for name in names:
        if freqDict[name] / numCounts < 1 / numNames * 0.9:
            #print(name + " deleted")
            names_del_list.append(name)
    
    for name in names_del_list:
        del freqDict[name]
        
    return freqDict

def nameAccuValidate(freqDict):
    names = list(freqDict.keys())
    # Case 1: Three word names
    if len(names) == 2:
        name1 = names[0].split()
        name2 = names[1].split()
        if name1[0] == name2[1] and name1[1] != name2[0]:
            realname = name2[0] + " " + name2[1] + " " + name1[1]
            return [realname]
        elif name1[0] != name2[1] and name1[1] == name2[0]:
            realname = name1[0] + " " + name1[1] + " " + name2[1]  
            return [realname]
        elif names[0] in names[1]:
            return [names[1]]
        elif names[1] in names[0]:
            return [names[0]]
        else:
            return names
    
    # Case 2: Three presenters due to wrong names
    elif len(names) > 2:
        print(names[2] + " deleted")
        return names[0:2]
    else:
        return names


def getPresenters(year):
	'Load Data'
    tweet_dic = get_classified_data(year)
    awardcat = tweet_dic.keys()
    presenter_dict = {}

    'Stopword and keyword manipulation'
    stopWords = set(stopwords.words('english'))
    twitterwords = {"http", "rt", "goldenglobes", "golden", "globes", "golden", "globes", "globe"}
    stopWords = stopWords.union(twitterwords)
    new_stopWords = [award.split() for award in awardcat]
    award_stopwords = []
    for k in new_stopWords:
        award_stopwords = set(award_stopwords).union(set(k))
    new_stopWords = [i.lower() for i in award_stopwords]
    
    stopWords = stopWords.union(new_stopWords)
    keyword = ['present', 'presenting', 'presented', 'presents', 'presenter', 'presenters', 
               'introduce', 'introducing', 'introduces', 'introduced',
               'announce', 'announcing', 'announces', 'announces']

	#alltweets = [data[i]['text'] for i in range(len(data))]
    #all_pseudo_namelist = namesValidate(alltweets, stopWords, threshold = 50)
    
    for award in awardcat:
        #print()
        #print(award + ":")
        testdoc = tweet_dic[award]
        #pseudo_namelist = all_pseudo_namelist
        pseudo_namelist = namesValidate(testdoc, stopWords, threshold = 1)
        
        tweetSeq = tweetTextContain(testdoc, keyword)
        category_tweet = [testdoc[i] for i in tweetSeq]
        tweetInfo = subjverb_tweets(category_tweet, pseudo_namelist, keyword)
        presenter_info = nameCountValidate(tweetInfo)
        presenter = nameAccuValidate(presenter_info)
        print(presenter)
        presenter_dict[award] = presenter

    return presenter_dict