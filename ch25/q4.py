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


def read_file(path_to_file):
    def _f():
        with open(path_to_file) as f:
            input_data = f.read()
        with open('../stop_words.txt') as f:
            stop_data = f.read()
        return input_data, stop_data
    return _f()

def extract_words(datum):
    input_data, stop_data = datum
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', input_data).lower().split()
    stop_words = stop_data.split(',')
    return word_list, stop_words


def remove_stop_words(datum):
    word_list, stop_words = datum
    return [w for w in word_list if not w in stop_words]


def frequencies(word_list):
    word_freqs = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs


def sort(word_freq):
    return sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)


def top25_freqs(word_freqs):
    top25 = ""
    for tf in word_freqs[0:25]:
        top25 += f'{tf[0]} - {tf[1]}\n'
    return top25

TFQuarantine(get_input)\
.bind(read_file)\
.bind(extract_words)\
.bind(remove_stop_words)\
.bind(frequencies)\
.bind(sort)\
.bind(top25_freqs)\
.execute()
