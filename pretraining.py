from preprocessing import remove_stopwords, lemmatize
from utils import load_data_from_binary, to_binary
from random import shuffle, randint
from os.path import abspath, exists
from tensorflow import constant, data as tfdata
