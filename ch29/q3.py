import sys
import operator
import string
import threading
import queue

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


class Characters(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'run':
            self._run(message[1:])

    def _init(self, message):
        self._all_words = message[0]

    def _run(self, message):
        filename = message[0]
        for line in open(filename):
            for c in line:
                send(self._all_words, ['run', c])
        send(self._all_words, ['fin'])
        send(self, ['die'])


class AllWords(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'run':
            self._run(message[1:])
        elif message[0] == 'fin':
            self._fin() 

    def _init(self, message):
        self._non_stop_words = message[0]
        self._start_char = True
        self._word = ''

    def _run(self, message):
        c = message[0]
        if self._start_char:
            self._word = ''
            if c.isalnum():
                self._word = c.lower()
                self._start_char = False
        else:
            if c.isalnum():
                self._word += c.lower()
            else:
                self._start_char = True
                send(self._non_stop_words, ['run', self._word])

    def _fin(self):
        send(self._non_stop_words, ['fin'])
        send(self, ['die'])


class NonStopWords(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'run':
            self._run(message[1:])
        elif message[0] == 'fin':
            self._fin() 

    def _init(self, message):
        self._count_and_sort = message[0]
        self._stop_words = set(open('../stop_words.txt').read().strip('\n').split(',') + list(string.ascii_lowercase))
    
    def _run(self, message):
        w = message[0]
        if not w in self._stop_words:
            send(self._count_and_sort, ['run', w])

    def _fin(self):
        send(self._count_and_sort, ['fin'])
        send(self, ['die'])

class CountAndSort(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'run':
            self._run(message[1:])
        elif message[0] == 'fin':
            self._fin() 

    def _init(self, message):
        self._app = message[0]
        self._freqs = {}
        self._i = 1

    def _run(self, message):
        w = message[0]
        self._freqs[w] = 1 if w not in self._freqs else self._freqs[w]+1
        if self._i % 5000 == 0:
            send(self._app, ['run', sorted(self._freqs.items(), key=operator.itemgetter(1), reverse=True)])
        self._i += 1

    def _fin(self):
        send(self._app, ['run', sorted(self._freqs.items(), key=operator.itemgetter(1), reverse=True)])
        send(self._app, ['fin'])
        send(self, ['die'])

class App(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'run':
            self._run(message[1:])
        elif message[0] == 'fin':
             self._fin()

    def _run(self, message):
        word_freqs = message[0]
        print("-----------------------------")
        for (w, c) in word_freqs[0:25]:
            print(w, '-', c)

    def _fin(self):
        send(self, ['die'])



characters = Characters()
all_words = AllWords()
non_stop_words = NonStopWords()
count_and_sort = CountAndSort()
app = App()

send(characters, ['init', all_words])
send(all_words, ['init', non_stop_words])
send(non_stop_words, ['init', count_and_sort])
send(count_and_sort, ['init', app])

send(characters, ['run', sys.argv[1]])

characters.join()
all_words.join()
non_stop_words.join()
count_and_sort.join()
app.join()