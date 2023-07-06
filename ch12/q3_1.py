import re
import string
import sys

class FileReader():
    def dispatch(self, message):
        if message[0] == 'read':
            return self._read(message[1])
        else:
            raise Exception("Message not understood " + message[0])

    def _read(self, path_to_file):
        self.words = []
        with open(path_to_file) as f:
            for lineno, line in enumerate(f):
                for word in re.findall("[a-z]{2,}", line.lower()):
                    self.words.append((word, lineno//45+1))
        return self.words
    

class StopWords():
    def dispatch(self, message):
        if message[0] == 'init':
            return self._init()
        if message[0] == 'is_stop_word':
            return self._is_stop_word(message[1])
        else:
            raise Exception("Message not understood " + message[0])

    def _init(self):
        self.stop_words = []
        with open('../stop_words.txt') as f:
            self.stop_words.extend(f.read().split(','))
        self.stop_words.extend(string.ascii_lowercase)

    def _is_stop_word(self, word):
        return word in self.stop_words
    

class Counter():
    def __init__(self):
        self.counter = {}

    def dispatch(self, message):
        if message[0] == 'add':
            return self._add(message[1], message[2])
        elif message[0] == 'pretty_print':
            return self._pretty_print()
        else:
            raise Exception("Message not understood " + message[0])
    
    def _add(self, word, pageno):
        if not word in self.counter:
            self.counter[word] = []
        if not word in self.counter[word]:
            self.counter[word].append(pageno)

    def _pretty_print(self):
        for word in sorted(self.counter):
            if len(self.counter[word]) < 100:
                print(word, '-', ', '.join(map(str, self.counter[word])))


class App():
    def dispatch(self, message):
        if message[0] == 'run':
            return self.run(message[1])
        else:
            raise Exception("Message not understood " + message[0])

    def run(self, path_to_file):
        file_reader = FileReader()
        stop_words = StopWords()
        counter = Counter()
        stop_words.dispatch(["init"])

        words = file_reader.dispatch(['read', path_to_file])
        for word, pageno in words:
            if not stop_words.dispatch(["is_stop_word", word]):
                counter.dispatch(["add", word, pageno])
        counter.dispatch(["pretty_print"])


App().dispatch(["run", sys.argv[1]])
