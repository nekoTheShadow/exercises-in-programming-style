import re, sys

class Model():
    def __init__(self, path_to_file):
        self.words = []
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                page = i//45+1
                for word in re.sub(r'[\W_]+', ' ', line.lower()).split():
                    self.words.append((word, page))

    def grep(self, target):
        self.results = []
        for i, (word, page) in enumerate(self.words):
            if word == target:
                self.results.append((page, *(self.words[i+j][0] for j in range(-2, 3))))


class View():
    def __init__(self, model):
        self.model = model
    
    def render(self):
        for result in self.model.results:
            print(*result[1:], '-', result[0])


class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        with open('../target_words.txt') as f:
            for target in sorted( f.read().split(',')):
                self.model.grep(target)
                self.view.render()

m = Model(sys.argv[1])
v = View(m)
c = Controller(m, v)
c.run()