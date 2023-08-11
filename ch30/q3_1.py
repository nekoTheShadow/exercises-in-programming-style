import collections
import queue
import re
import sys
import threading


word_q = queue.Queue()
dict_q = queue.Queue()
stopwords = set(open('../stop_words.txt').read().split(','))

def tally():
    groups = collections.defaultdict(set)
    while True:
        try:
            word, page = word_q.get(timeout=1)
        except queue.Empty:
            break
        groups[word].add(page)
    dict_q.put(groups)


with open(sys.argv[1]) as f:
    for i, line in enumerate(f):
        for word in re.findall('[a-z]{2,}', line.lower()):
            word_q.put((word, i//45+1))

threads = [threading.Thread(target=tally) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

groups = collections.defaultdict(set)
while not dict_q.empty():
    for word, pages in dict_q.get().items():
        groups[word] |= pages

for word, pages in sorted(groups.items()):
    if len(pages) < 100:
        print(word, '-', ', '.join(map(str, pages)))