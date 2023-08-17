import operator
import queue
import string
import threading
import re
import copy
import sys
import util


def send(receiver, message):
    receiver.queue.put(message)

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


class WordsCounter(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'count':
            self._count()

    def _init(self, message):
        self.controller = message[0]
        self.file = open(message[1])
        self.stopwords = set(open('../stop_words.txt').read().split(',')  + list(string.ascii_lowercase))
        self.freqs = {}

    def _count(self):
        def read_word():
            for line in self.file:
                for word in re.findall('[a-z]{2,}', line.lower()):
                    yield word
        
        x = 0
        for word in read_word():
            if word in self.stopwords:
                continue
            if word in self.freqs:
                self.freqs[word] += 1
            else:
                self.freqs[word] = 1
            x += 1
            if x == 100:
                break
        if x == 0:
            send(self.controller, ['ng'])
        else:
            send(self.controller, ['ok', copy.deepcopy(self.freqs)])


class FreqObserver(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'update_display':
            self._update_display(message[1:])

    def _update_display(self, message):
        freqs = message[0]
        data_str = ""
        for (w, c) in sorted(freqs.items(), key=operator.itemgetter(1), reverse=True)[:25]:
            data_str += f'{w} - {c}\n'
        util.cls()
        print(data_str)
        sys.stdout.flush()



class App(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'run':
            self._run(message[1:])
        elif message[0] == 'ok':
            self._ok(message[1:])
        elif message[0] == 'ng':
            self._ng()

    def _ng(self):
        send(self.model, ['die'])
        send(self.view, ['die'])
        send(self, ['die'])
    
    def _ok(self, message):
        freqs = message[0]
        send(self.view, ['update_display', freqs])
        if util.get_input():
            send(self.model, ['count'])

    def _run(self, message):
        print("Press space bar to fetch words from the file one by one")
        print("Press ESC to switch to automatic mode")
        self.model = message[0]
        self.view = message[1]
        send(self.model, ['init', self, sys.argv[1]])
        if util.get_input():
            send(self.model, ['count'])


view = FreqObserver()
model = WordsCounter()
controller = App()
send(controller, ['run', model, view])

view.join()
model.join()
controller.join()