import re

def read_words(path_to_file):
    with open('../../stop_words.txt') as f:
        stop_words = f.read().split(',')
    
    words = []
    with open(path_to_file) as f:
        for i, line in enumerate(f):
            for word in re.findall(r'[a-z]{2,}', line.lower()):
                if word not in stop_words:
                    words.append((i//45+1, word))
    return words