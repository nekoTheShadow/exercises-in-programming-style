import sys, re, operator, string

def extract_words(obj, path_to_file):
    with open(path_to_file) as f:
        obj['data'] = f.read()
    pattern = re.compile('[\W_]+')
    data_str = ''.join(pattern.sub(' ', obj['data']).lower())
    obj['data'] = data_str.split()

def load_stop_words(obj):
    with open('../stop_words.txt') as f:
        obj['stop_words'] = f.read().split(',')
    obj['stop_words'].extend(list(string.ascii_lowercase))

def increment_count(obj, w):
    obj['freqs'][w] = 1 if w not in obj['freqs'] else obj['freqs'][w]+1

def make_data_storage_obj():
    this = {
        'data' : [],
        'init' : lambda path_to_file : extract_words(this, path_to_file),
        'words' : lambda : this['data']
    }
    return this

def make_stop_words_obj():
    this = {
        'stop_words' : [],
        'init' : lambda : load_stop_words(this),
        'is_stop_word' : lambda word : word in this['stop_words']
    }
    return this

def make_word_freqs_obj():
    this = {
        'freqs' : {},
        'increment_count' : lambda w : increment_count(this, w),
        'sorted' : lambda : sorted(this['freqs'].items(), key=operator.itemgetter(1), reverse=True),
    }
    return this

data_storage_obj = make_data_storage_obj()
stop_words_obj = make_stop_words_obj()
word_freqs_obj = make_word_freqs_obj()

data_storage_obj['init'](sys.argv[1])
stop_words_obj['init']()

for w in data_storage_obj['words']():
    if not stop_words_obj['is_stop_word'](w):
        word_freqs_obj['increment_count'](w)

word_freqs = word_freqs_obj['sorted']()
for (w, c) in word_freqs[0:25]:
    print(w, '-', c)
