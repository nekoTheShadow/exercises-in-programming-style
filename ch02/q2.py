import sys, re, operator, string

stack = []
heap = {}

def read_file():
    f = open(stack.pop())
    stack.append([f.read()])
    f.close()

def filter_chars():
    stack.append(re.compile('[\W_]+'))
    stack.append([stack.pop().sub(' ', stack.pop()[0]).lower()])

def scan():
    stack.extend(stack.pop()[0].split())

def remove_stop_words():
    f = open('../stop_words.txt')
    stack.append(f.read().split(','))
    f.close()

    stack[-1].extend(list(string.ascii_lowercase))
    heap['stop_words'] = stack.pop()

    heap['words'] = []
    while len(stack) > 0:
        if stack[-1] in heap['stop_words']:
            stack.pop()
        else:
            heap['words'].append(stack.pop())

    stack.extend(heap['words'])
    del heap['stop_words']
    del heap['words']
    
def frequencies():
    heap['word_freqs'] = {}
    heap['word'] = None
    heap['i'] = None

    while len(stack) > 0:
        heap['word'] = stack.pop()
        stack.extend(heap['word_freqs'])
        stack.append(False)
        stack.append(len(heap['word_freqs']))
        while True:
            heap['i'] = stack.pop()
            if heap['i'] == 0:
                break

            if stack.pop():
                stack.pop()
                stack.append(True)
            else:
                stack.append(stack.pop()==heap['word'])
            stack.append(heap['i']-1)
        
        if stack.pop():
             heap['word_freqs'][heap['word']] += 1
        else:
             heap['word_freqs'][heap['word']] = 1

    stack.append(heap['word_freqs'])
    del heap['word_freqs']
    del heap['word']
    del heap['i']

def sort():
    stack.extend(sorted(stack.pop().items(), key=operator.itemgetter(1)))

stack.append(sys.argv[1])
read_file()
filter_chars()
scan()
remove_stop_words()
frequencies()
sort()

stack.append(0)
while stack[-1] < 25 and len(stack) > 1:
    heap['i'] = stack.pop()
    (w, f) = stack.pop()
    print(w, '-', f)
    stack.append(heap['i'])
    stack.append(1)
    stack.append(stack.pop() + stack.pop())
