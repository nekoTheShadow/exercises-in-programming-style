import re, sys


def read_words(path_to_file):
    if type(path_to_file) is not str or not path_to_file:
        return []

    pattern = re.compile(r'\w+')
    words = []

    try:
        with open(path_to_file) as f:
            for lineno, line in enumerate(f):
                words.extend((lineno//45+1, word) for word in pattern.findall(line.lower()))
    except IOError as e:
        print(f"I/O error({e.errno}) when opening {path_to_file}: {e.strerror}! I quit!")
        return []
    
    return words


def read_target_words():
    try:
        with open('../target_words.txt') as f:
            target_words = f.read().split(',')
    except IOError as e:
        print(f"I/O error({e.errno}) when opening ../stop_words.txt: {e.strerror}! I quit!")
        return []

    target_words.sort()
    return target_words


def find(words, target_word):
    if type(words) is not list or not words:
        return []
    if type(target_word) is not str or not target_word:
        return []
    
    results = []
    for i, (page, word) in enumerate(words):
        if word == target_word:
            result = (page, *(words[i+j][1] for j in range(-2, 3)))
            results.append(result)
    return results


filename = sys.argv[1] if len(sys.argv) > 1 else '../input.txt'
words = read_words(filename)
target_words = read_target_words()
for target_word in target_words:
    for result in find(words, target_word):
        print(*result[1:], '-', result[0])