import re
import sys



target_words = [(), None]
all_lines = [(), None]
all_words = [(), lambda : sum(([(word, i//45+1) for word in re.findall('\w+', line.lower())] for i, line in all_lines[0]), [])]
result_sets = [(), lambda : [[(page, all_words[0][i-2][0], all_words[0][i-1][0], all_words[0][i][0], all_words[0][i+1][0], all_words[0][i+2][0]) for i, (word, page) in enumerate(all_words[0]) if target_word == word] for target_word in target_words[0]]]
displays = [(), lambda : [' '.join(result[1:]) + ' - ' + str(result[0]) for result in sum(result_sets[0], [])]]

all_columns = [target_words, all_lines, all_words, result_sets, displays]

def update():
    global all_columns
    for c in all_columns:
        if c[1] != None:
            c[0] = c[1]() 

target_words[0] = list(sorted(open('../target_words.txt').read().split(',')))
all_lines[0] = list(enumerate(open(sys.argv[1])))
update()
for display in displays[0]:
    print(display)