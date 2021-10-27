from __future__ import absolute_import, unicode_literals, division, print_function
import tensorflow as tf
import tensorflow_datasets as tfds

from transformer.network import create_masks, loss_function
from time import time
from random import seed, shuffle
from os import makedirs, remove, environ
from os.path import abspath, exists, join
from re import match
import logging
import yaml
import sys
import utils


if not len(sys.argv) > 1:
    raise Exception("Please use a config file.")

with open(abspath(sys.argv[1]), 'r', encoding='utf-8-sig') as yaml_file:
    settings = yaml.load(yaml_file, Loader=yaml.FullLoader)
    settings = yaml.load(yaml_file, Loader=yaml.FullLoader)

DATASET = settings["dataset"]
DUPLICATION = settings["duplication"]
TEST_SET = settings["test"]
PRETRAIN = settings["pretrain"]
TRAIN_WITH_TAGS = True
REORDER_SENTENCES = settings["reorder"]
REMOVE_NUMBERS_NOT_IN_EQ = settings["tagging"]
REMOVE_STOP_WORDS = settings["remove_stopwords"]
PART_OF_SPEECH_TAGGING = settings["pos"]
PART_OF_SPEECH_TAGGING_W_WORDS = settings["pos_words"]
LEMMAS = settings["as_lemmas"]
DATA_PATH = abspath("data/" + DATASET)
USER_INPUT = settings["input"]
EQUALS_SIGN = False
SAVE = settings["save"]

utils.MAX_LENGTH = 60


LIVE_MODE = EPOCHS == 0 and USER_INPUT

if __name__ == "__main__":
    if LIVE_MODE:
        print("Starting the MWP Transformer live testing.")
    else:
        print("Starting the MWP Transformer training")

