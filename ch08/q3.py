import operator
import re
import sys

RECURSION_LIMIT=5000
sys.setrecursionlimit(RECURSION_LIMIT+100)

def count(word_list, stopwords, wordfreqs):
    if word_list == []:
        return word_freqs
    else:
        word = word_list[0]
        if word not in stopwords:
            if word in wordfreqs:
                wordfreqs[word]+=1
            else:
                wordfreqs[word]=1
        return count(word_list[1:], stopwords, wordfreqs)

def wf_print(wordfreqs):
    if wordfreqs==[]:
        return
    else:
        w, c = wordfreqs[0]
        print(w, '-', c)
        wf_print(wordfreqs[1:])

stop_words = set(open('../stop_words.txt').read().split(','))
words = re.findall(r'[a-z]{2,}', open(sys.argv[1]).read().lower())
word_freqs = {}
for i in range(0, len(words), RECURSION_LIMIT):
    word_freqs = count(words[i:i+RECURSION_LIMIT], stop_words, word_freqs)
wf_print(sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)[:25])


