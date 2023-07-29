import re, sys, traceback


def read_words(path_to_file):
    assert (type(path_to_file) is str), 'I need a string!'
    assert (path_to_file), 'I need a non-empty string!'
    pattern = re.compile(r'\w+')
    words = []
    with open(path_to_file) as f:
        for lineno, line in enumerate(f):
            words.extend((lineno//45+1, word) for word in pattern.findall(line.lower()))
    return words


def read_target_words():
    with open('../target_words.txt') as f:
        target_words = f.read().split(',')
    target_words.sort()
    return target_words


def find(words, target_word):
    assert (type(words) is list), 'I need a list!'
    assert (words), 'I need a non-empty list!'
    assert (type(target_word) is str), 'I need a string!'
    assert (target_word), 'I need a non-empty string!'
    results = []
    for i, (page, word) in enumerate(words):
        if word == target_word:
            result = (page, *(words[i+j][1] for j in range(-2, 3)))
            results.append(result)
    return results


try:
    assert(len(sys.argv)>1), 'You idiot! Ineed an input file!'
    filename = sys.argv[1] if len(sys.argv) > 1 else '../input.txt'
    words = read_words(filename)
    target_words = read_target_words()
    for target_word in target_words:
        for result in find(words, target_word):
            print(*result[1:], '-', result[0])
except Exception as e:
    print(f'Something wrong: {e}')