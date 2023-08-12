import sys, re, operator, string, functools

def partition(data_str, nlines):
    lines = data_str.split('\n')
    for i in range(0, len(lines), nlines):
        yield '\n'.join(lines[i:i+nlines])

def split_words(data_str):
    def _scan(str_data):
        pattern = re.compile('[\W_]+')
        return pattern.sub(' ', str_data).lower().split()

    def _remove_stop_words(word_list):
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
        stop_words.extend(list(string.ascii_lowercase))
        return [w for w in word_list if not w in stop_words]

    words = _remove_stop_words(_scan(data_str))
    result = {}
    for word in words:
        if word not in result:
            result[word] = 0
        result[word] += 1
    return result.items()

def count_words(pairs_list_1, pairs_list_2):
    mapping = {}
    for pl in [pairs_list_1, pairs_list_2]:
        for p in pl:
            if p[0] in mapping:
                mapping[p[0]] += p[1]
            else:
                mapping[p[0]] = p[1]
    return mapping.items()

def read_file(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    return data

def sort(word_freq):
    return sorted(word_freq, key=operator.itemgetter(1), reverse=True)

splits = map(split_words, partition(read_file(sys.argv[1]), 200))
word_freqs = sort(functools.reduce(count_words, splits))

for (w, c) in word_freqs[0:25]:
    print(w, '-', c)