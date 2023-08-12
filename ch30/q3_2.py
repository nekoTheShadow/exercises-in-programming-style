import queue
import re
import sys
import threading


target_q = queue.Queue()
result_q = queue.Queue()
words = []
with open(sys.argv[1]) as f:
    for i, line in enumerate(f):
        for word in re.findall('\w+', line.lower()):
            words.append((word, i//45+1))

def grep():
    target = target_q.get()
    for i, (word, page) in enumerate(words):
        if word == target:
            result = ' '.join(words[i+j][0] for j in range(-2, 3))
            result_q.put((target, page, result))


n = 0
with open('../target_words.txt') as f:
    for target in f.read().split(','):
        n += 1
        target_q.put(target)

threads = [threading.Thread(target=grep) for _ in range(n)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

results = []
while not result_q.empty():
    results.append(result_q.get())
for target, page, result in sorted(results):
    print(result, '-', page)
