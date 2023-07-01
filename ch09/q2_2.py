def read_file(path_to_file, func):
    with open(path_to_file) as f:
        lines = [line for line in f]
    func(lines, filter)


def scan(lines, func):
    import re
    words = []
    for lineno in range(len(lines)):
        for word in re.findall('\w+', lines[lineno].lower()):
            words.append((lineno, word))
    func(words, print_text)


def filter(words, func):
    with open('../target_words.txt') as f:
        targets = f.read().split(',')
    texts = []
    for target in sorted(targets):
        for i in range(len(words)):
            if words[i][1] == target:
                texts.append((words[i][0]//45+1, words[i-2][1], words[i-1][1], words[i][1], words[i+1][1], words[i+2][1]))
    func(texts, no_op)


def print_text(texts, func):
    for text in texts:
        print(*text[1:], '-', text[0])
    func(None)


def no_op(func):
    return



# read_file
# scan
# filter
# print_text

import sys
read_file(sys.argv[1], scan)