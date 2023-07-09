import operator
import re
import sys
import string

def extract_words(data_storage_obj, path_to_file):
    with open(path_to_file) as f:
        for i, line in enumerate(f):
            for word in re.finditer('[a-z]+', line.lower()):
                data_storage_obj["_words"].append((i//45+1, word.group()))

def load_stop_words(stop_words_obj):
    with open('../stop_words.txt') as f:
        stop_words_obj['_stop_words'] = f.read().split(',')
    stop_words_obj['_stop_words'].extend(list(string.ascii_lowercase))

def add_word_freqs(word_freqs_obj, word, page):
    if word not in word_freqs_obj["_freqs"]:
        word_freqs_obj["_freqs"][word] = []
    if page not in word_freqs_obj["_freqs"][word]:
        word_freqs_obj["_freqs"][word].append(page)


data_storage_obj = {
    '_words' : [],
    'init' : lambda path_to_file : extract_words(data_storage_obj, path_to_file),
    'words' : lambda : data_storage_obj['_words'],
}

stop_words_obj = {
    '_stop_words' : [],
    'init' : lambda : load_stop_words(stop_words_obj),
    'is_stop_word' : lambda word : word in stop_words_obj["_stop_words"]
}

word_freqs_obj = {
    '_freqs' : {},
    'add' : lambda word, page : add_word_freqs(word_freqs_obj, word, page),
    'format' : lambda : '\n'.join(word + ' - ' + ', '.join(map(str, pages)) for word, pages in sorted(word_freqs_obj['_freqs'].items(), key=operator.itemgetter(0)) if len(pages)<100)
}

data_storage_obj['init'](sys.argv[1])
stop_words_obj['init']()

for page, word in data_storage_obj['words']():
    if not stop_words_obj['is_stop_word'](word):
        word_freqs_obj['add'](word, page)

print(word_freqs_obj["format"]())