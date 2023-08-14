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

    result = []
    words = _remove_stop_words(_scan(data_str))
    for w in words:
        result.append((w, 1))
    return result

def regroup(pairs_list):
    mapping = {}
    for pairs in pairs_list:
        for p in pairs:
            key = (ord(p[0][0]) - ord('a'))//5
            if key in mapping:
                mapping[key].append(p)
            else:
                mapping[key] = [p]
    return mapping

def count_words(mapping):
    counter = {}
    for w, c in mapping[1]:
        if w in counter:
            counter[w] += c
        else:
            counter[w] = c
    return [(w, c) for w, c in counter.items()]

def read_file(path_to_file):
    with open(path_to_file) as f:
        data = f.read()
    return data

def sort(word_freq):
    return sorted(word_freq, key=operator.itemgetter(1), reverse=True)

splits = map(split_words, partition(read_file(sys.argv[1]), 200))
splits_per_word = regroup(splits)
word_freqs = sort(functools.reduce(operator.add, map(count_words, splits_per_word.items())))
for (w, c) in word_freqs[0:25]:
    print(w, '-', c)