import sys, re

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
        self._event_manager.subscribe('load', self.load)
        self._event_manager.subscribe('grep', self.grep)

    def load(self, event):
        path_to_file = event[1]
        self._words = []
        with open(path_to_file) as f:
            for i, line in enumerate(f):
                for word in re.findall(r'\w+', line.lower()):
                    self._words.append((word, i//45+1))
    
    def grep(self, event):
        target = event[1]
        for i, (word, page) in enumerate(self._words):
            if word == target:
                self._event_manager.publish(['grep_result', self._words[i-2][0], self._words[i-1][0], self._words[i][0], self._words[i+1][0], self._words[i+2][0], page])


class Application:
    def __init__(self, event_manager):
        self._results = []
        self._event_manager = event_manager
        self._event_manager.subscribe('run', self.run)
        self._event_manager.subscribe('grep_result', self.grep_result)
        self._event_manager.subscribe('print', self.print)
    
    def run(self, event):
        self._event_manager.publish(['load', sys.argv[1]])
        with open('../target_words.txt') as f:
            for target in f.read().split(','):
                self._event_manager.publish(['grep', target])
        self._event_manager.publish(['print', None])
    
    def grep_result(self, event):
        w1 = event[1]
        w2 = event[2]
        w3 = event[3]
        w4 = event[4]
        w5 = event[5]
        page = event[6]
        self._results.append((w3, page, f'{w1} {w2} {w3} {w4} {w5} - {page}'))

    def print(self, event):
        for _, _, result in sorted(self._results):
             print(result)

em = EventManager()
DataStorage(em)
Application(em)
em.publish(('run', sys.argv[1]))