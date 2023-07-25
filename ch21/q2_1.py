import re, sys

def read_words(path_to_file):
    if type(path_to_file) is not str or not path_to_file:
        return []

    pattern = re.compile(r'[a-z]{2,}')
    words = []

    try:
        with open(path_to_file) as f:
            for lineno, line in enumerate(f):
                words.extend((lineno//45+1, word) for word in pattern.findall(line.lower()))
    except IOError as e:
        print(f"I/O error({e.errno}) when opening {path_to_file}: {e.strerror}! I quit!")
        return []
    
    return words


def remove_stop_words(words):
    if type(words) is not list or not words:
        return []

    try:
        with open('../stop_words.txt') as f:
            stop_words = set(f.read().split(','))
    except IOError as e:
        print(f"I/O error({e.errno}) when opening ../stop_words.txt: {e.strerror}! I quit!")
        return []

    return [(page, word) for page, word in words if word not in stop_words]


def group_by(words):
    if type(words) is not list or not words:
        return []

    pages = {}
    for page, word in words:
        if word not in pages:
            pages[word] = []
        if page not in pages[word]:
            pages[word].append(page)
    return pages


def sort(pages):
    if type(pages) is not dict or not dict:
        return []
    
    return sorted(pages.items())


filename = sys.argv[1] if len(sys.argv) > 1 else '../input.txt'
for word, pages in sort(group_by(remove_stop_words(read_words(filename)))):
    if len(pages) < 100:
        print(word, '-', ', '.join(map(str, pages)))