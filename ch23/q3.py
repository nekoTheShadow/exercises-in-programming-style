import sys, re, operator, string, traceback

class TFTheOne:
    def __init__(self, v):
        self._value = v
        self._e = None

    def bind(self, func):
        if self._e is None:
            try:
                self._value = func(self._value)
            except Exception as e:
                self._e = e
        return self

    def printme(self):
        if self._e is None:
            print(self._value, end='')
        else:
            raise self._e


def extract_words(path_to_file):
    assert(type(path_to_file) is str), 'I need a string! I quit!' 
    assert(path_to_file), 'I need a non-empty string! I quit!' 

    with open(path_to_file) as f:
        data = f.read()
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', data).lower().split()
    return word_list

def remove_stop_words(word_list):
    assert(type(word_list) is list), 'I need a list! I quit!'

    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    assert(type(word_list) is list), 'I need a list! I quit!'
    assert(word_list != []), 'I need a non-empty list! I quit!'

    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(word_freqs):
    assert(type(word_freqs) is dict), 'I need a dictionary! I quit!'
    assert(word_freqs != {}), 'I need a non-empty dictionary! I quit!'

    return sorted(word_freqs.items(), key=operator.itemgetter(1), reverse=True)

def top25_freqs(word_freqs):
    return ''.join(f'{tf[0]} - {tf[1]}\n' for tf in word_freqs[0:25])


TFTheOne(sys.argv[1]) \
.bind(extract_words) \
.bind(remove_stop_words) \
.bind(frequencies) \
.bind(sort) \
.bind(top25_freqs) \
.printme()

# $ python3 q3.py ../nothing.txt
# Traceback (most recent call last):
#   File "q3.py", line 63, in <module>
#     TFTheOne(sys.argv[1]) \
#   File "q3.py", line 20, in printme
#     raise self._e
#   File "q3.py", line 11, in bind
#     self._value = func(self._value)
#   File "q3.py", line 27, in extract_words
#     with open(path_to_file) as f:
# FileNotFoundError: [Errno 2] No such file or directory: '../nothing.txt'