import re
import sys

class FileReader():
    def __init__(self, path_to_file):
        self.words = []
        with open(path_to_file) as f:
            for lineno, line in enumerate(f):
                for word in re.findall("[\w]+", line.lower()):
                    self.words.append((word, lineno//45+1))

    def find(self, target):
        results = []
        for i in range(len(self.words)):
            word, pageno = self.words[i]
            if word == target:
                results.append((pageno, self.words[i-2][0], self.words[i-1][0], self.words[i][0], self.words[i+1][0], self.words[i+2][0]))
        return results
    
class TargetWords():
    def __init__(self):
        self.target_words = []
        with open('../target_words.txt') as f:
            self.target_words.extend(f.read().split(','))
        self.target_words.sort()

    def words(self):
        return self.target_words

class App():
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def run(self):
        file_reader = FileReader(self.path_to_file)
        target_words = TargetWords()
        for target in target_words.words():
            for result in file_reader.find(target):
                print(*result[1:], '-', result[0])


App(sys.argv[1]).run()