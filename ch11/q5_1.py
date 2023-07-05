import re
import string
import sys

class Word():
    def __init__(self, word, page):
        self.word = word
        self.page = page

    def get_word(self):
        return self.word
    
    def get_page(self):
        return self.page


class FileReader():
    def __init__(self, path_to_file):
        self.words = []
        with open(path_to_file) as f:
            for lineno, line in enumerate(f):
                for word in re.findall("[a-z]{2,}", line.lower()):
                    self.words.append(Word(word, lineno//45+1))
    
    def get_words(self):
        return self.words
    

class StopWords():
    def __init__(self):
        self.stop_words = []
        with open('../stop_words.txt') as f:
            self.stop_words.extend(f.read().split(','))
        self.stop_words.extend(string.ascii_lowercase)

    def is_stop_word(self, word):
        return word in self.stop_words
    

class Counter():
    def __init__(self):
        self.counter = {}
    
    def add(self, word):
        if not word.get_word() in self.counter:
            self.counter[word.get_word()] = []
        if not word.get_page() in self.counter[word.get_word()]:
            self.counter[word.get_word()].append(word.get_page())

    def pretty_print(self):
        for word in sorted(self.counter):
            if len(self.counter[word]) < 100:
                print(word, '-', ', '.join(map(str, self.counter[word])))

class App():
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def run(self):
        words = FileReader(self.path_to_file).get_words()
        stop_words = StopWords()
        counter = Counter()
        for word in words:
            if not stop_words.is_stop_word(word):
                counter.add(word)
        counter.pretty_print()

    

App(sys.argv[1]).run()
