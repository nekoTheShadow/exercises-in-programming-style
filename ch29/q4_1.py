import collections
import queue
import re
import sys
import threading
import string


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



class Words(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'start':
            self._start(message[1:])
    
    def _init(self, message):
        self._filter = message[0]

    def _start(self, message):
        filename = message[0]
        with open(filename) as f:
            for i, line in enumerate(f):
                for word in re.findall('[a-z]+', line.lower()):
                    send(self._filter, ['start', word, i//45+1])
        send(self._filter, ['fin'])
        send(self, ['die'])

    
class Filter(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'start':
            self._start(message[1:])
        elif message[0] == 'fin':
            self._fin()
    
    def _init(self, message):
        self._box = message[0]
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(string.ascii_lowercase)
    
    def _start(self, message):
        word = message[0]
        page = message[1]
        if word not in self._stop_words:
            send(self._box, ['start', word, page])

    def _fin(self):
        send(self._box, ['fin'])
        send(self, ['die'])


class Box(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init()
        elif message[0] == 'start':
            self._start(message[1:])
        elif message[0] == 'fin':
            self._fin()
        
    def _init(self):
        self._groups = collections.defaultdict(list)
    
    def _start(self, message):
        word = message[0]
        page = message[1]
        if page not in self._groups[word]:
            self._groups[word].append(page)
    
    def _fin(self):
        for w, pages in sorted(self._groups.items()):
            if len(pages) < 100:
                print(w, '-', ', '.join(map(str, pages)))
        send(self, ['die'])


words = Words()
filter = Filter()
box = Box()

send(words, ['init', filter])
send(filter, ['init', box])
send(box, ['init'])
send(words, ['start', sys.argv[1]])

words.join()
filter.join()
box.join()