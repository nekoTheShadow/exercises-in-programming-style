import re, collections, sys, operator

class FileReader():
    def __init__(self, path_to_file):
        self.fp = open(path_to_file)
        self.words = collections.deque()
    
    def next_word(self):
        return self.words.popleft()
    
    def has_next_word(self):
        if len(self.words) == 0:
            while True:
                line = self.fp.readline()
                if line == "":
                    break
                next_words = re.findall("\w+", line.lower())
                if len(next_words) > 0:
                    self.words.extend(next_words)
                    break
        return len(self.words) > 0
    
    def close(self):
        self.fp.close()


class StopWords():
    def __init__(self):
        self.stop_words = set()
        fr = FileReader('../stop_words.txt')
        while fr.has_next_word():
            self.stop_words.add(fr.next_word())
        fr.close()

    def is_stop_word(self, word):
        return len(word) < 2 or word in self.stop_words


class WordCounter():
    def __init__(self):
        self.counter = collections.Counter()
    
    def add(self, word):
        self.counter[word] += 1

    def pretty_print(self, n):
        for w, c in sorted(self.counter.items(), key=operator.itemgetter(1), reverse=True):
            print(f'{w} - {c}')
            n -= 1
            if n == 0:
                break


class App():
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def run(self):
        stop_words = StopWords()
        word_counter = WordCounter()
        file_reader = FileReader(self.path_to_file)
        while file_reader.has_next_word():
            word = file_reader.next_word()
            if not stop_words.is_stop_word(word):
                word_counter.add(word)
        file_reader.close()
        word_counter.pretty_print(25)


App(sys.argv[1]).run()