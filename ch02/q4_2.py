import sys, re

stack = []
heap = {}

heap["wps"] = None
heap["i"] = None
heap["lines"] = None
heap["words"] = None
heap["j"] = None

stack.append(open(sys.argv[1]))
stack.append(list(stack.pop()))
stack.append(0)
stack.append([])

while True:
    heap["wps"] = stack.pop()
    heap["i"] = stack.pop()
    heap["lines"] = stack.pop()

    stack.append(heap["lines"])
    stack.append(heap["i"])
    if stack.pop() == len(stack.pop()):
        break

    stack.append(heap["i"])
    stack.append(heap["lines"])
    stack.append(stack.pop()[stack.pop()])

    stack.append(re.compile(r"\w+"))
    stack.append(stack.pop().findall(stack.pop().lower()))
    heap["words"] = stack.pop()
    
    stack.append(0)
    while True:
        heap["j"] = stack.pop()

        stack.append(heap["words"])
        stack.append(heap["j"])
        if stack.pop() == len(stack.pop()):
            break

        stack.append(heap["i"])
        stack.append(stack.pop()//45+1)
        stack.append(heap["j"])
        stack.append(heap["words"])
        stack.append(heap["wps"])
        stack.pop().append((stack.pop()[stack.pop()], stack.pop()))

        stack.append(heap["j"])
        stack.append(stack.pop()+1)

    stack.append(heap["lines"])
    stack.append(heap["i"])
    stack.append(stack.pop()+1)
    stack.append(heap["wps"])

stack.append(heap["wps"])

del heap["wps"]
del heap["i"]
del heap["lines"]
del heap["words"]
del heap["j"]

stack.append(open('../target_words.txt'))
stack.append(stack.pop().read())
stack.append(stack.pop().split(','))
stack.append(list(sorted(stack.pop())))


heap["i"] = None
heap["target_words"] = None
heap["target_word"] = None
heap["wps"] = None
heap["wp"] = None
heap["j"] = None
heap["w"] = None
heap["p"] = None

stack.append(0)
while True:
    heap["i"] = stack.pop()
    heap["target_words"] = stack.pop()
    heap["wps"] = stack.pop()

    stack.append(heap["i"])
    stack.append(heap["target_words"])
    if len(stack.pop()) == stack.pop():
        break

    stack.append(heap["i"])
    stack.append(heap["target_words"])
    stack.append(stack.pop()[stack.pop()])
    heap["target_word"] = stack.pop()

    stack.append(0)
    while True:
        heap["j"] = stack.pop()

        stack.append(heap["j"])
        stack.append(heap["wps"])
        if len(stack.pop()) == stack.pop():
            break

        stack.append(heap["j"])
        stack.append(heap["wps"])
        
        stack.append(stack.pop()[stack.pop()])
        heap["wp"] = stack.pop()

        stack.append(heap["wp"])
        stack.append(stack.pop()[0])
        heap["w"] = stack.pop()
        stack.append(heap["wp"])
        stack.append(stack.pop()[1])
        heap["p"] = stack.pop()

        stack.append(heap["w"])
        stack.append(heap["target_word"])
        if stack.pop() == stack.pop():
            stack.append(heap["p"])

            stack.append(heap["j"])
            stack.append(stack.pop()+2)
            stack.append(heap["wps"])
            stack.append(stack.pop()[stack.pop()][0])

            stack.append(heap["j"])
            stack.append(stack.pop()+1)
            stack.append(heap["wps"])
            stack.append(stack.pop()[stack.pop()][0])

            stack.append(heap["j"])
            stack.append(stack.pop())
            stack.append(heap["wps"])
            stack.append(stack.pop()[stack.pop()][0])

            stack.append(heap["j"])
            stack.append(stack.pop()-1)
            stack.append(heap["wps"])
            stack.append(stack.pop()[stack.pop()][0])

            stack.append(heap["j"])
            stack.append(stack.pop()-2)
            stack.append(heap["wps"])
            stack.append(stack.pop()[stack.pop()][0])
            print(stack.pop(), stack.pop(), stack.pop(), stack.pop(), stack.pop(), "-", stack.pop())
            
        stack.append(heap["j"])
        stack.append(stack.pop()+1)
    
    stack.append(heap["wps"])
    stack.append(heap["target_words"])
    stack.append(heap["i"])
    stack.append(stack.pop()+1)

del heap["i"] 
del heap["target_words"] 
del heap["target_word"] 
del heap["wps"] 
del heap["wp"] 
del heap["j"] 
del heap["w"] 
del heap["p"] 