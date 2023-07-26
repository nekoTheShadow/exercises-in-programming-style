import re, sys, traceback

def read_words(path_to_file):
    assert (type(path_to_file) is str), "I need a string!"
    assert (path_to_file), "I need a non-empty string!"

    pattern = re.compile(r'[a-z]{2,}')
    words = []

    try:
        with open(path_to_file) as f:
            for lineno, line in enumerate(f):
                words.extend((lineno//45+1, word) for word in pattern.findall(line.lower()))
    except IOError as e:
        print(f"I/O error({e.errno}) when opening {path_to_file}: {e.strerror}! I quit!")
        raise e
    
    return words


def remove_stop_words(words):
    assert (type(words) is list), "I need a list!"
    assert (words), "I need a non-empty list!"

    try:
        with open('../stop_words.txt') as f:
            stop_words = set(f.read().split(','))
    except IOError as e:
        print(f"I/O error({e.errno}) when opening ../stop_words.txt: {e.strerror}! I quit!")
        raise e

    return [(page, word) for page, word in words if word not in stop_words]


def group_by(words):
    assert (type(words) is list), "I need a list!"
    assert (words), "I need a non-empty list!"

    pages = {}
    for page, word in words:
        if word not in pages:
            pages[word] = []
        if page not in pages[word]:
            pages[word].append(page)
    return pages


def sort(pages):
    assert (type(pages) is dict), "I need a dictionary!"
    assert (pages), "I need a non-empty dictionary!"
    try:
        return sorted(pages.items())
    except Exception as e:
        print(f"Somthing threw {e}")
        raise e


try:
    assert(len(sys.argv)>1), "You idiot! Ineed an input file!"
    filename = sys.argv[1]
    for word, pages in sort(group_by(remove_stop_words(read_words(filename)))):
        if len(pages) < 100:
            print(word, '-', ', '.join(map(str, pages)))
except Exception as e:
    print(f"Something wrong: {e}")
    traceback.print_exc()