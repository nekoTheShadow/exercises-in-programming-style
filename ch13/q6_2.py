import re
import sys

def extract_words(data_storage_obj, path_to_file):
    with open(path_to_file) as f:
        for i, line in enumerate(f):
            for word in re.finditer('\w+', line.lower()):
                data_storage_obj["_words"].append((i//45+1, word.group()))

def find_target(data_storage_obj, target):
    results = []
    for i, (page, word) in enumerate(data_storage_obj['_words']):
        if word == target:
            results.append((page, *(data_storage_obj['_words'][i+j][1] for j in range(-2, 3))))
    return results

def read_target_words(target_words_obj):
    with open('../target_words.txt') as f:
        target_words_obj['_words'] = f.read().split(',')
    target_words_obj['_words'].sort()

data_storage_obj = {
    '_words' : [],
    'init' : lambda path_to_file : extract_words(data_storage_obj, path_to_file),
    'find' : lambda target : find_target(data_storage_obj, target)
}

target_words_obj = {
    '_words' : [],
    'init' : lambda : read_target_words(target_words_obj),
    'words' : lambda : target_words_obj['_words']
}

data_storage_obj['init'](sys.argv[1])
target_words_obj['init']()
for target in target_words_obj['words']():
    for result in data_storage_obj["find"](target):
        print(*result[1:], '-', result[0])
