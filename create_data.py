from __future__ import absolute_import
import os, re
import sys, random
import yaml, time
import json
import pickle
from word2number import w2n
from EquationConverter import EquationConverter

data_root_dir = os.path.join(os.getcwd(), '../MWP-Automatic-Solver/data')
data_dir = os.path.join(data_root_dir, 'datasets')
PROBLEM_LIST = []
DIR_PATH = os.path.abspath(os.getcwd())

USE_GENERATED = False
TEST_SPLIT = 0.05
WORDS_FOR_OPERATORS = False

# Composite list of MWPs
PROBLEM_LIST = []

# The same list with all equations converted from infix to cleaned infix
CLEAN_INFIX_CONVERTED_PROBLEM_LIST = []

# The same list with all equations converted from infix to Polish notation
POLISH_CONVERTED_PROBLEM_LIST = []

# The same list with all equations converted from infix to Reverse Polish notation
REVERSE_POLISH_CONVERTED_PROBLEM_LIST = []

# The generated data (not used in testing)
GENERATED = []

# Dataset specific
AI2 = []
ILLINOIS = []
COMMONCORE = []
MAWPS = []

KEEP_INFIX_PARENTHESIS = True
MAKE_IND_SETS = True

# Large test sets
PREFIX_TEST = []
POSTFIX_TEST = []
INFIX_TEST = []

settings = {
    'dataset': 'train_all_postfix.p',
    'duplication': False,
    'test': 'postfix',
    'model': False,
    'layers': 2,
    'heads': 8,
    'd_model': 256,
    'dff': 1024,
    'lr': 'scheduled',
    'dropout': 0.1,
    'epochs': 300,
    'batch': 128,
    'pretrain': False,
    'beta_1': 0.95,
    'beta_2': 0.99,
    'pos': False,
    'pos_words': False,
    'remove_stopwords': False,
    'as_lemmas': False,
    'reorder': False,
    'tagging': 'lst',
    'input': False,
    'seed': 420365,
    'save': True
}

SEED = settings['seed']
random.seed(SEED)

def one_sentence_clean(text):
    # Clean up the data and separate everything by spaces
    text = re.sub(r"(?<!Mr|Mr|Dr|Ms)(?<!Mrs)(?<![0-9])(\s+)?\.(\s+)?", " . ",
                  text, flags=re.IGNORECASE)
    text = re.sub(r"(\s+)?\?(\s+)?", " ? ", text)
    text = re.sub(r",", "", text)
    text = re.sub(r"^\s+", "", text)
    text = text.replace('\n', ' ')
    text = text.replace("'", " '")
    text = text.replace('%', ' percent')
    text = text.replace('$', ' $ ')
    text = re.sub(r"\.\s+", " . ", text)
    text = re.sub(r"\s+", ' ', text)
    
    sent = []
    for word in text.split(' '):
        try:
            sent.append(str(w2n.word_to_num(word)))
        except:
            sent.append(word)
    
    return ' '.join(sent)        

def to_lower_case(text):
    try:
        return text.lower()
    except:
        return text


def transform_AI2():
    print("\nWorking on AI2 data...")
    problem_list = []

    with open(os.path.join(data_dir, 'AI2/questions.txt'), "r") as fh:
        content = fh.readlines()
        
    for i in range(len(content)):
        if i % 3 ==0 or i == 0:
            question_text = one_sentence_clean(content[i].strip())            
            eq = content[i + 2].strip()
            
            problem = [("question", to_lower_case(question_text)),
                       ("equation", to_lower_case(eq)),
                       ("answer", content[i+1].strip())
                      ]
            
            if problem != []:
                problem_list.append(problem)
                AI2.append(problem)
        
    total_problems = int(len(content) / 3)    
    print(f"-> Retrived {len(problem_list)} / {total_problems} problems.")
    print("...done.\n")
            
    return AI2

def transform_all_datasets():
    total_datasets = []
    # Iteratively rework all the data
    total_datasets.append(transform_AI2())
#     total_datasets.append(transform_CommonCore())
#     total_datasets.append(transform_Illinois())
#     total_datasets.append(transform_MaWPS())
#     if USE_GENERATED:
#         total_datasets.append(transform_custom())

    return total_datasets

def convert_to(problem_list, tag):
    output = []
    
    for problem in problem_list:
        problem_dict = dict(problem)
        ol = []
        discard = False
        
        for k, v in problem_dict.items():
            if k == 'equation':
                convert = EquationConverter()
                convert.eqset(v)


if __name__ == "__main__":
    print("Transforming all original datasets...")
    print(f"Splitting {(1 - TEST_SPLIT) * 100}% for training.")
    print("NOTE: Find resulting data binaries in the data folder.")

    total_filtered_datasets = transform_all_datasets()

    # Split
    AI2_TEST = AI2[:int(len(AI2) * TEST_SPLIT)]
    AI2 = AI2[int(len(AI2) * TEST_SPLIT):]