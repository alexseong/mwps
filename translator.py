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
import preprocessing
import pretraining 

if not len(sys.argv) > 1:
    raise Exception("Please use a config file.")

with open(abspath(sys.argv[1]), 'r', encoding='utf-8-sig') as yaml_file:
    settings = yaml.safe_load(yaml_file)

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

if len(sys.argv) > 2:
    LOSS_THRESHHOLD = float(sys.argv[2])
else:
    LOSS_THRESHHOLD = 0

# If fine-tuning set this to a str containing the model name
CKPT_MODEL = settings["model"]

# text.SubwordTextEncoder / text.TextEncoder
#ENCODE_METHOD = tfds.deprecated.text.SubwordTextEncoder
MIRRORED_STRATEGY = tf.distribute.MirroredStrategy(
    cross_device_ops=tf.distribute.ReductionToOneDevice()
)

# Hyperparameters
NUM_LAYERS = settings["layers"]
D_MODEL = settings["d_model"]
DFF = settings["dff"]
NUM_HEADS = settings["heads"]
DROPOUT = settings["dropout"]

# Training settings
EPOCHS = settings["epochs"]
BATCH_SIZE = settings["batch"]
GLOBAL_BATCH_SIZE = BATCH_SIZE * MIRRORED_STRATEGY.num_replicas_in_sync

# Adam optimizer params
BETA_1 = settings["beta_1"]
BETA_2 = settings["beta_2"]
EPSILON = 1e-9

LIVE_MODE = EPOCHS == 0 and USER_INPUT

# Random seed for shuffling the data
SEED = settings["seed"]
# Set the seed for random
seed(SEED)

tf.compat.v1.set_random_seed(SEED)

if isinstance(CKPT_MODEL, str):
    # If a model name is given train from that model
    CONTINUE_FROM_CKPT = True
    MODEL_NAME = CKPT_MODEL
    CHECKPOINT_PATH = abspath(f"models/trained/{CKPT_MODEL}/")
else:
    CONTINUE_FROM_CKPT = False
    MODEL_NAME = f"mwp_{NUM_LAYERS}_{NUM_HEADS}_{D_MODEL}_{DFF}_{int(time())}"

TRAINED_PATH = abspath(f"models/trained/")
MODEL_PATH = abspath(f"models/trained/{MODEL_NAME}/")

TEXT_TOKENIZER_PATH = abspath(f"models/trained/{MODEL_NAME}/tokenizers/{MODEL_NAME}_t.p")
EQUATION_TOKENIZER_PATH = abspath(f"models/trained/{MODEL_NAME}/tokenizers/{MODEL_NAME}_e.p")

ARE_TOKENIZERS_PRESENT = exists(TEXT_TOKENIZER_PATH) or exists(EQUATION_TOKENIZER_PATH)

tf.compat.v1.enable_eager_execution()

if __name__ == "__main__":
    if LIVE_MODE:
        print("Starting the MWP Transformer live testing.")
    else:
        print("Starting the MWP Transformer training")

    if not exists(TRAINED_PATH):
        makedirs(TRAINED_PATH)

    num_examples = 0

    if not isinstance(PRETRAIN, bool) and not LIVE_MODE:
        print("Getting pre-training data...")

        if PRETRAIN == "imdb":
            # Pretrain on unlabelled english text for more in-depth understanding of english
            english_dataset, num_examples = pretraining.imdb(remove_stop_words=REMOVE_STOP_WORDS, as_lemmas=LEMMAS)


