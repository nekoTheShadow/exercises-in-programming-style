import sys, re, operator, string

class TFQuarantine:
    def __init__(self, func):
        self._funcs = [func]

    def bind(self, func):
        self._funcs.append(func)
        return self

    def execute(self):
        def guard_callable(v):
            return v() if callable(v) else v
        
        value = lambda : None
        for func in self._funcs:
            value = func(guard_callable(value))
        print(guard_callable(value))


def get_input(arg):
    def _f():
        return sys.argv[1]
    return _f


def extract_words(path_to_file):
    def _f():
        pattern = re.compile('[^a-z]+')
        word_list = []
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                word_list.extend((word, i//45+1) for word in pattern.sub(' ', line).lower().split())
        return word_list
    return _f

def remove_stop_words(word_list):
    def _f():
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
        stop_words.extend(list(string.ascii_lowercase))
        return [(w, page) for w, page in word_list if not w in stop_words]
    return _f


def grouping(word_list):
    word_freqs = {}
    for w, page in word_list:
        if not w in word_freqs:
            word_freqs[w] = []
        if not page in word_freqs[w]:
            word_freqs[w].append(page)
    return word_freqs


def sort(word_freq):
    return sorted(word_freq.items())


def text(word_freqs):
    return '\n'.join(w + ' - ' + ', '.join(map(str, pages)) for w, pages in word_freqs)

TFQuarantine(get_input)\
.bind(extract_words)\
.bind(remove_stop_words)\
.bind(grouping)\
.bind(sort)\
.bind(text)\
.execute()
