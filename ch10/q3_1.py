import sys, re, collections, io

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
    matrix = []
    for line in lines:
        matrix.append(re.findall('[a-z]{2,}', line.lower()))
    return matrix


def remove_stop_words(matrix):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    return [[word for word in words if not word in stop_words] for words in matrix]


def groupby(matrix):
    groups = collections.defaultdict(list)
    for lineno, words in enumerate(matrix):
        for word in words:
            if not lineno//45+1 in groups[word]:
                groups[word].append(lineno//45+1)
    return groups


def to_text(groups):
    ss = io.StringIO()
    for word in sorted(groups):
        print(word, '-', ', '.join(map(str, groups[word])), file=ss)
    return ss.getvalue()



TFTheOne(sys.argv[1]) \
.bind(read_file) \
.bind(scan) \
.bind(remove_stop_words) \
.bind(groupby) \
.bind(to_text) \
.printme()