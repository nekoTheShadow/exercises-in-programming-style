class DataStorageManager
  def dispatch(message)
    return init(message[1]) if message[0] == :init
    return words if message[0] == :words
    raise "Message not understood #{message[0]}"
  end

  def init(path_to_file)
    @data = IO.read(path_to_file).gsub(/[\W_]+/, " ").downcase
  end

  def words = @data.split
end

class StopWordManager
  def dispatch(message)
    return init if message[0] == :init
    return is_stop_word(message[1]) if message[0] == :is_stop_word
    raise "Message not understood #{message[0]}"
  end

  def init
    @stop_words = IO.read('../stop_words.txt').split(',') + "abcdefghijklmnopqrstuvwxyz".chars
  end

  def is_stop_word(word) = @stop_words.include?(word)
end


class WordFrequencyManager
  def initialize
    @word_freqs = Hash.new{|h, k| h[k] = 0}
  end

  def dispatch(message)
    return increment_count(message[1]) if message[0] == :increment_count
    return sorted if message[0] == :sorted
    raise "Message not understood #{message[0]}"
  end

  def increment_count(word) = @word_freqs[word] += 1
  def sorted = @word_freqs.sort_by{|word, count| -count}
end

class WordFrequencyController
  def dispatch(message)
    return init(message[1]) if message[0] == :init
    return run if message[0] == :run
    raise "Message not understood #{message[0]}"
  end

  def init(path_to_file)
    @storage_manager = DataStorageManager.new
    @stop_word_manager = StopWordManager.new
    @word_freq_manager = WordFrequencyManager.new
    
    @storage_manager.dispatch [:init, path_to_file]
    @stop_word_manager.dispatch [:init]
  end

  def run
    @storage_manager.dispatch([:words]).each do |word|
      @word_freq_manager.dispatch([:increment_count, word]) unless @stop_word_manager.dispatch([:is_stop_word, word])
    end
    word_freqs = @word_freq_manager.dispatch([:sorted])
    word_freqs[...25].each{|w, c| puts "#{w} - #{c}"}
  end
end

wfcontroller = WordFrequencyController.new
wfcontroller.dispatch([:init, ARGV[0]])
wfcontroller.dispatch([:run])