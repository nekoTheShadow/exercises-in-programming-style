
import re, collections, sys, string


def filter_chars_and_normalize(line):
    return re.sub('[\W_]+', ' ', line).lower()

def scan(line):
    return line.split()

def frequencies(words):
    return collections.Counter(words)

def merge(counters):
    merged_counter = collections.Counter()
    for counter in counters:
        for key in counter:
            merged_counter[key] += counter[key]
    return merged_counter

def remove_stop_words(counter):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))
    return collections.Counter({key : counter[key] for key in counter if key not in stop_words})

def print_all(counter):
    for key, value in counter.most_common(25):
        print(key, '-', value)

with open(sys.argv[1]) as f:
    print_all(remove_stop_words(merge([frequencies(scan(filter_chars_and_normalize(line))) for line in f])))