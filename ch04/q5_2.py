import sys

with open(sys.argv[1]) as f:
    lines = f.readlines()

words = []
lineno = 0
for line in lines:
    start_char = None
    i = 0
    for c in line:
        if start_char == None:
            if c.isalnum():
                start_char = i
        else:
            if not c.isalnum():
                found = False
                words.append([line[start_char:i].lower(), lineno//45+1])
                start_char = None
        i += 1
    lineno += 1

with open('../target_words.txt') as f:
    targets = f.read().split(',')

for i in range(len(targets)):
    x = i
    for j in range(i+1, len(targets)):
        if targets[x][0] > targets[j][0]:
            x = j
    targets[x], targets[i] = targets[i], targets[x]
    
    for x in range(len(words)):
        if words[x][0] == targets[i]:
            print(words[x-2][0], words[x-1][0], words[x][0], words[x+1][0], words[x+2][0], '-', words[x][1])

