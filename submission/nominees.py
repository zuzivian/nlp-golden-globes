# -*- coding: utf-8 -*-
import json
from nltk import word_tokenize
from classifier import *
from collections import Counter
from operator import itemgetter

def get_tweets(year):
    
    # get tweets
    with open('gg%s.json' % year) as json_data:
        data = json.load(json_data)
    json_data.close()
    
    #stopWords = set(stopwords.words('english'))
    stopWords_tweets = ['http','rt','goldenglobes','golden','globes','rt','golden','globes','globe' \
                        'goldenglobes','goldenglobe']    
    keywords = ['best','winner','wins','award','awards','nominees','nominated','congratulates',\
                'congratulations','congrats','announce','announcing','present']
    
    # tokenize tweets and select matching tweets
    start = 0
    end = len(data)
    word_list = []  
    for q in range(start, end):
        words = word_tokenize(data[q]['text'])
        
        # convert to lower case
        text = [words[i].lower() for i in range(len(words))]
        
        words_meaningful = [token for token in text if token not in stopWords_tweets and token.isalpha()]
        if len(list(set(words_meaningful) & set(keywords)))>0:
            word_list.append(words_meaningful)
    
    return word_list  


def get_awardsKeywords(year):
    
    # get awards
    with open('classified%d.json' % year) as json_data:
        awards = json.load(json_data)
    json_data.close()

    awards_keys = list(awards.keys())
    awards_keywords = []
    for i in range(len(awards_keys)):
        # tokenize awards words
        awards_token = word_tokenize(awards_keys[i])
        # find awards keywords
        awards_temp = []
        stopWords_awards = ['by', 'an', 'in', 'a', 'for', 'or', '-', ',']
        j = 0
        while len(awards_temp) < 5 and j < len(awards_token):
            if awards_token[j] not in stopWords_awards:
                awards_temp.append(awards_token[j])
                j = j + 1
            else:
                j = j + 1
        awards_keywords.append(awards_temp)
        
    return awards_keywords


def get_nominees_raw(year, awards):
    
    word_list = get_tweets(year)
    awards_keys = list(awards.keys())   
    awards_keywords = get_awardsKeywords(year)
    tweets_stopwords = ['best','better','winner','wins','won','winning','presents','at','for',
                        'in','to','award','awards','nominees','nominated','congratulates','congratulations',
                        'congrats','Congrats','was','a','an','i','announced','announce', 'announcing','present',
                       'by','with','the', 'todayshow','of','latest','movie','film','is','awarded','and',
                       'actor','globe','or','picture','animated','animation','motion','from']
    
    # get tweets with possible nominees
    nominees_raw = {}
    for i in range(len(awards_keywords)):
        nom_values = []
        # get the matching tweets
        for j in range(len(word_list)):
            if set(awards_keywords[i]) <= set(word_list[j]):
                
                wordList_copy = word_list[j].copy()
                
                # exclude awards_keywords
                for ak in awards_keywords[i]:
                    wordList_copy.remove(ak)
                # exculde tweets_stopwords
                wordList = [item for item in wordList_copy if item not in tweets_stopwords]
                nom_values.append(wordList)
            else:
                continue

        nominees_raw[awards_keys[i]] = nom_values
      
    return nominees_raw


def get_nominees(year):
    
    # get awards
    with open('classified%d.json' % year) as json_data:
        awards = json.load(json_data)
    
    # get refined nominees
    nominees = {}
    nominees_raw = get_nominees_raw(year, awards)
    nominees_raw_val = list(nominees_raw.values())
    nominees_raw_key = list(nominees_raw.keys())
    
    for i in range(len(nominees_raw_val)):
        
        # concatenate nominees according to awards
        nom_val = [n for nv in nominees_raw_val[i] for n in nv]
        
        if nom_val == []:
            nominees[nominees_raw_key[i]] = []
        elif len(nom_val) < 5:
            nominees[nominees_raw_key[i]] = nom_val
        elif len(nom_val) >= 5:
            cnt = Counter(nom_val)
            sorted_cnt = sorted(cnt.items(), key=itemgetter(1))
            nominees[nominees_raw_key[i]] = [sorted_cnt[-1][0],sorted_cnt[-2][0],sorted_cnt[-3][0],sorted_cnt[-4][0],sorted_cnt[-5][0]]
        
    return nominees
   

nominees = get_nominees(2013)
nom_key = list(nominees.keys())
nom_val = list(nominees.values())
for i in range(len(nominees)):
    print(nom_key[i], ' : ', nom_val[i])




