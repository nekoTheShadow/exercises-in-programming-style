import sys, string

# 大域変数の代わりにq2.tmpファイルを利用する

def read_file(path_to_file):
    with open(path_to_file) as src, open('q2.tmp', 'w') as dst:
        dst.write(src.read())


def filter_chars_and_normalize():
    with open('q2.tmp') as f:
        data = list(f.read())
    
    for i in range(len(data)):
        if not data[i].isalnum():
            data[i] = ' '
        else:
            data[i] = data[i].lower()
    
    with open('q2.tmp', 'w') as f:
        f.writelines(data)


def scan():
    with open('q2.tmp') as f:
        data = f.read()
    with open('q2.tmp', 'w') as f:
        for word in data.split():
            f.write(word)
            f.write('\n')


def remove_stop_words():
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    stop_words.extend(list(string.ascii_lowercase))

    with open('q2.tmp') as f:
        words = list(map(str.strip, f.readlines()))

    indexes = []
    for i in range(len(words)):
        if words[i].strip() in stop_words:
            indexes.append(i)
    for i in reversed(indexes):
        words.pop(i)

    with open('q2.tmp', 'w') as f:
        for word in words:
            f.write(word)
            f.write('\n')


def frequencies():
    with open('q2.tmp') as f:
        words = list(map(str.strip, f.readlines()))
    word_freqs = []

    for w in words:
        keys = [wd[0] for wd in word_freqs]
        if w in keys:
            word_freqs[keys.index(w)][1] += 1
        else:
            word_freqs.append([w, 1])
    
    with open('q2.tmp', 'w') as f:
        for wd in word_freqs:
            print(wd[0], wd[1], file=f)


def sort():
    with open('q2.tmp') as f:
        word_freqs = [v.strip().split() for v in f]
    word_freqs.sort(key=lambda x: int(x[1]), reverse=True)

    with open('q2.tmp', 'w') as f:
        for wd in word_freqs:
            print(wd[0], wd[1], file=f)


read_file(sys.argv[1])
filter_chars_and_normalize()
scan()
remove_stop_words()
frequencies()
sort()

with open('q2.tmp') as f:
        word_freqs = [v.strip().split() for v in f]
for tf in word_freqs[0:25]:
    print(tf[0], '-', tf[1])