import re, sys, operator

class WordFrequencyFramework:
    _load_event_handlers = []
    _dowork_event_handlers = []
    _end_event_handlers = []

    def register_for_load_event(self, handler):
        self._load_event_handlers.append(handler)

    def register_for_dowork_event(self, handler):
        self._dowork_event_handlers.append(handler)

    def register_for_end_event(self, handler):
        self._end_event_handlers.append(handler)
    
    def run(self, path_to_file):
        for h in self._load_event_handlers:
            h(path_to_file)
        for h in self._dowork_event_handlers:
            h()
        for h in self._end_event_handlers:
            h()

class DataStorage:
    def __init__(self, wfapp, grep_filter):
        self._words = []
        self._word_event_handlers = []
        self._grep_filter = grep_filter
        wfapp.register_for_load_event(self.__load)
        wfapp.register_for_dowork_event(self.__produce_words)
    
    def __load(self, path_to_file, ):
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                for word in re.findall(r'\w+', line.lower()):
                    self._words.append((word, i//45+1))
    
    def __produce_words(self):
        for i, (word, page) in enumerate(self._words):
            if self._grep_filter.grep(word):
                for h in self._word_event_handlers:
                    h(self._words[i-2][0], self._words[i-1][0], self._words[i][0], self._words[i+1][0], self._words[i+2][0], page)

    def register_for_word_event(self, handler):
        self._word_event_handlers.append(handler)


class GrepFilter:
    def __init__(self, wfapp):
        self._target_words = []
        wfapp.register_for_load_event(self.__load)

    def __load(self, ignore):
        with open('../target_words.txt') as f:
            self._target_words = f.read().split(',')

    def grep(self, word):
        return word in self._target_words
    

class GrepResult:
    def __init__(self, wfapp, data_storage):
        self._results = []
        data_storage.register_for_word_event(self.__increment_count)
        wfapp.register_for_end_event(self.__print_freqs)

    def __increment_count(self, w1, w2, w3, w4, w5, page):
        self._results.append((w1, w2, w3, w4, w5, page))

    def __print_freqs(self):
        for w1, w2, w3, w4, w5, page in sorted(self._results, key=lambda r: (r[2], r[5])):
            print(w1, w2, w3, w4, w5, '-', page)



wfapp = WordFrequencyFramework()
grep_filter = GrepFilter(wfapp)
data_storage = DataStorage(wfapp, grep_filter)
grep_result = GrepResult(wfapp, data_storage)
wfapp.run(sys.argv[1])
