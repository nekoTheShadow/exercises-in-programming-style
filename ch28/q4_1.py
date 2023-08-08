import collections
import re
import sys


def all_lines(filename):
    with open(filename) as f:
        for i, line in enumerate(f):
            yield i, line


def all_words(filename):
    pattern = re.compile('[a-z]+')
    for lineno, line in all_lines(filename):
        for word in pattern.findall(line.lower()):
            yield lineno//45+1, word


pages = collections.defaultdict(list)
for pageno, word in all_words(sys.argv[1]):
    if pageno not in pages[word]:
        pages[word].append(pageno)
for word, page in sorted(pages.items()):
    if len(page) < 100:
        print(word, '-', ', '.join(map(str, page)))