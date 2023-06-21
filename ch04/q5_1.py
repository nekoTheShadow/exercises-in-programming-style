import sys, string

word_freqs = []

with open('../stop_words.txt') as f:
    stop_words = f.read().split(',')
stop_words.extend(list(string.ascii_lowercase))

with open(sys.argv[1]) as f:
    lines = f.readlines()

lineno = 0
for line in lines:
    start_char = None
    i = 0
    for c in line:
        if start_char == None:
            if c.isalpha():
                start_char = i
        else:
            if not c.isalpha():
                found = False
                word = line[start_char:i].lower()
                pageno = lineno//45+1
                if word not in stop_words:
                    for lst in word_freqs:
                        if word == lst[0]:
                            lst.append(pageno)
                            found = True
                            break
                    if not found:
                        word_freqs.append([word, pageno])
                start_char = None
        i += 1
    lineno += 1

for i in range(len(word_freqs)):
    x = i
    for j in range(i+1, len(word_freqs)):
        if word_freqs[x][0] > word_freqs[j][0]:
            x = j
    word_freqs[x], word_freqs[i] = word_freqs[i], word_freqs[x]

    pagenos = []
    for pageno in word_freqs[i][1:]:
        if str(pageno) not in pagenos:
            pagenos.append(str(pageno))
    if len(pagenos) < 100:
        s = word_freqs[i][0] + ' - '
        for j in range(len(pagenos)):
            s += pagenos[j]
            if j < len(pagenos)-1:
                s += ', '
        print(s)
            