# 1. stop_words.txtを読み込む
# 2. 入力ファイルをオープンする
# 3. 入力ファイルがEOFになるまで以下の処理を繰り返す
#   1. ファイルを1行読み込む
#   2. 不要な文字を除去する & 小文字に変換する
#   3. 単語に分割する
#   4. stop_wordを取り除く
#   5. カウンタに記録する。
# 4. 入力ファイルをクローズする
# 5. カウンタをソートする
# 5. コンソールに表示する。

import string, sys

stop_words = []
fp = None
line = None
words = []
counter = []

def read_stop_words():
    global stop_words
    with open('../stop_words.txt') as f:
        stop_words = f.readline().split(',')
    stop_words.extend(list(string.ascii_lowercase))


def open_input_file():
    global fp
    fp = open(sys.argv[1])


def read_input_file():
    global line
    line = fp.readline()


def normalize_line():
    global line
    a = list(line)
    for i in range(len(a)):
        a[i] = a[i].lower() if a[i].isalnum() else ' '
    line = ''.join(a)


def scan_line():
    global line
    global words
    words = line.split()


def remove_words():
    global words
    global stop_words
    indexes = []
    for i in range(len(words)):
        if words[i] in stop_words:
            indexes.append(i)
    for i in reversed(indexes):
        words.pop(i)

def frequencies():
    global counter
    for word in words:
        found = False
        for i in range(len(counter)):
            if counter[i][0] == word:
                counter[i][1] += 1
                found = True
                break
        if not found:
            counter.append([word, 1])

def close_input_file():
    global fp
    fp.close()


def sort_counter():
    global counter
    for i in range(len(counter)):
        x = i
        for j in range(i+1, len(counter)):
            if counter[x][1] < counter[j][1]:
                x = j
        counter[x], counter[i] = counter[i], counter[x]


def display_counter():
    global counter
    for i in range(25):
        if i < len(counter):
            print(counter[i][0], '-', counter[i][1])

read_stop_words()

open_input_file()
while True:
    read_input_file()
    if line == '':
        break
    normalize_line()
    scan_line()
    remove_words()
    frequencies()
close_input_file()

sort_counter()
display_counter()
