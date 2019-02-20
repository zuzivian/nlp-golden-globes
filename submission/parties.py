import difflib
import statistics
from classifier import *
from presenter import *

from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def dictCount(plist):
    common_ngrams = {}
    for p in plist:
        if p in common_ngrams.keys():
            common_ngrams[p] += 1
        else:
            common_ngrams[p] = 1

    return common_ngrams

def dictClean(plist3):
    unique_grams = {}
    threshold = statistics.mean(plist3.values()) // 2

    for phrase in plist3.keys():
        allscores = []
        if plist3[phrase] > threshold:
            for phrase3 in plist3.keys():
                if plist3[phrase3] > threshold:
                    if phrase != phrase3:
                        score = similar(phrase, phrase3)
                        allscores.append(score)
            if allscores and max(allscores) < 0.4: # Correct for Warner Brothers
                unique_grams[phrase] = plist3[phrase]

    return unique_grams

def getParty(year):
    dir_path = os.path.dirname(os.path.realpath(""))
    with open('gg' + str(year) + '.json') as f:
        data = json.load(f)
    alltweets = [tweetFull['text'] for tweetFull in data]

    # Failed classifier method
    #tweet_dict_by_award = get_classified_data(year)
    #alltweets = tweet_dict_by_award['party']
    stopWords = set(stopwords.words('english'))
    twitterwords = {"http", "rt", "goldenglobes", "golden", "globes", "golden", "globes", "globe"}
    stopWords = stopWords.union(twitterwords)

    partywords = ["party", "parties"]
    partyTweets = tweetTokenContain(alltweets, partywords, stopWords)
    partydata = partyTweets[1]

    party2 = []
    party3 = []

    for sentencelist in partydata:
        if "party" in sentencelist:
            pos = sentencelist.index("party")
            if pos > 0:
                describer_1 = sentencelist[pos - 1]
                describer_2 = ""
                if pos > 1:
                    describer_2 = sentencelist[pos - 2]

                if describer_1.istitle() == True:
                    partyname = describer_1
                    party2.append(partyname.replace("Bros", "Brothers"))
                    if describer_2.istitle() == True :
                        partyname = describer_2 + " " + describer_1
                        party3.append(partyname.replace("Bros", "Brothers"))

    p2 = dictCount(party2)
    p3 = dictCount(party3)

    largedict = {**dictClean(p2), **dictClean(p3)}
    parties = []

    for party in largedict.keys():
        pn = party + " " + "Party"
        parties.append(pn)
        print(pn)

    return parties
