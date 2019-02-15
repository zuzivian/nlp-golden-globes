import nltk
from nltk.tokenize import TweetTokenizer
import datetime
import string
import os

# define globals
dir_path = os.path.dirname(os.path.realpath(__file__))

# stop words
def get_stopwords():
    stop_words = nltk.corpus.stopwords.words('english')
    twitter_words = ["http", "rt"]
    gg_words = ['golden', 'globes', 'globe']
    return stop_words + twitter_words + gg_words

def get_replacewords():
    return {
        'television': 'tv',
        'picture': 'movie',
        'mini-series': 'limited',
        'miniseries': 'limited',
    }

def remove_stopwords(words, stop_words, replace_words={}):
    processed_list = []
    for w in words:
        if w not in stop_words and w not in processed_list:
            if w in replace_words.keys():
                processed_list.append(replace_words[w])
            processed_list.append(w)
    return processed_list


def content_fraction(words):
    stop_words = get_stopwords()
    content = [w for w in words if w.lower() not in stop_words]
    return len(content) / len(words)


# tokenize
def twitter_tokenize(text, preserve_case=False):
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=preserve_case)
    return tknzr.tokenize(text)

def tokenize_multiple_texts(listof_texts):
    tokenized_words = []
    for text in listof_texts:
        tokenized_words.extend(twitter_tokenize(text))
    return tokenized_words

def strip_punctuation(words):
    translate_table = dict((ord(char), None) for char in string.punctuation)
    new_words = []
    for w in words:
        new_word = w.translate(translate_table)
        if new_word:
            new_words.append(new_word)
    return new_words




# returns a dict containing frequency of words in list
def get_word_freq_dict(words):
    words_sorted_by_freq = {}
    for word in words:
        if word in words_sorted_by_freq.keys():
            words_sorted_by_freq[word] += 1
        else:
            words_sorted_by_freq[word] = 1
    return words_sorted_by_freq

# printing
def print_dict(dict):
    date = datetime.datetime.now()
    file = open(dir_path + '/output/' + str(date) + ".txt", "w")

    d_view = [ (v,k) for k,v in dict.iteritems() ]
    d_view.sort(reverse=True) # natively sort tuples by first element
    for v,k in d_view:
        file.write("%s: %s\n" % (k.encode('ascii', 'ignore'),str(v)))

    file.close()




def ie_preprocess(document):
	stop = get_stopwords()
	document = ' '.join([i for i in document.split() if i not in stop])
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	return sentences


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


def SearchName(NameDic,segment):
	RealNames=[]
	for j in NameDic.keys():
		if segment in j.lower():
			RealNames.append(j.lower())
	return RealNames


def extract_names(document):
    names = []
    namesdic = {}

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

#we assume that only names with length 2 are legal.
def IsLegalName(name):
	return len(name.split()) == 2

# "Fey, Tina" and "Tina Fey" are the same person
def IsRepeatedName(l1,l2):
    a = l1.split()
    b = l2.split()
    if ((len(a) != 2) or (len(b) != 2)):
        return False
    return a[0] == b[1] and a[1] == b[0]

def get_classified_data(year):
    with open('classified%s.json' % year) as json_data:
        data = json.load(json_data)
    json_data.close()
    return data
