require 'thread'

class ActiveWFObject
  def initialize()
    @queue = Queue.new
    @stop_me = false
    @thread = Thread.new do
      until @stop_me
        message = @queue.shift
        dispatch(message)
        @stop_me = true if message[0] == :die
      end
    end
  end

  def join
    @thread.join
  end

  attr_accessor :queue, :stop_me
end

def send(receiver, message)
    receiver.queue << message
end

class DataStorageManager < ActiveWFObject
  def dispatch(message)
    if message[0] == :init
      init(message[1..])
    elsif message[0] == :send_word_freqs
      process_words(message[1..])
    else
      send(@stop_word_manager, message)
    end
  end

  def init(message)
    path_to_file = message[0]
    @stop_word_manager = message[1]
    @data = IO.read(path_to_file).gsub(/[\W_]+/, ' ').downcase
  end

  def process_words(message)
    recipient = message[0]
    words = @data.split
    words.each{|w| send(@stop_word_manager, [:filter, w])}
    send(@stop_word_manager, [:top25, recipient])
  end
end

class StopWordManager < ActiveWFObject
  def dispatch(message)
    if message[0] == :init
      init(message[1..])
    elsif message[0] == :filter
      filter(message[1..])
    else
      send(@word_freqs_manager, message)
    end
  end

  def init(message)
    @stop_words = IO.read('../stop_words.txt').split(',')
    @stop_words.concat(('a'..'z').to_a)
    @word_freqs_manager = message[0]
  end

  def filter(message)
    word = message[0]
    send(@word_freqs_manager, [:word, word]) unless @stop_words.include?(word)
  end
end

class WordFrequencyManager < ActiveWFObject
  def dispatch(message)
    @word_freqs ||= Hash.new{|h, k| h[k] = 0}
    if message[0] == :word
      increment_count(message[1..])
    elsif message[0] == :top25
      top25(message[1..])
    end
  end

  def increment_count(message)
    word = message[0]
    @word_freqs[word] += 1
  end

  def top25(message)
    recipient = message[0]
    freqs_sorted = @word_freqs.sort_by{-_2}
    send(recipient, [:top25, freqs_sorted])
  end
end

class WordFrequencyController < ActiveWFObject
  def dispatch(message)
    if message[0] == :run
      run(message[1..])
    elsif message[0] == :top25
      display(message[1..])
    else
      raise("Message not understood #{message[0]}")
    end
  end

  def run(message)
    @storage_manager = message[0]
    send(@storage_manager, [:send_word_freqs, self])
  end

  def display(message)
    word_freqs = message[0]
    word_freqs.take(25).each{|w, f| puts "#{w} #{f}"}
    send(@storage_manager, [:die])
    self.stop_me = true
  end
end

word_freq_manager = WordFrequencyManager.new
stop_word_manager = StopWordManager.new
send(stop_word_manager, [:init, word_freq_manager])
storage_manager = DataStorageManager.new
send(storage_manager, [:init, ARGV[0], stop_word_manager])
wfcontroller = WordFrequencyController.new
send(wfcontroller, [:run, storage_manager])
[word_freq_manager, stop_word_manager, storage_manager, wfcontroller].each{|t| t.join}