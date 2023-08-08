import operator
import string
import sys


class Characters(object):
    def __init__(self, filename):
        self.f = open(filename)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        c = self.f.read(1)
        if c == "":
            raise StopIteration()
        return c


class AllWords(object):
    def __init__(self, filename):
        self.characters = Characters(filename)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        start_char = True
        for c in self.characters:
            if start_char == True:
                word = ''
                if c.isalnum():
                    word = c.lower()
                    start_char = False
                else:
                    pass
            else:
                if c.isalnum():
                    word += c.lower()
                else:
                    start_char = True
                    return word
        raise StopIteration()


class NonStopWords(object):
    def __init__(self, filename):
        self.stop_words = set(open('../stop_words.txt').read().strip('\n').split(',') + list(string.ascii_lowercase))
        self.all_words = AllWords(filename)
    
    def __iter__(self):
        return self

    def __next__(self):
        for word in self.all_words:
            if word not in self.stop_words:
                return word
        raise StopIteration()
    

class CountAndSort(object):
    def __init__(self, filename):
        self.freqs = {}
        self.i = 1
        self.non_stop_words = NonStopWords(filename)
        self.finished = False

    def __iter__(self):
        return self

    def __next__(self):
        for w in self.non_stop_words:
            self.freqs[w] = 1 if w not in self.freqs else self.freqs[w]+1
            if self.i % 5000 == 0:
                return sorted(self.freqs.items(), key=operator.itemgetter(1), reverse=True)
            self.i = self.i+1
        
        if self.finished:
            raise StopIteration()
        else:
            self.finished = True
            return sorted(self.freqs.items(), key=operator.itemgetter(1), reverse=True)


for word_freqs in CountAndSort(sys.argv[1]):
    print("-----------------------------")
    for (w, c) in word_freqs[0:25]:
        print(w, '-', c)
