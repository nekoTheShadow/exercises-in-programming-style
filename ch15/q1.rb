class WordFrequencyFramework
  def initialize()
    @load_event_handlers = []
    @dowork_event_handlers = []
    @end_event_handlers = []
  end

  def register_for_load_event(handler) = @load_event_handlers << handler
  def register_for_dowork_event(handler) = @dowork_event_handlers << handler
  def register_for_end_event(handler) = @end_event_handlers << handler
  
  def run(path_to_file)
    @load_event_handlers.each{|h| h[path_to_file]}
    @dowork_event_handlers.each{|h| h[]}
    @end_event_handlers.each{|h| h[]}
  end
end

class DataStorage
  def initialize(wfapp, stop_word_filter)
    @data = ''
    @stop_word_filter = stop_word_filter
    @word_event_handlers = []
    wfapp.register_for_load_event(proc{|path_to_file| self.load(path_to_file)})
    wfapp.register_for_dowork_event(proc{self.produce_words})
  end

  def load(path_to_file)
    @data = IO.read(path_to_file).gsub(/[\W_]+/, ' ').downcase
  end

  def produce_words()
    @data.split.each do |w|
      if !@stop_word_filter.is_stop_word(w)
        @word_event_handlers.each{|h| h[w]}
      end
    end
  end

  def register_for_word_event(handler) = @word_event_handlers << handler
end

class StopWordFilter
  def initialize(wfapp)
    @stop_words = []
    wfapp.register_for_load_event(proc{|path_to_file| self.load(path_to_file)})
  end

  def load(ignore)
    @stop_words.concat(IO.read('../stop_words.txt').split(','))
    @stop_words.concat(('a'..'z').to_a)
  end

  def is_stop_word(word) = @stop_words.include?(word)
end

class WordFrequencyCounter
  def initialize(wfapp, data_storage)
    @word_freqs = {}
    data_storage.register_for_word_event(proc{|word| self.increment_count(word)})
    wfapp.register_for_end_event(proc{self.print_freqs})
  end

  def increment_count(word)
    @word_freqs[word] = 0 unless @word_freqs.include?(word)
    @word_freqs[word] += 1
  end

  def print_freqs()
    word_freqs = @word_freqs.sort_by{|k, v| -v}
    word_freqs.take(25).each{|w, c| puts "#{w} #{c}"}
  end
end

wfapp = WordFrequencyFramework.new()
stop_word_filter = StopWordFilter.new(wfapp)
data_storage = DataStorage.new(wfapp, stop_word_filter)
word_freq_counter = WordFrequencyCounter.new(wfapp, data_storage)
wfapp.run(ARGV[0])
