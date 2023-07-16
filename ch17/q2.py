import sys, re, operator, string, inspect

def read_stop_words():
    print_info()
    if inspect.stack()[1][3] != 'extract_words':
        return None

    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return stop_words

def extract_words(path_to_file):
    print_info()
    with open(locals()['path_to_file']) as f:
        str_data = f.read()
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()
    stop_words = read_stop_words()
    return [w for w in word_list if not w in stop_words]

def frequencies(word_list):
    print_info()
    word_freqs = {}
    for w in locals()['word_list']:
        if w in word_freqs:
            word_freqs[w] += 1
        else:
            word_freqs[w] = 1
    return word_freqs

def sort(word_freq):
    print_info()
    return sorted(locals()['word_freq'].items(), key=operator.itemgetter(1), reverse=True)

def print_info():
    print(f'My name is {inspect.stack()[1].function}')
    print(f"  my locals are " + ','.join( f"{k}={v}" for k, v in inspect.stack()[1].frame.f_locals.items()))
    print(f"  and I'm being called from {inspect.stack()[2].function}")

def main():
    print_info()
    word_freqs = sort(frequencies(extract_words(sys.argv[1])))
    for (w, c) in word_freqs[0:25]:
        print(w, '-', c)

if __name__ == "__main__":
    main()
