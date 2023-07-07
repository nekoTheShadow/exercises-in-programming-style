import re
import sys

class FileReader():
    def dispatch(self, message):
        if message[0] == 'init':
            return self._init(message[1])
        elif message[0] == 'find':
            return self._find(message[1])
        else:
            raise Exception("Message not understood " + message[0])

    def _init(self, path_to_file):
        self.words = []
        with open(path_to_file) as f:
            for lineno, line in enumerate(f):
                for word in re.findall("[a-z]{2,}", line.lower()):
                    self.words.append((word, lineno//45+1))

    def _find(self, target):
        results = []
        for i in range(len(self.words)):
            word, pageno = self.words[i]
            if word == target:
                results.append((pageno, self.words[i-2][0], self.words[i-1][0], self.words[i][0], self.words[i+1][0], self.words[i+2][0]))
        return results

class TargetWords():
    def dispatch(self, message):
        if message[0] == 'init':
            return self._init()
        elif message[0] == 'words':
            return self._words()
        else:
            raise Exception("Message not understood " + message[0])
        
    def _init(self):
        self.target_words = []
        with open('../target_words.txt') as f:
            self.target_words.extend(f.read().split(','))
        self.target_words.sort()

    def _words(self):
        return self.target_words

        

class App():
    def dispatch(self, message):
        if message[0] == 'run':
            return self._run(message[1])
        else:
            raise Exception("Message not understood " + message[0])

    def _run(self, path_to_file):
        file_reader = FileReader()
        target_words = TargetWords()
        file_reader.dispatch(["init", path_to_file])
        target_words.dispatch(["init"])
        for target in target_words.dispatch(['words']):
            for result in file_reader.dispatch(["find", target]):
                print(*result[1:], '-', result[0])


App().dispatch(["run", sys.argv[1]])