import re, string, collections, sys

class AcceptTypes():
    def __init__(self, *args):
        self._args = args

    def __call__(self, f):
        def wrapped_f(*args):
            for i in range(len(self._args)):
                if type(args[i]) != self._args[i]:
                    raise TypeError(f'Expecting {str(self._args[i])} got {str(type(args[i]))}')
            return f(*args)
        return wrapped_f
    

@AcceptTypes(str)
def extract_words(path_to_file):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    
    pattern = re.compile('[a-z]+')
    words = []
    with open(path_to_file) as f:
        for i, line in enumerate(f):
            for word in pattern.findall(line.lower()):
                if word not in stop_words:
                    words.append((i//45+1, word))
    return words


@AcceptTypes(list)
def grouping(words):
    pages = collections.defaultdict(list)
    for page, word in words:
        if page not in pages[word]:
            pages[word].append(page)
    return pages


@AcceptTypes(collections.defaultdict)
def to_texts(pages):
    texts = []
    for k, v in sorted(pages.items()):
        texts.append(f'{k} - ' + ', '.join(map(str, v)))
    return texts

for text in to_texts(grouping(extract_words(sys.argv[1]))):
    print(text)