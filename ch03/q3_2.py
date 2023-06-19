import numpy as np
import re, sys

with open('../target_words.txt') as f:
    target_words = np.array(sorted(f.read().split(',')))
with open(sys.argv[1]) as f:
    words = np.array([word for i, line in enumerate(f) for word in re.findall('\w+', line)])
with open(sys.argv[1]) as f:
    pages = np.array([i//45+1 for i, line in enumerate(f) for word in re.findall('\w+', line)])

words = np.char.lower(words)
words1 = np.array(['', '', *words[:-2]])
words2 = np.array(['', *words[:-1]])
words3 = np.array([*words])
words4 = np.array([*words[1:], ''])
words5 = np.array([*words[2:], '', ''])

x = np.where(np.isin(words3, target_words))
for w1, w2, w3, w4, w5, p in sorted(zip(words1[x], words2[x], words3[x], words4[x], words5[x], pages[x]), key=lambda r : (r[2], r[5])):
    print(w1, w2, w3, w4, w5, '-', p)


