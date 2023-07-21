import re, string, collections, time, sys

def profile(f):
    def profilewrapper(*arg, **kw):
        start_time = time.time()
        ret_value = f(*arg, **kw)
        elapsed = time.time() - start_time
        print("%s(...) took %s secs" % (f.__name__, elapsed))
        return ret_value
    return profilewrapper

@profile
def read_stop_words():
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(iter(string.ascii_lowercase))
    return stop_words

@profile
def read_lines(path_to_file):
    lines = []
    with open(path_to_file) as f:
        for i, line in enumerate(f):
            lines.append((i//45+1, line))
    return lines

@profile
def split_words(lines):
    pattern = re.compile('[a-z]+')
    words = []
    for page, line in lines:
        for word in pattern.findall(line.lower()):
            words.append((page, word))
    return words

@profile
def tally(words):
    pages = collections.defaultdict(list)
    stop_words = read_stop_words()
    for page, word in words:
        if not word in stop_words and not page in pages[word]:
            pages[word].append(page)
    return pages
            

@profile
def main():
    pages = tally(split_words(read_lines(sys.argv[1])))
    for word, pages in sorted(pages.items()):
        if len(pages) < 100:
            print(word, ', '.join(map(str, pages)))

main()