from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import download, data, pos_tag
from collections import Counter
from itertools import permutations
from os.path import abspath, exists
from re import match, sub
import os

NLTK_DIR = abspath("data/datasets/nltk/")
data.path.append(NLTK_DIR)

if not os.path.exists(NLTK_DIR):
    os.makedirs(NLTK_DIR)

# Download NLTK data if not already existing
if not exists(abspath("data/datasets/nltk/corpora/stopwords/english")):
    download("stopwords", download_dir=NLTK_DIR)

if not exists(abspath("data/datasets/nltk/corpora/wordnet")):
    download("wordnet", download_dir=NLTK_DIR)

if not exists(abspath("data/datasets/nltk/tokenizers/punkt")):
    download("punkt", download_dir=NLTK_DIR)

if not exists(abspath("data/datasets/nltk/taggers/averaged_perceptron_tagger")):
    download("averaged_perceptron_tagger", download_dir=NLTK_DIR)

STOPWORDS = set(stopwords.words('english'))
NOUNS = { x.name().split('.', 1)[0] for x in wordnet.all_synsets('n') }
WNL = WordNetLemmatizer()

def remove_stopwords(lst):
    '''
    Remove any stop words in the question.
    '''
    output_array = []
    for sentence in lst:
        temp_list = []
        for word in sentence.split(' '):
            if word.lower() not in STOPWORDS:
                temp_list.append(word)

        output_array.append(' '.join(temp_list))
    return output_array

def lemmatize(lst):
    '''
    Convert plurals to lemmas in questions for consistent language.
    '''
    output_array = []
    for sentence in lst:
        temp_list = []
        for word in sentence.split(' '):
            temp_list.append(WNL.lemmatize(word))
        
        output_array.append(' '.join(temp_list))
    return output_array
