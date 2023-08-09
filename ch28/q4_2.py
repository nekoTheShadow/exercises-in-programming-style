import re
import sys


def all_lines(filename):
    with open(filename) as f:
        for i, line in enumerate(f):
            yield i, line


def all_words(filename):
    pattern = re.compile('\w+')
    for lineno, line in all_lines(filename):
        for word in pattern.findall(line.lower()):
            yield lineno//45+1, word


def target_words():
    with open('../target_words.txt') as f:
        target_words = f.read().split(',')
        for target_word in sorted(target_words):
            yield target_word


def search(filename):
    for target_word in target_words():
        v1, v2, v3, v4, v5 = (-1, ''), (-1, ''), (-1, ''), (-1, ''), (-1, '')
        for page, word in all_words(filename):
            v1, v2, v3, v4, v5 = v2, v3, v4, v5, (page, word)
            if v3[1] == target_word:
                yield f'{v1[1]} {v2[1]} {v3[1]} {v4[1]} {v5[1]} - {page}'


for result in search(sys.argv[1]):
    print(result)