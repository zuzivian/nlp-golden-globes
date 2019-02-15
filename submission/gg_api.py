import json
import os
from pprint import pprint

from awards import *
from dressed import *
from classifier import *
from OptimizedWin import *
from SolvingHost import *
from presenter import *
MAX_TWEETS = 10000000
YEARS = [2013, 2015, 2018, 2019]

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

'''
START HELPERS
'''

def get_classified_data(year):
    with open('classified%s.json' % year) as json_data:
        data = json.load(json_data)
    json_data.close()
    return data

def get_redcarpet(year):
    tweet_dict_by_award = get_classified_data(year)
    red_carpet_tweets = tweet_dict_by_award['red carpet']
    dict = analyze_sentiment_of_tweets(red_carpet_tweets)
    ranked_tuple = sorted(dict.items(), key=lambda kv: kv[1])
    print(ranked_tuple)
    return {'best dressed': ranked_tuple[-1][0], 'worst dressed': ranked_tuple[0][0]}

def get_jokes(year):
    return {}

def get_parties(year):
    return {}

'''
END OF HELPERS
'''

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    hosts=GetHost('gg%s.json' % year)
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    awards = generate_awards(year)
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    nominees = {}
    return nominees

def get_winner(year):
    dic=get_classified_data(year)

    winner= {}
    if year=='2013'or year=='2015':
        for i in OFFICIAL_AWARDS_1315:
            GetWinner(dic,i,winner)

    else:
        for i in OFFICIAL_AWARDS_1819:
            GetWinner(dic,i,winner)

    return winner

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    presenters = getPresenters(year)
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''

    print("Pre-ceremony processing complete.")
    return

def post_ceremony():
    # loading corpuses from file
    for year in YEARS:
        print('Loading gg%d tweets...' % year)
        if os.path.exists("classified%d.json" % year):
          continue
        try:
            award_list = OFFICIAL_AWARDS_1315 if year < 2016 else OFFICIAL_AWARDS_1819
            classified_tweets = get_and_classify_tweets('gg%d.json' % year, MAX_TWEETS, award_list, ['red carpet'])
            with open('classified%d.json' % year, 'w') as outfile:
                json.dump(classified_tweets, outfile)
            print('Classifying gg%d tweets... done.' % year)
        except:
            print('Could not load gg%d.json.' % year)
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here

    while True:
        print()
        year = int(input("Select a year: "))
        if year not in YEARS:
            print("Error: invalid year")
            continue
        print('Valid functions: hosts awards nominees presenters redcarpet jokes parties')
        choice = input("Select function: ")
        if choice == 'hosts':
            output = get_hosts(year)
        elif choice == 'awards':
            output = get_awards(year)
        elif choice == 'nominees':
            output = get_nominees(year)
        elif choice == 'presenters':
            output = get_presenters(year)
        elif choice == 'redcarpet':
            output = get_redcarpet(year)
        elif choice == 'jokes':
            output = get_jokes(year)
        elif choice == 'parties':
            output = get_parties(year)
        else:
            print("Error: Invalid response")
            continue

        # process data and print out nicely
        print("\n" + str(year) + " " + choice + ": \n")
        pprint(output)

if __name__ == '__main__':
    post_ceremony()
    main()
