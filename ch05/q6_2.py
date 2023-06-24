import sys

lines = []
words = []
targets = []

def read_targets():
    global targets
    with open('../target_words.txt') as f:
        targets = f.read().split(',')
    targets.sort()

def read_flie():
    global lines
    with open(sys.argv[1]) as f:
        lines = f.readlines()

def normalize():
    global lines
    for i in range(len(lines)):
        chars = list(lines[i])
        for j in range(len(chars)):
            chars[j] = chars[j].lower() if chars[j].isalnum() else ' '
        lines[i] = ''.join(chars)

def split():
    global lines
    global words
    for i in range(len(lines)):
        for word in lines[i].split():
            words.append([word, i//45+1])


def display():
    for target in sorted(targets):
        for i in range(len(words)):
            if words[i][0] == target:
                print(words[i-2][0], words[i-1][0],words [i][0], words[i+1][0], words[i+2][0], '-', words[i][1])

read_targets()
read_flie()
normalize()
split()
display()