import operator
import re
import sys
import itertools

stop_words = [(), None]
all_lines = [(), None]
all_words = [(), lambda : sum(([(word, i//45+1) for word in re.findall('[a-z]{2,}', line.lower())] for i, line in all_lines[0]), [])]
non_stop_words = [(), lambda : set(filter(lambda c: c[0] not in stop_words[0], all_words[0]))]
grouping_words = [(), lambda : [(w, set(map(operator.itemgetter(1), ps))) for w, ps in itertools.groupby(sorted(non_stop_words[0], key=operator.itemgetter(0)), key=operator.itemgetter(0))]]
sorted_data = [(), lambda : [w + ' - ' + ', '.join(map(str, sorted(pages))) for w, pages in sorted(grouping_words[0]) if len(pages) < 100] ]

all_columns = [stop_words, all_lines, all_words, non_stop_words, grouping_words, sorted_data]

def update():
    global all_columns
    for c in all_columns:
        if c[1] != None:
            c[0] = c[1]() 

stop_words[0] = set(open('../stop_words.txt').read().split(','))
all_lines[0] = list(enumerate(open(sys.argv[1])))
update()
for s in sorted_data[0]:
    print(s)

