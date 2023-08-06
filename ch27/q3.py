import re, itertools, operator, sys

cells = [
    [(), None], 
    [(), None],
    [(), lambda : list(map(lambda w : w if w not in cells[1][0] else '', cells[0][0]))],
    [(), lambda : set([w for w in cells[2][0] if w!=''])],
    [(), lambda : list(map(lambda w, word_list : word_list.count(w), cells[3][0], itertools.repeat(cells[2][0], len(cells[3][0]))))],
    [(), lambda : sorted(zip(list(cells[3][0]),  list(cells[4][0])), key=operator.itemgetter(1), reverse=True)]
]
def update():
    global cells
    for cell in cells:
        if cell[1] is not None:
            cell[0] = cell[1]()



cells[0][0] = re.findall('[a-z]{2,}', open(sys.argv[1]).read().lower())
cells[1][0] = set(open('../stop_words.txt').read().split(','))
update()

for (w, c) in cells[5][0][:25]:
    print(w, '-', c)

# 問題の意図汲み取れているのか?