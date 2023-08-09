import sys, re, operator, string, threading, queue

class ActiveWFObject(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = str(type(self))
        self.queue = queue.Queue()
        self._stopMe = False
        self.start()

    def run(self):
        while not self._stopMe:
            message = self.queue.get()
            self._dispatch(message)
            if message[0] == 'die':
                self._stopMe = True

def send(receiver, message):
    receiver.queue.put(message)

class DataStorageManager(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'send_word_freqs':
            self._process_words(message[1:])
        else:
            send(self._stop_word_manager, message)
 
    def _init(self, message):
        path_to_file = message[0]
        self._stop_word_manager = message[1]
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def _process_words(self, message):
        # recipient = message[0]
        data_str = ''.join(self._data)
        words = data_str.split()
        for w in words:
            send(self._stop_word_manager, ['filter', w])
        send(self._stop_word_manager, ['top25'])

class StopWordManager(ActiveWFObject):
    def _dispatch(self, message):
        if message[0] == 'init':
            self._init(message[1:])
        elif message[0] == 'filter':
            return self._filter(message[1:])
        else:
            send(self._word_freqs_manager, message)
 
    def _init(self, message):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))
        self._word_freqs_manager = message[0]

    def _filter(self, message):
        word = message[0]
        if word not in self._stop_words:
            send(self._word_freqs_manager, ['word', word])

class WordFrequencyManager(ActiveWFObject):
    _word_freqs = {}

    def _dispatch(self, message):
        if message[0] == 'word':
            self._increment_count(message[1:])
        elif message[0] == 'top25':
            self._top25(message[1:])
 
    def _increment_count(self, message):
        word = message[0]
        if word in self._word_freqs:
            self._word_freqs[word] += 1 
        else: 
            self._word_freqs[word] = 1

    def _top25(self, message):
        freqs_sorted = sorted(self._word_freqs.items(), key=operator.itemgetter(1), reverse=True)
        for (w, f) in freqs_sorted[0:25]:
            print(w, '-', f)


word_freq_manager = WordFrequencyManager()
stop_word_manager = StopWordManager()
send(stop_word_manager, ['init', word_freq_manager])
storage_manager = DataStorageManager()
send(storage_manager, ['init', sys.argv[1], stop_word_manager])
send(storage_manager, ['send_word_freqs'])
send(storage_manager, ['die'])
word_freq_manager.join()
stop_word_manager.join()
storage_manager.join()
