import re
import sys

RECURSION_LIMIT=5000
sys.setrecursionlimit(RECURSION_LIMIT+100)

def read_file_with_recursion(f, lines=[]):
    lines, eof,  = read_file(f, lines, False, RECURSION_LIMIT)
    if eof:
        return lines
    else:
        return read_file_with_recursion(f, lines)


def read_file(f, lines, eof, level):
    if level==0:
        return lines, False

    line = f.readline()
    if line=="":
        return lines, True

    lines.append(re.findall(r'[a-z]{2,}', line.lower()))
    return read_file(f, lines, eof, level-1)


def read_stopwords(s, stop_words=set()):
    i = s.find(',')
    if i == -1:
        return stop_words
    stop_words.add(s[:i])
    return read_stopwords(s[i+1:], stop_words)


def groupby_with_recursion(lines, stop_words, lineno=0, pagenos={}):
    pagenos, lineno = groupby(lines, stop_words, lineno, pagenos, RECURSION_LIMIT)
    if lineno==-1:
        return pagenos
    else:
        return groupby_with_recursion(lines, stop_words, lineno+1, pagenos)


def groupby(lines, stop_words, lineno, pagenos, level):
    if level==0:
        return pagenos, lineno
    if lineno==len(lines):
        return pagenos, -1
    groupby_with_words(lines[lineno], lineno, pagenos)
    return groupby(lines, stop_words, lineno+1, pagenos, level-1)


def groupby_with_words(words, lineno, pagenos):
    if len(words) == 0:
        return
    word = words[0]
    if not word in stop_words:
        if not word in pagenos:
            pagenos[word] = []
        if not lineno//45+1 in pagenos[word]:
            pagenos[word].append(lineno//45+1)
    groupby_with_words(words[1:], lineno, pagenos)


def print_wc_with_recursion(pagenos, i=0):
    i = print_wc(pagenos, i, RECURSION_LIMIT)
    if i != -1:
        print_wc_with_recursion(pagenos, i+1)


def print_wc(pagenos, i, level):
    if level==0:
        return i
    if i==len(pagenos):
        return -1
    
    w, c = pagenos[i]
    print(w, '-', join(c))
    return print_wc(pagenos, i+1, level-1)


def join(lst):
    if len(lst) == 1:
        return str(lst[0])
    return str(lst[0]) + "," + join(lst[1:])



with open(sys.argv[1]) as f:
    lines = read_file_with_recursion(f)
with open('../stop_words.txt') as f:
    stop_words = read_stopwords(f.read())

pagenos = groupby_with_recursion(lines, stop_words)
print_wc_with_recursion((sorted(pagenos.items())))