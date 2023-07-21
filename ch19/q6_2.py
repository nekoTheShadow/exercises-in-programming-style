import re, time, sys

def profile(f):
    def profilewrapper(*arg, **kw):
        start_time = time.time()
        ret_value = f(*arg, **kw)
        elapsed = time.time() - start_time
        print("%s(...) took %s secs" % (f.__name__, elapsed))
        return ret_value
    return profilewrapper

@profile
def read_lines(path_to_file):
    lines = []
    with open(path_to_file) as f:
        for i, line in enumerate(f):
            lines.append((i//45+1, line))
    return lines

@profile
def split_words(lines):
    pattern = re.compile('\w+')
    words = []
    for page, line in lines:
        for word in pattern.findall(line.lower()):
            words.append((page, word))
    return words

@profile
def read_target_words():
    with open('../target_words.txt') as f:
        return f.read().split(',')

@profile    
def main():
    words = split_words(read_lines(sys.argv[1]))
    target_words = read_target_words()
    for target_word in sorted(target_words):
        for i, (page, word) in enumerate(words):
            if word == target_word:
                print(*(words[i+j][1] for j in range(-2, 3)), "-", page)

main()



