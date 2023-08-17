import re

class Model():
    def __init__(self):
        with open('../stop_words.txt') as f:
            self.stop_words = set(f.read().split(','))

    def update(self, path_to_file):
        box = {}
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                page = i//45+1
                for word in re.findall(r'[a-z]{2,}', line.lower()):
                    if word in self.stop_words:
                        continue
                    if word not in box:
                        box[word] = []
                    if page not in box[word]:
                        box[word].append(page)
        self.box = box


class View():
    def __init__(self, model):
        self.model = model
    
    def render(self):
        for word, pages in sorted(self.model.box.items()):
            if len(pages) < 100:
                print(word, '-', ', '.join(map(str, pages)))


class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        while True:
            path_to_file = input('Next File: ')
            self.model.update(path_to_file)
            self.view.render()


m = Model()
v = View(m)
c = Controller(m, v)
c.run()