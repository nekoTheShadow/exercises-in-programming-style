import re, sys, io

class TFTheOne:
    def __init__(self, v):
        self._value = v

    def bind(self, func):
        self._value = func(self._value)
        return self

    def printme(self):
        print(self._value, end='')


def read_file(path_to_file):
    with open(path_to_file) as f:
        lines = [line for line in f]
    return lines


def scan(lines):
    words = []
    for lineno, line in enumerate(lines):
        for word in re.findall('\w+', line.lower()):
            words.append((lineno, word))
    return words


def filter(words):
    with open('../target_words.txt') as f:
        targets = f.read().split(',')
    targets.sort()
    texts = []
    for target in targets:
        for i, (lineno, word) in enumerate(words):
            if word == target:
                texts.append([
                    lineno//45+1,
                    words[i-2][1],
                    words[i-1][1],
                    words[i][1],
                    words[i+1][1],
                    words[i+2][1],
                ])
    return texts

def to_text(texts):
    ss = io.StringIO()
    for text in texts:
        print(*text[1:], '-', text[0], file=ss)
    return ss.getvalue()


TFTheOne(sys.argv[1]) \
.bind(read_file) \
.bind(scan) \
.bind(filter) \
.bind(to_text) \
.printme()