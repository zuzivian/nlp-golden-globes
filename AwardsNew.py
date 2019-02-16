#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
import re
import json
import nltk
from nltk.tokenize import RegexpTokenizer
import difflib


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']


def read_data(year):

    # read data
    df = pd.read_json('gg' + year + '.json')
    rawdata = df['text']

    # sample data if necessary
    sample_size = 200000
    if len(df) > sample_size:
        rawdata = rawdata.sample(n=sample_size)

    # clean tweets
    data = []
    for tweet in rawdata:
        line = remove_hashtag(tweet)
        line = remove_at(line)
        line = remove_url(line)
        line = cleanse(line)
        data.append(line)
    return data


def find_awards(data):
    endlist = ['picture', 'television', 'drama', 'film', 'musical']
    awards = {}
    for item in data:
        l = item.lower().split()
        for j in endlist:
            if 'best' in l and j in l:
                temp1 = l.index('best')
                temp2 = l.index(j)
                if temp1 < temp2:
                    l2 = ['television' if x == 'tv' else x for x in l]
                    # l3 = ['film' if x == 'movie' else x for x in l]
                    key1 = " ".join(l2[temp1:temp2 + 1])
                    if key1 not in awards:
                        awards[key1] = 1
                    else:
                        awards[key1] += 1
    res = []
    #res.append('cecil b.demille award')
    for item in awards:
        if awards.get(item) > 60:
            l = item
            if len(l.split()) > 3:
                res.append(item)

    removelist = []
    for i in range(0, len(res) - 1):
        for j in range(i + 1, len(res)):
            if stringMatch(res[i], res[j]):
                if len(res[i]) > len(res[j]):
                    removelist.append(res[j])
                else:
                    removelist.append(res[i])

    for item in removelist:
        if item in res:
            res.remove(item)

    for item in res:
        print(item)

    # sorted(awards.items(), key=lambda x: x[1], reverse=True)
    return res[0:30]





def main(year):

    data = read_data(year)
    res = find_awards(data)
    return res


def stringMatch(a,b):
    if len(a) > len(b):
        return b in a
    return a in b
