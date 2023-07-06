import sys, re, operator, string

class TFExercise():
    def dispatch(self, message):
        if message[0] == 'info':
            return self._info(message[1])
        else:
            raise Exception("Message not understood " + message[0])

    def _info(self, other):
        return other.__class__.__name__


class DataStorageManager():
    _data = ''
    _parent = TFExercise()

    def dispatch(self, message):
        if message[0] == 'init':
            return self._init(message[1])
        elif message[0] == 'words':
            return self._words()
        elif message[0] == 'info':
            return self._parent.dispatch(['info', self])
        else:
            raise Exception("Message not understood " + message[0])
 
    def _init(self, path_to_file):
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def _words(self):
        data_str = ''.join(self._data)
        return data_str.split()


class StopWordManager():
    _stop_words = []
    _parent = TFExercise()

    def dispatch(self, message):
        if message[0] == 'init':
            return self._init()
        elif message[0] == 'is_stop_word':
            return self._is_stop_word(message[1])
        elif message[0] == 'info':
            return self._parent.dispatch(['info', self])
        else:
            raise Exception("Message not understood " + message[0])
 
    def _init(self):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    def _is_stop_word(self, word):
        return word in self._stop_words


class WordFrequencyManager():
    _word_freqs = {}
    _parent = TFExercise()

    def dispatch(self, message):
        if message[0] == 'increment_count':
            return self._increment_count(message[1])
        elif message[0] == 'sorted':
            return self._sorted()
        elif message[0] == 'info':
            return self._parent.dispatch(['info', self])
        else:
            raise Exception("Message not understood " + message[0])
 
    def _increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def _sorted(self):
        return sorted(self._word_freqs.items(), key=operator.itemgetter(1), reverse=True)


class WordFrequencyController():
    _parent = TFExercise()
    
    def dispatch(self, message):
        if message[0] == 'init':
            return self._init(message[1])
        elif message[0] == 'run':
            return self._run()
        elif message[0] == 'info':
            return self._parent.dispatch(['info', self])
        else:
            raise Exception("Message not understood " + message[0])
 
    def _init(self, path_to_file):
        self._storage_manager = DataStorageManager()
        self._stop_word_manager = StopWordManager()
        self._word_freq_manager = WordFrequencyManager()
        self._storage_manager.dispatch(['init', path_to_file])
        self._stop_word_manager.dispatch(['init'])

    def _run(self):
        print(self._storage_manager.dispatch(['info']))
        print(self._stop_word_manager.dispatch(['info']))
        print(self._word_freq_manager.dispatch(['info']))

        for w in self._storage_manager.dispatch(['words']):
            if not self._stop_word_manager.dispatch(['is_stop_word', w]):
                self._word_freq_manager.dispatch(['increment_count', w])

        word_freqs = self._word_freq_manager.dispatch(['sorted'])
        for (w, c) in word_freqs[0:25]:
            print(w, '-', c)


wfcontroller = WordFrequencyController()
wfcontroller.dispatch(['init', sys.argv[1]])
wfcontroller.dispatch(['run'])
