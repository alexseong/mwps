from tensorflow import logical_and, size
from re import sub
from pickle import load, dump

# Data constraints
MAX_LENGTH = 60

def load_data_from_binary(absolute_path):
    # Get the lines in a binary as list
    with open(absolute_path, "rb") as fh:
        file_data = load(fh)

    return file_data

def to_binary(absolute_path, what):
    # Save to a binary
    with open(absolute_path, 'wb') as fh:
        dump(what, fh)
