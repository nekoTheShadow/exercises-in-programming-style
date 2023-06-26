import re, sys

def read_file(path_to_file):
    with open(path_to_file) as f:
        return [(i//45+1, line) for i, line in enumerate(f)]

def filter_chars_and_normalize(tpls):
    return [(pageno, re.sub('[^a-zA-Z]+', ' ', line).lower().split()) for pageno, line in tpls]

def tally(tpls):
    d = {}
    for pageno, words in tpls:
        for word in words:
            if word not in d:
                d[word] = []
            if pageno not in d[word]:
                d[word].append(pageno)
    return d

def remove_stop_words(pagenos):
    with open('stop_words.txt') as f:
        stop_words = f.read().split(',')
    return {word : pagenos[word] for word in pagenos if word not in stop_words}

def print_all(pagenos):
    for word in sorted(pagenos):
        if len(pagenos[word]) < 100:
            print(word, '-', ', '.join(map(str, pagenos[word])))


print_all(tally(filter_chars_and_normalize(read_file(sys.argv[1]))))