import sys, re, itertools, operator
import numpy as np

with open('../stop_words.txt') as f:
    stop_words = np.array(f.read().split(','))

with open(sys.argv[1]) as f:
    words = np.array([word for i, line in enumerate(f) for word in re.findall('[a-zA-Z]+', line)])
with open(sys.argv[1]) as f:
    pages = np.array([i//45+1 for i, line in enumerate(f) for word in re.findall('[a-zA-Z]+', line)])

words = np.char.lower(words)
stop_index = ~np.isin(words, stop_words)
words = words[stop_index]
pages = pages[stop_index]
results = [
    (word, sorted(set(map(operator.itemgetter(1), tpls))))
    for word, tpls 
    in itertools.groupby(sorted(zip(words, pages)), operator.itemgetter(0))
]
for w, p in results:
    if len(p) < 100:
        print(w, '-', ', '.join(map(str, p)))