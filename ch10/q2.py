import sys, re, operator, string

def wrap(v):
    return lambda : v


def bind(v, func):
    return func(v())


def printme(v):
    print(v)


def read_file(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    return data


def filter_chars(str_data):
    pattern = re.compile('[\W_]+')
    return pattern.sub(' ', str_data)


def normalize(str_data):
    return str_data.lower()


def scan(str_data):
    return str_data.split()


def remove_stop_words(word_list):
    with open('../stop_words.txt') as f:
        stop_words = f.read().strip('\n').split(',')
    stop_words.extend(list(string.ascii_lowercase))
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
        top25 += str(tf[0]) + ' - ' + str(tf[1]) + '\n'
    return top25


v = sys.argv[1]
v = bind(wrap(v), read_file)
v = bind(wrap(v), filter_chars)
v = bind(wrap(v), normalize)
v = bind(wrap(v), scan)
v = bind(wrap(v), remove_stop_words)
v = bind(wrap(v), frequencies)
v = bind(wrap(v), sort)
v = bind(wrap(v), top25_freqs)
printme(v)