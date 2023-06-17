import sys, re

stack = []
heap = {}

# ファイルを読み込む
heap['i'] = None
heap['j'] = None
heap['fp'] = None
heap['line'] = None
heap['words'] = None

stack.append(open(sys.argv[1]))
stack.append(0)
while True:
    heap['i'] = stack.pop()
    heap['fp'] = stack.pop()

    stack.append(heap['fp'])
    heap['line'] = stack.pop().readline()

    stack.append(heap['line'])
    if stack.pop() == '':
        break

    stack.append(heap['line'])
    stack.append(re.compile('[a-z]{2,}'))
    stack.append(stack.pop().findall(stack.pop().lower()))
    stack.append(0)
    
    while True:
        heap['j'] = stack.pop()
        heap['words'] = stack.pop()

        stack.append(heap['words'])
        stack.append(heap['j'])
        if stack.pop() == len(stack.pop()):
            break

        stack.append(heap['i'])
        stack.append(heap['j'])
        stack.append(heap['words'])
        stack.append((stack.pop()[stack.pop()], stack.pop()//45+1))
        stack.append(heap['words'])
        stack.append(heap['j'])
        stack.append(stack.pop()+1)

    stack.append(heap['fp'])
    stack.append(heap['i'])
    stack.append(stack.pop()+1)

del heap['i']
del heap['j']
del heap['fp']
del heap['line']
del heap['words']

# 集計する
heap['dict'] = {}
heap['word'] = None
while stack:
    heap['word'] = stack.pop()
    stack.append(heap['dict'])
    stack.append(heap['word'])
    if stack.pop()[0] not in stack.pop():
        stack.append(heap['word'])
        stack.append(heap['dict'])
        stack.append([])
        stack.pop()[stack.pop()[0]] = stack.pop()
    
    # なぜか動いている
    stack.append(heap['word'])
    stack.append(heap['dict'])
    stack.append(heap['word'])
    stack.append(heap['word'])
    stack.append(heap['dict'])
    stack.append(stack.pop()[stack.pop()[0]])
    stack.append(stack.pop() + [stack.pop()[1]])
    stack.pop()[stack.pop()[0]] = stack.pop()
stack.append(heap['dict'])
del heap['dict']
del heap['word']

# キーをソートする
stack.append(list(sorted(stack[-1])))
stack.append(0)


heap['i'] = None
heap['j'] = None
heap['keys'] = None
heap['dict'] = None
heap['pages'] = None
heap['str'] = None
heap['count'] = None
heap['key'] = None
while True:
    heap['i'] = stack.pop()
    heap['keys'] = stack.pop()
    heap['dict'] = stack.pop()
    stack.append(heap['i'])
    stack.append(heap['keys'])
    if len(stack.pop()) == stack.pop():
        break

    stack.append(heap['i'])
    stack.append(heap['keys'])
    heap['key'] = stack.pop()[stack.pop()]

    stack.append(heap['key'])
    stack.append(heap['dict'])
    heap['pages'] = stack.pop()[stack.pop()]
    
    stack.append(0)
    while True:
        heap['j'] = stack.pop()

        stack.append(heap['j'])
        stack.append(heap['pages'])
        if len(stack.pop()) == stack.pop():
            break
        
        if len(stack) == 0:
            stack.append(heap['j'])
            stack.append(heap['pages'])
            stack.append(stack.pop()[stack.pop()])
        else:
            stack.append(heap['j'])
            stack.append(heap['pages'])
            if stack.pop()[stack.pop()] != stack[-1]:
                stack.append(heap['j'])
                stack.append(heap['pages'])
                stack.append(stack.pop()[stack.pop()])
        stack.append(heap['j'])
        stack.append(stack.pop()+1)

    
    stack.append(heap['key'])
    stack.append(stack.pop() + ' - ')
    stack.append(0)
    while True:
        heap['count'] = stack.pop()
        heap['str'] = stack.pop()
        
        if len(stack) == 0:
            stack.append(heap['str'])
            stack.append(heap['count'])
            if stack.pop() < 100:
                print(stack.pop())
            break

        stack.append(str(stack.pop()))
        stack.append(heap['str'])
        stack.append(heap['count'])
        if stack.pop() == 0:
            stack.append(stack.pop() + stack.pop())
        else:
            stack.append(stack.pop() + ', '+ stack.pop())
        stack.append(heap['count'])
        stack.append(stack.pop()+1)


    stack.append(heap['dict'])
    stack.append(heap['keys'])
    stack.append(heap['i'])
    stack.append(stack.pop()+1)


del heap['i']
del heap['j']
del heap['keys']
del heap['dict']
del heap['pages']
del heap['str']
del heap['count']
del heap['key']