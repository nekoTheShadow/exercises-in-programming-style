import re, sys, operator, queue, threading

words_space = queue.Queue()
stopwords = set(open('../stop_words.txt').read().split(','))
freqs = {}

def process_words():
    word_freqs = {}
    words = words_space.get()
    for word in words:
        if not word in stopwords:
            if word in word_freqs:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1
    freqs.update(word_freqs)


words_list = [[] for _ in range(5)]
for word in re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower()):
    words_list[(ord(word[0])-ord('a'))%5].append(word)
for words in words_list:
    words_space.put(words)

workers = []
for i in range(5):
    workers.append(threading.Thread(target = process_words))
[t.start() for t in workers]
[t.join() for t in workers]

for (w, c) in sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)[:25]:
    print(w, '-', c)