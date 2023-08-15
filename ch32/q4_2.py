import re
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
            results.append((page, *(words[i+j][0] for j in range(-2, 3))))
    return results

def regrop(results_list):
    mapping = {}
    for results in results_list:
        for page, w1, w2, w3, w4, w5 in results:
            if w3 not in mapping:
                mapping[w3] = []
            mapping[w3].append((page, w1, w2, w3, w4, w5))
    return mapping

def to_text(pair):
    word, results = pair
    texts = []
    for page, w1, w2, w3, w4, w5 in results:
        texts.append(f'{w1} {w2} {w3} {w4} {w5} - {page}')
    return (word, texts)

def merge(results1, results2):
    return results1 + results2

with open('../target_words.txt') as f:
    results_list = map(grep, f.read().split(','))
    mapping = regrop(results_list)
    texts = map(to_text, mapping.items())
    for _, results in sorted(texts):
        for result in results:
            print(result)