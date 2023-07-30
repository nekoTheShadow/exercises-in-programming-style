import sys, re, operator, string
import typing

def extract_words(path_to_file: str) -> typing.List[str]:
    with open(path_to_file) as f:
        str_data = f.read()    
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list: typing.List[str]) -> typing.Dict[str, int]:
    word_freqs: typing.Dict[str, int] = {}
    for w in word_list:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(word_freq: typing.Dict[str, int]) -> typing.List[typing.Tuple[str, int]]:
    return sorted(word_freq.items(), key=operator.itemgetter(1), reverse=True)

word_freqs = sort(frequencies(extract_words(sys.argv[1])))
for (w, c) in word_freqs[0:25]:
    print(w, '-', c)

# pip install mypy
# /home/dev/.local/bin/mypy q3.py 