def read_file(path_to_file, func):
    lines = []
    with open(path_to_file) as f:
        for line in f:
            lines.append(line)
    func(lines, remove_stop_words)


def scan(lines, func):
    import re
    matrix = []
    for line in lines:
        matrix.append(re.findall(r'[a-z]{2,}', line.lower()))
    func(matrix, group_by)


def remove_stop_words(matrix, func):
    with open('../stop_words.txt') as f:
        stop_words = f.read().split(',')
    
    next_matrix = [[word for word in words if not word in stop_words] for words in matrix]
    func(next_matrix, remove100)


def group_by(matrix, func):
    groups = {}
    for i, words in enumerate(matrix):
        for word in words:
            if not word in groups:
                groups[word] = []
            if not i//45+1 in groups[word]:
                groups[word].append(i//45+1)
    func(groups, sort)


def remove100(groups, func):
    matrix = []
    for word in groups:
        if len(groups[word]) < 100:
            matrix.append([word, *groups[word]])
    func(matrix, print_text)


def sort(matrix, func):
    func(list(sorted(matrix, key=lambda a : a[0])), no_op)


def print_text(matrix, func):
    for row in matrix:
        print(row[0], '-', ', '.join(map(str, row[1:])))
    func(None)


def no_op(func):
    return

import sys

# read_file 
# scan 
# remove_stop_words 
# group_by
# remove100
# sort
# print_text
read_file(sys.argv[1], scan)
