import sys, re, operator, string

class Stack:
    def __init__(self):
        self._stack = []
    
    def push(self, v):
        self._stack.append(v)
    
    def pop(self):
        return self._stack.pop()

    def peek(self):
        return self._stack[-1]
    
    def empty(self):
        return len(self._stack)==0


stack = Stack()
heap = {}

def read_file():
    f = open(stack.pop())
    stack.push([f.read()])
    f.close()

def filter_chars():
    stack.push(re.compile('[\W_]+'))
    stack.push([stack.pop().sub(' ', stack.pop()[0]).lower()])

def scan():
    for v in stack.pop()[0].split():
        stack.push(v)

def remove_stop_words():
    f = open('../stop_words.txt')
    stack.push(f.read().split(','))
    f.close()

    stack.peek().extend(list(string.ascii_lowercase))
    heap['stop_words'] = stack.pop()

    heap['words'] = []
    while not stack.empty():
        if stack.peek() in heap['stop_words']:
            stack.pop()
        else:
            heap['words'].append(stack.pop())

    for v in heap['words']:
        stack.push(v)
    del heap['stop_words']
    del heap['words']
    
def frequencies():
    heap['word_freqs'] = {}
    while not stack.empty():
        if stack.peek() in heap['word_freqs']:
            stack.push(heap['word_freqs'][stack.peek()])
            stack.push(1)
            stack.push(stack.pop() + stack.pop())
        else:
            stack.push(1)
        heap['word_freqs'][stack.pop()] = stack.pop()  

    stack.push(heap['word_freqs'])
    del heap['word_freqs']

def sort():
    for v in sorted(stack.pop().items(), key=operator.itemgetter(1)):
        stack.push(v)

stack.push(sys.argv[1])
read_file()
filter_chars()
scan()
remove_stop_words()
frequencies()
sort()

stack.push(0)
while stack.peek() < 25:
    heap['i'] = stack.pop()
    if stack.empty():
        break
    (w, f) = stack.pop()
    print(w, '-', f)
    stack.push(heap['i'])
    stack.push(1)
    stack.push(stack.pop() + stack.pop())
