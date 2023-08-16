import re, operator, collections

class WordFrequenciesModel:
    def __init__(self):
        self.stopwords = set(open('../stop_words.txt').read().split(','))
        self.handler = None

    def update(self, path_to_file):
        words = re.findall('[a-z]{2,}', open(path_to_file).read().lower())
        freqs = collections.Counter(w for w in words if w not in self.stopwords)
        self.handler(freqs)

    def register_for_update_event(self, handler):
        self.handler = handler


class WordFrequenciesView:
    def render(self, freqs):
        sorted_freqs = sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)
        for (w, c) in sorted_freqs[0:25]:
            print(w, '-', c)

class WordFrequencyController:
    def __init__(self):
        self.handler = None

    def register_for_change_event(self, handler):
        self.handler = handler

    def change(self, path_to_file):
        self.handler(path_to_file)

    def run(self):
        while True:
            path_to_file = input('Next file: ').strip()
            self.change(path_to_file)

m = WordFrequenciesModel()
v = WordFrequenciesView()
c = WordFrequencyController()
m.register_for_update_event(lambda freqs : v.render(freqs))
c.register_for_change_event(lambda path_to_file : m.update(path_to_file))
c.run()