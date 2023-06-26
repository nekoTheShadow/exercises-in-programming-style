import re, sys

def read_file(path_to_file):
    with open(path_to_file) as f:
        return [(i//45+1, line) for i, line in enumerate(f)]

def filter_chars_and_normalize(tpls):
    return [(pageno, re.sub('[\W_]+', ' ', line).lower().split()) for pageno, line in tpls]

def flatten(tpls):
    word_list = []
    for pageno, words in tpls:
        for word in words:
            word_list.append((pageno, word))
    return word_list

def print_all(word_list):
    with open('../target_words.txt') as f:
        targets = f.read().split(',')
    targets.sort()
    
    for target in sorted(targets):
        for i in range(len(word_list)):
            pageno, word = word_list[i]
            if word == target:
                print(word_list[i-2][1], word_list[i-1][1], word_list[i][1], word_list[i+1][1], word_list[i+2][1], '-', pageno)

print_all(flatten(filter_chars_and_normalize(read_file(sys.argv[1]))))