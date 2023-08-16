import re, operator, collections

class WordFrequenciesModel:
    stopwords = set(open('../stop_words.txt').read().split(','))
    def change(self, path_to_file):
        self.words = re.findall('[a-z]{2,}', open(path_to_file).read().lower())
        self.cur = 0
        self.freqs = collections.defaultdict(int)
        return self.update()

    def update(self):
        x = 0
        while self.cur < len(self.words) and x < 5000 :
            if self.words[self.cur] not in self.stopwords:
                self.freqs[self.words[self.cur]] += 1
                x += 1
            self.cur += 1
        return self.cur < len(self.words)

class WordFrequenciesView:
    def __init__(self, model):
        self._model = model

    def render(self):
        sorted_freqs = sorted(self._model.freqs.items(), key=operator.itemgetter(1), reverse=True)
        for (w, c) in sorted_freqs[0:25]:
            print(w, '-', c)

class WordFrequencyController:
    def __init__(self, model, view):
        self._model, self._view = model, view

    def run(self):
        while True:
            filename = input('Next file: ').strip()
            has_next = self._model.change(filename)
            self._view.render()
            while has_next:
                yn = input('More?[y/n]')
                if yn == 'y':
                    has_next = self._model.update()
                    self._view.render()
                else:
                    has_next = False

m = WordFrequenciesModel()
v = WordFrequenciesView(m)
c = WordFrequencyController(m, v)
c.run()