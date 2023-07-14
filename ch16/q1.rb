class EventManager
  def initialize()
    @subscriptions = Hash.new{|h, k| h[k] = []}
  end

  def subscribe(event_type, handler)
    @subscriptions[event_type] << handler
  end

  def publish(event)
    event_type = event[0]
    @subscriptions[event].each{|h| h[event]}
  end
end

class DataStorage
  def initialize(event_manager)
    @event_manager = event_manager
    @event_manager.subscribe(:load, ->(){|event| self.load(event)})
    @event_manager.subscribe(:start, ->(){|event| self.produce_words(event)})
  end

  def load(event)
    path_to_file = event[1]
    @data = IO.read(path_to_file).gsub(/[\W_]+/, ' ').downcase
  end

  def produce_words(event)
    @data.split.each{|w| @event_manager.publish([:word, w])}
    @event_manager.publish([:eof, nil])
  end
end

class StopWordFilter
  def initialize(event_manager)
    @event_manager = event_manager
    @event_manager.subscribe(:load, ->(){|event| self.load(event)})
    @event_manager.subscribe(:word, ->(){|event| self.is_stop_word(event)})
  end

  def load(event)
    @stop_words = IO.read('../stop_words.txt').split(',')
    @stop_words.concat([*'a'..'z'])
  end

  def is_stop_word(event)
    word = event[1]
    @event_manager.publish([:valid_word, word]) if word not in @stop_words
  end
end

class WordFrequencyCounter
  def initialize(event_manager)
    @event_manager = event_manager
    @event_manager.subscribe(:valid_word, ->(){|event| self.increment_count(event)})
    @event_manager.subscribe(:print, ->(){|event| self.print_freqs(event)})
    @word_freqs = Hash.new{|h, k| h[k] = 0}
  end

  def increment_count(event)
    word = event[1]
    @word_freqs[word] += 1
  end

  def print_freqs(event)
    word_freqs = @word_freqs.sort_by{-_2}
    word_freqs.take(25).each{|w, c| puts "#{w} #{c}"}
  end
end

class WordFrequencyAppliction
  def initialize(event_manager)
    @event_manager = event_manager
    @event_manager.subscribe(:run, ->(){|event| self.run(event)})
    @event_manager.subscribe(:eof, ->(){|event| self.stop(event)})
  end

  def run(event)
    path_to_file = event[1]
    @event_manager.publish([:load, path_to_file])
    @event_manager.publish([:start, nil])
  end

  def stop(event)
    @event_manager.publish([:print, nil])
  end
end

em = EventManager.new
DataStorage.new(em)
StopWordFilter.new(em)
WordFrequencyCounter.new(em)
WordFrequencyAppliction.new(em)
em.publish([:run, ARGV[1]])