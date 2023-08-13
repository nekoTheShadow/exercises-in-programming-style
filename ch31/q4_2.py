import re
import functools
import sys

def read_words(filename):
    words = []
    with open(filename) as f:
        for i, line in enumerate(f):
            for word in re.findall(r'\w+', line.lower()):
                words.append((word, i//45+1))
                
    return words

def grep(target):
    words = read_words(sys.argv[1])
    results = []
    for i, (word, page) in enumerate(words):
        if word == target:
            result = ' '.join(words[i+j][0] for j in range(-2, 3))
            results.append((target, page, result + f' - {page}'))
    return results

def merge(results1, results2):
    return results1 + results2

with open('../target_words.txt') as f:
    results = functools.reduce(merge, map(grep, f.read().split(',')))

for _, _, result in sorted(results):
    print(result)