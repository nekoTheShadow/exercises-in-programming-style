import re
import sys

RECURSION_LIMIT=5000
sys.setrecursionlimit(RECURSION_LIMIT+100)

def read_file_with_recursion(f, lineno=0, words=[]):
    words, lineno = read_file(f, words, lineno, RECURSION_LIMIT)
    if lineno==-1:
        return words
    else:
        return read_file_with_recursion(f, lineno+1, words)
    

def read_file(f, words, lineno, level):
    if level==0:
        return words, lineno

    line = f.readline()
    if line=="":
        return words, -1
    
    extend(words, re.findall(r'[\w]+', line.lower()), lineno)
    return read_file(f, words, lineno+1, level-1)


def extend(alist, blist, lineno):
    if len(blist)==0:
        return
    alist.append((blist[0], lineno//45+1))
    extend(alist, blist[1:], lineno)


def display_with_targets(words, targets):
    if len(targets)==0:
        return
    display_with_recursion(words, targets[0])
    display_with_targets(words, targets[1:])


def display_with_recursion(words, target, i=0):
    i = display(words, target, i, RECURSION_LIMIT)
    if i != -1:
        display_with_recursion(words, target, i+1)


def display(words, target, i, level):
    if level==0:
        return i
    if i==len(words):
        return -1
    word, pageno = words[i]
    if word == target:
        print(words[i-2][0], words[i-1][0], words[i][0], words[i+1][0], words[i+2][0], '-', pageno)
    return display(words, target, i+1, level-1)


def read_targets(s, targets=[]):
    i = s.find(',')
    if i == -1:
        targets.append(s)
        targets.sort()
        return targets
    targets.append(s[:i])
    return read_targets(s[i+1:], targets)

with open(sys.argv[1]) as f:
    words = read_file_with_recursion(f)
with open('../target_words.txt') as f:
    targets = read_targets(f.read())
display_with_targets(words, targets)