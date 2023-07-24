import re

def read_words(path_to_file):
    words = []
    with open(path_to_file) as f:
        for i, line in enumerate(f):
            for word in re.findall(r'\w+', line.lower()):
                words.append((i//45+1, word))
    return words