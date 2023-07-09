module IDataStorageManager
  def words = raise "Not Implemented"
end

module IStopWordFilter
  def is_stop_word(word) = raise "Not Implemented"
end

module IWordFrequencyManager
  def increment_count(word) = raise "Not Implemented"
    def sorted = raise "Not Implemented"
end

class DataStorageManager
  def initialize(path_to_file)
    @data = IO.read(path_to_file).gsub(/[\W_]+/, " ").downcase
  end

  def words = @data.split
  def info = super.info + ": My major data structure is a " + @data.class.to_s
end

class StopWordManager
  def initialize
    @stop_words = IO.read("../stop_words.txt").split(',') + "abcdefghijklmnopqrstuvwxyz".chars
  end

  def is_stop_word(word) = @stop_words.include?(word)
  def info = super.info + ": My major data structure is a " + @stop_words.class.to_s
end

class WordFrequencyManager
  def initialize
    @word_freqs = Hash.new{|h, k| h[k] = 0}
  end

  def increment_count(word) = @word_freqs[word] += 1
  def sorted = @word_freqs.sort_by{|word, count| -count}
  def info = super.info + ": My major data structure is a " + @word_freqs.class.to_s
end

class WordFrequencyController
  def initialize(path_to_file)
    @storage_manager = DataStorageManager.new(path_to_file)
    @stop_word_manager = StopWordManager.new
    @word_freq_manager = WordFrequencyManager.new
  end

  def run
    @storage_manager.words.each do |word|
      @word_freq_manager.increment_count(word) unless @stop_word_manager.is_stop_word(word)
    end
    word_freqs = @word_freq_manager.sorted
    word_freqs[...25].each{|w, c| puts "#{w} - #{c}"}
  end
end


DataStorageManager.include(IDataStorageManager)
StopWordManager.include(IStopWordFilter)
WordFrequencyManager.include(IWordFrequencyManager)

WordFrequencyController.new(ARGV[0]).run