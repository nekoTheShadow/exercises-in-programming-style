import abc, re, sys, operator

class IDataStorage (metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def words(self):
        pass

class IWordFilter (metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(self, word):
        pass

class DataStorageManager(IDataStorage):
    def __init__(self, path_to_file):
        pattern = re.compile('\w+')
        self._data = []
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                self._data.extend((i//45+1, w) for w in pattern.findall(line.lower()))

    def words(self):
        return self._data
    
class WordFilter(IWordFilter):
    def __init__(self, data_storage_manager) -> None:
        self._data_storage_manager = data_storage_manager

    def find(self, target):
        result = []
        words = self._data_storage_manager.words()
        for i, (page, w) in enumerate(words):
            if w == target:
                result.append(tuple(words[i+j] for j in range(-2, 3)))
        return result


class TargetWords(IDataStorage):
    def __init__(self):
        with open('../target_words.txt') as f:
            self._words = f.read().split(',')
        self._words.sort()
    
    def words(self):
        return self._words

    
class WordFrequencyController:
    def __init__(self, path_to_file):
        self._storage = DataStorageManager(path_to_file)
        self._word_filter = WordFilter(self._storage)
        self._target_words = TargetWords()

    def run(self):
        for target in self._target_words.words():
            for result in self._word_filter.find(target):
                print(*map(operator.itemgetter(1), result), '-', result[2][0])

WordFrequencyController(sys.argv[1]).run()
