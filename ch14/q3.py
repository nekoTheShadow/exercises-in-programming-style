import abc, sys, re, operator, string
from typing import Any

class IDataStorage (metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def words(self):
        pass

class IStopWordFilter (metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_stop_word(self, word):
        pass

class IWordFrequencyCounter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def increment_count(self, word):
        pass

    @abc.abstractmethod
    def sorted(self):
        pass

class AcceptTypes:
    def __init__(self, *args):
        self._args = args
    
    def __call__(self, f):
        def wrapped_f(*args):
            for i in range(len(self._args)):
                if self._args[i] == 'primitive' and type(args[i+1]) in (str, int, float, bool):
                    continue
                if not isinstance(args[i+1], globals()[self._args[i]]):
                    raise TypeError('Wrong type')
            return f(*args)
        return wrapped_f

class DataStorageManager:
    _data = ''

    @AcceptTypes('primitive')
    def __init__(self, path_to_file):
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()
        self._data = ''.join(self._data).split()

    def words(self):
        return self._data

class StopWordManager:
    _stop_words = []
    def __init__(self):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    @AcceptTypes('primitive')
    def is_stop_word(self, word):
        return word in self._stop_words

class WordFrequencyManager:
    _word_freqs = {}

    @AcceptTypes('primitive')
    def increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def sorted(self):
        return sorted(self._word_freqs.items(), key=operator.itemgetter(1), reverse=True)


IDataStorage.register(subclass=DataStorageManager)
IStopWordFilter.register(subclass=StopWordManager)
IWordFrequencyCounter.register(subclass=WordFrequencyManager)

class WordFrequencyController:
    @AcceptTypes('primitive')
    def __init__(self, path_to_file):
        self._storage = DataStorageManager(path_to_file)
        self._stop_word_manager = StopWordManager()
        self._word_freq_counter = WordFrequencyManager()

    def run(self):
        for w in self._storage.words():
            if not self._stop_word_manager.is_stop_word(w):
                self._word_freq_counter.increment_count(w)

        word_freqs = self._word_freq_counter.sorted()
        for (w, c) in word_freqs[0:25]:
            print(w, '-', c)

# 型チェックに失敗する
WordFrequencyController([]).run()

# 型チェックに成功する
WordFrequencyController(sys.argv[1]).run()
