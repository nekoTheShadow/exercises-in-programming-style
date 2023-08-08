
import operator
import re
import string
import sys


def lines(filename):
    for line in open(filename):
        yield line


def all_words(filename):
    for line in lines(filename):
        for word in re.findall('[0-9a-z]+', line.lower()):
            yield word


def non_stop_words(filename):
    stopwords = set(open('../stop_words.txt').read().strip('\n').split(',') + list(string.ascii_lowercase))
    for w in all_words(filename):
        if not w in stopwords:
            yield w


def count_and_sort(filename):
    freqs, i = {}, 1
    for w in non_stop_words(filename):
        freqs[w] = 1 if w not in freqs else freqs[w]+1
        if i % 5000 == 0:
            yield sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
        i = i+1
    yield sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)

for word_freqs in count_and_sort(sys.argv[1]):
    print('-----------------------------')
    for (w, c) in word_freqs[0:25]:
        print(w, '-', c)