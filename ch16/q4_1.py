import sys, re, string, collections

class EventManager:
    def __init__(self):
        self._subscriptions = {}

    def subscribe(self, event_type, handler):
        if event_type in self._subscriptions:
            self._subscriptions[event_type].append(handler)
        else:
            self._subscriptions[event_type] = [handler]

    def publish(self, event):
        event_type = event[0]
        if event_type in self._subscriptions:
            for h in self._subscriptions[event_type]:
                h(event)


class DataStorage:
    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.subscribe('start', self.produce_words)

    def produce_words(self, event):
        path_to_file = event[1]
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                for word in re.findall(r'[a-z]+', line.lower()):
                    self._event_manager.publish(('word', word, i//45+1))
        self._event_manager.publish(('eof', None))


class StopWordFilter:
    def __init__(self, event_manager):
        self._stop_words = []
        self._event_manager = event_manager
        self._event_manager.subscribe('load', self.load)
        self._event_manager.subscribe('word', self.is_stop_word)

    def load(self, event):
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, event):
        word = event[1]
        page = event[2]
        if word not in self._stop_words:
            self._event_manager.publish(('valid_word', word, page))


class Words:
    def __init__(self, event_manager):
        self._words = collections.defaultdict(set)
        self._event_manager = event_manager
        self._event_manager.subscribe('valid_word', self.add)
        self._event_manager.subscribe('print', self.print)

    def add(self, event):
        word = event[1]
        page = event[2]
        self._words[word].add(page)

    def print(self, event):
        for word, pages in sorted(self._words.items()):
            if len(pages) < 100:
                print(word, '-', ', '.join(map(str, sorted(pages))))


class Application:
    def __init__(self, event_manager):
        self._event_manager = event_manager
        self._event_manager.subscribe('run', self.run)
        self._event_manager.subscribe('eof', self.stop)

    def run(self, event):
        path_to_file = event[1]
        self._event_manager.publish(('start', path_to_file))

    def stop(self, event):
        self._event_manager.publish(('print', None))



em = EventManager()
DataStorage(em)
StopWordFilter(em)
Words(em)
Application(em)
em.publish(('run', sys.argv[1]))