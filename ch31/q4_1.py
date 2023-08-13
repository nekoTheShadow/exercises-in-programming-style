import functools
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

def grouping(words):
    groups = collections.defaultdict(set)
    for word, page in words:
        groups[word].add(page)
    return groups

def merge(g1, g2):
    groups = collections.defaultdict(set)
    for g in (g1, g2):
        for word, pages in g.items():
            groups[word].update(pages)
    return groups



groups = functools.reduce(merge, map(grouping, read_words(sys.argv[1], 1000)))
for word, pages in sorted(groups.items()):
    if len(pages) < 100:
        print(word, '-', ', '.join(map(str, sorted(pages))))