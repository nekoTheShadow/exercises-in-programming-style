import sys, re, operator, string

class TFQuarantine:
    def __init__(self, func):
        self._funcs = [func]

    def bind(self, func):
        self._funcs.append(func)
        return self

    def execute(self):
        def guard_callable(v):
            return v() if callable(v) else v
        
        value = lambda : None
        for func in self._funcs:
            value = func(guard_callable(value))
        print(guard_callable(value))


def get_input(arg):
    def _f():
        return sys.argv[1]
    return _f


def extract_words(path_to_file):
    def _f():
        pattern = re.compile('[\W_]+')
        word_list = []
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                word_list.extend((word, i//45+1) for word in pattern.sub(' ', line).lower().split())
        return word_list
    return _f

def grep(word_list):
    def _f():
        results = []
        with open('../target_words.txt') as f:
            target_words = f.read().split(',')
        for target_word in sorted(target_words):
            for i, (word, page) in enumerate(word_list):
                if word == target_word:
                    results.append((page, *(word_list[i+j][0] for j in range(-2, 3))))
        return results
    return _f

def text(results):
    return '\n'.join(' '.join(map(str, result[1:])) + f' - {result[0]}' for result in results)

TFQuarantine(get_input)\
.bind(extract_words)\
.bind(grep)\
.bind(text)\
.execute()
