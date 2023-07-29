import re, sys, traceback

def read_words(path_to_file):
    assert (type(path_to_file) is str), 'I need a string!'
    assert (path_to_file), 'I need a non-empty string!'
    pattern = re.compile(r'[a-z]{2,}')
    words = []
    with open(path_to_file) as f:
        for lineno, line in enumerate(f):
            words.extend((lineno//45+1, word) for word in pattern.findall(line.lower()))
    return words


def remove_stop_words(words):
    assert (type(words) is list), 'I need a list!'
    assert (words), 'I need a non-empty list!'
    with open('../stop_words.txt') as f:
        stop_words = set(f.read().split(','))
    return [(page, word) for page, word in words if word not in stop_words]


def group_by(words):
    assert (type(words) is list), 'I need a list!'
    assert (words), 'I need a non-empty list!'
    pages = {}
    for page, word in words:
        if word not in pages:
            pages[word] = []
        if page not in pages[word]:
            pages[word].append(page)
    return pages


def sort(pages):
    assert (type(pages) is dict), 'I need a dictionary!'
    assert (pages), 'I need a non-empty dictionary!'
    return sorted(pages.items())


try:
    assert(len(sys.argv)>1), 'You idiot! Ineed an input file!'
    filename = sys.argv[1]
    for word, pages in sort(group_by(remove_stop_words(read_words(filename)))):
        if len(pages) < 100:
            print(word, '-', ', '.join(map(str, pages)))
except Exception as e:
    print(f'Something wrong: {e}')