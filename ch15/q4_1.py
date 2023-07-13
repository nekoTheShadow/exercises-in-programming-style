import re, string, collections, sys

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
    def __init__(self, wfapp, stop_word_filter):
        self._words = []
        self._word_event_handlers = []
        self._stop_word_filter = stop_word_filter
        wfapp.register_for_load_event(self.__load)
        wfapp.register_for_dowork_event(self.__produce_words)
    
    def __load(self, path_to_file, ):
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                for word in re.findall(r'[a-z]+', line.lower()):
                    self._words.append((word, i//45+1))
    
    def __produce_words(self):
        for word, page in self._words:
            if not self._stop_word_filter.is_stop_word(word):
                for h in self._word_event_handlers:
                    h(word, page)

    def register_for_word_event(self, handler):
        self._word_event_handlers.append(handler)


class StopWordFilter:
    def __init__(self, wfapp):
        self._stop_words = []
        wfapp.register_for_load_event(self.__load)

    def __load(self, ignore):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        return word in self._stop_words
    

class PageDict:
    def __init__(self, wfapp, data_storage):
        self._dict = collections.defaultdict(set)
        data_storage.register_for_word_event(self.__increment_count)
        wfapp.register_for_end_event(self.__print_freqs)

    def __increment_count(self, word, page):
        self._dict[word].add(page)

    def __print_freqs(self):
        for word, pages in sorted(self._dict.items()):
            if len(pages) < 100:
                print(word, '-', ', '.join(map(str, sorted(pages))))



wfapp = WordFrequencyFramework()
stop_word_filter = StopWordFilter(wfapp)
data_storage = DataStorage(wfapp, stop_word_filter)
page_dict = PageDict(wfapp, data_storage)
wfapp.run(sys.argv[1])
