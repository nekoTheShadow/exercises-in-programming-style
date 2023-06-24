
import sys

lines = []
counter = []

def read_flie():
    global lines
    with open(sys.argv[1]) as f:
        lines = f.readlines()

def normalize():
    global lines
    for i in range(len(lines)):
        chars = list(lines[i])
        for j in range(len(chars)):
            chars[j] = chars[j].lower() if chars[j].isalpha() else ' '
        lines[i] = ''.join(chars)

def split():
    global lines
    for i in range(len(lines)):
        lines[i] = lines[i].split()

def remove():
    global lines
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    
    for i in range(len(lines)):
        indexes = [j for j in range(len(lines[i])) if lines[i][j] in stop_words]
        for j in reversed(indexes):
            lines[i].pop(j)

def count():
    global lines
    global counter
    for i in range(len(lines)):
        for word in lines[i]:
            found = False
            for e in counter:
                if e[0] == word and (i//45+1) not in e[1:]:
                    e.append(i//45+1)
                    found = True
                    break
            if not found:
                counter.append([word, i//45+1])


def sort():
    global counter
    counter.sort(key=lambda v : v[0])


def display():
    global counter
    for e in counter:
        if len(e[1:]) < 100:
            print(e[0], '-', ' ,'.join(map(str, e[1:])))


# 1. ファイルを読み込む
# 2. 正規化する
# 3. 単語に分割する
# 4. stop_wordsを取り除く
# 5. カウンタに記録する
# 6. カウンタをソートする
# 7. コンソールに表示する

read_flie()
normalize()
split()
remove()
count()
sort()
display()