import re, itertools, operator

all_words = [[], None]
stop_words = [(), None]
non_stop_words = [(), lambda : list(map(lambda w : w if w not in stop_words[0] else '', all_words[0]))]
unique_words = [(),lambda : set([w for w in non_stop_words[0] if w!=''])]
counts = [(), lambda : list(map(lambda w, word_list : word_list.count(w), unique_words[0], itertools.repeat(non_stop_words[0], len(unique_words[0]))))]
sorted_data = [(), lambda : sorted(zip(list(unique_words[0]),  list(counts[0])), key=operator.itemgetter(1), reverse=True)]

all_columns = [all_words, stop_words, non_stop_words, unique_words, counts, sorted_data]

def update():
    global all_columns
    for c in all_columns:
        if c[1] != None:
            c[0] = c[1]() 

stop_words[0] = set(open('../stop_words.txt').read().split(','))
while True:
    file_name = input('File Name: ')
    all_words[0].extend(re.findall('[a-z]{2,}', open(file_name).read().lower()))
    update()
    for (w, c) in sorted_data[0][:25]:
        print(w, '-', c)

