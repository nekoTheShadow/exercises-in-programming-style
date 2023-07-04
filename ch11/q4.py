import operator
import re
import string
import sys

def new_data_storage_manager(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    pattern = re.compile("[\W_]+")
    return pattern.sub(" ", data).lower()

def words(data_storage_manager):
    return data_storage_manager.split()

def new_stop_word_manager():
    with open("../stop_words.txt") as f:
        stop_words = f.read().split(",")
    stop_words.extend(list(string.ascii_lowercase))
    return stop_words

def is_stop_word(stop_word_manager, word):
    return word in stop_word_manager

def new_word_frequency_manager():
    return {}

def increment_count(word_frequency_manager, word):
    if word in word_frequency_manager:
        word_frequency_manager[word] += 1
    else:
        word_frequency_manager[word] = 1

def sort(word_frequency_manager):
    return sorted(word_frequency_manager.items(), key=operator.itemgetter(1), reverse=True)

def run(path_to_file):
    data_storage_manager = new_data_storage_manager(path_to_file)
    stop_word_manager = new_stop_word_manager()
    word_frequency_manager = new_word_frequency_manager()
    for w in words(data_storage_manager):
        if not is_stop_word(stop_word_manager, w):
            increment_count(word_frequency_manager, w)

    word_freqs = sort(word_frequency_manager)
    for (w, c) in word_freqs[0:25]:
        print(w, "-", c)

run(sys.argv[1])