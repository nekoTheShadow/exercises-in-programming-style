import re
import string

def read_words(path_to_file):
    with open('../../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.append(string.ascii_lowercase)
    
    words = []
    with open(path_to_file) as f:
        for i, line in enumerate(f):
            for word in re.sub(r'[\W_]+', ' ', line.lower()).split():
                if word.isalpha() and word not in stop_words:
                    words.append((i//45+1, word))
    return words