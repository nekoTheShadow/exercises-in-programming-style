import abc, re, sys, string

class IDataStorage (metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def words(self):
        pass

class IStopWordFilter (metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_stop_word(self, word):
        pass

class IWordFrequencyManager(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, word, page):
        pass

    @abc.abstractmethod
    def sorted(self):
        pass

class DataStorageManager(IDataStorage):
    def __init__(self, path_to_file):
        pattern = re.compile('[\W_]+')
        self._data = []
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                self._data.extend((i//45+1, w) for w in pattern.sub(' ', line).lower().split())

    def words(self):
        return self._data
    
class StopWordManager(IStopWordFilter):
    _stop_words = []
    def __init__(self):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        return any(ch.isdigit() for ch in word) or word in self._stop_words
    
class WordFrequencyManager(IWordFrequencyManager):
    def __init__(self):
        self._word_freqs = {}

    def add(self, word, page):
        if word not in self._word_freqs:
            self._word_freqs[word] = []
        if page not in self._word_freqs[word]:
            self._word_freqs[word].append(page)

    def sorted(self):
        return sorted(self._word_freqs.items())
    
class WordFrequencyController:
    def __init__(self, path_to_file):
        self._storage = DataStorageManager(path_to_file)
        self._stop_word_manager = StopWordManager()
        self._word_freq_manager = WordFrequencyManager()

    def run(self):
        for page, w in self._storage.words():
            if not self._stop_word_manager.is_stop_word(w):
                self._word_freq_manager.add(w, page)

        for (w, pages) in self._word_freq_manager.sorted():
            if len(pages) < 100:
                print(w, '-', ', '.join(map(str, pages)))

WordFrequencyController(sys.argv[1]).run()

