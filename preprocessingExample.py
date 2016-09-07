# -*- coding: utf-8 -*-
import re
import json
import operator
from collections import Counter
from nltk.corpus import stopwords
import string

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

# defining stopwords 
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['RT', 'via', 'The' , '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '10']
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

fileName = 'AtlantaDream052916.json'
with open(fileName, 'r') as f:
    countAll = Counter()
    countTerms = Counter()
    countHash = Counter()
    countMention = Counter()

    for line in f:
        tweet = json.loads(line) # load it as Python dict
        tokenList = preprocess(tweet['text'].encode('ascii', 'ignore')) # list of tokens created from this tweet
        
        termsAll = [term for term in tokenList if term not in stop]  # all terms including stop words
        termsTerms = [term for term in tokenList if term not in stop and not term.startswith(('#','@'))]  # terms with stop words removed
        termsHash = [term for term in tokenList if term.startswith('#')]
        termsMention = [term for term in tokenList if term.startswith('@')]

        countAll.update(termsAll)
        countTerms.update(termsTerms)
        countHash.update(termsHash)
        countMention.update(termsMention)

        
print("Top 5 terms (stopwords removed)")
print(countAll.most_common(5))
print
print("Top 5 terms with stopwords, mentions, and hashtags removed")
print(countTerms.most_common(5))
print
print("Top 5 Hashtags")
print(countHash.most_common(5))
print
print("Top 5 Mentions")
print(countMention.most_common(5))
