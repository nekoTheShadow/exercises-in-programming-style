import queue
import re
import sys
import threading


class ActiveWFObject(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = str(type(self))
        self.queue = queue.Queue()
        self._stop_me = False
        self.start()

    def run(self):
        while not self._stop_me:
            message = self.queue.get()
            self._dispatch(message)
            if message[0] == 'die':
                self._stop_me = True


def send(receiver, message):
    receiver.queue.put(message)



class Targets(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'run':
            self._run()
    
    def _init(self, message):
        self._words = message[0]

    def _run(self):
        with open('../target_words.txt') as f:
            targets = sorted(f.read().split(','))
            for target in targets:
                send(self._words, ['run', target])
        send(self._words, ['fin'])
        send(self, ['die'])


class Words(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'run':
            self._run(message[1:])
        elif message[0] == 'fin':
            self._fin()
    
    def _init(self, message):
        self._app = message[0]
        self._words = []
        filename = message[1]
        with open(filename) as f:
            for i, line in enumerate(f):
                for word in re.findall('\w+', line.lower()):
                    self._words.append((word, i//45+1))

    def _run(self, message):
        target = message[0]
        for i, (word, page) in enumerate(self._words):
            if word == target:
                result = ' '.join(self._words[i+j][0] for j in range(-2, 3)) + f' - {page}'
                send(self._app, ['run', result])

    def _fin(self):
        send(self._app, ['fin'])
        send(self, ['die'])


class App(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'run':
            self._run(message[1:])
        elif message[0] == 'fin':
            self._fin()
        
    def _run(self, message):
        print(message[0])
    
    def _fin(self):
        send(self, ['die'])


targets = Targets()
words = Words()
app = App()

send(targets, ['init', words])
send(words, ['init', app, sys.argv[1]])

send(targets, ['run'])

targets.join()
words.join()
app.join()