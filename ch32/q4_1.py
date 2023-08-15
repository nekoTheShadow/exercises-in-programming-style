import re
import sys
import collections

def read_words(filename, n):
    with open('../stop_words.txt') as f:
        stop_words = set(f.read().split(','))

    words = []
    with open(filename) as f:
        for i, line in enumerate(f):
            for word in re.findall(r'[a-z]{2,}', line.lower()):
                if word not in stop_words:
                    words.append((word, i//45+1))
                if len(words)==n:
                    yield words
                    words.clear()
    yield words

def regroup(words_list):
    mapping = collections.defaultdict(list)
    for words in words_list:
        for word, page in words:
            mapping[word].append((word, page))
    return mapping

def groupby(pairs):
    word, words = pairs
    pages = []
    for _, page in words:
        if page not in pages:
            pages.append(page)
    return (word, pages)


words_list = read_words(sys.argv[1], 1000)
mapping = regroup(words_list)
grouping = map(groupby, mapping.items())
for word, pages in sorted(grouping):
    if len(pages) < 100:
        print(word, '-', ', '.join(map(str, pages)))
