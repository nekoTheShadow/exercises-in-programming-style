import re, sys


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
    pattern = re.compile('\w+')
    words = []
    with open(path_to_file) as f:
        for i, line in enumerate(f):
            for word in pattern.findall(line.lower()):
                words.append((i//45+1, word))
    return words

def read_target_words():
    with open('../target_words.txt') as f:
        return f.read().split(',')
    
@AcceptTypes(list, str)
def find(words, target_word):
    results = []
    for i, (page, word) in enumerate(words):
        if word == target_word:
            results.append((page, words[i-2][1], words[i-1][1], words[i][1], words[i+1][1], words[i+2][1]))
    return results

words = extract_words(sys.argv[1])
for target_word in sorted(read_target_words()):
    for result in find(words, target_word):
        print(*result[1:], " - ", result[0])