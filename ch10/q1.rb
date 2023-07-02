class TFTheOne
  def initialize(v)
    @value = v
  end

  def bind(func)
    @value = method(func).call(@value)
    self
  end

  def printme()
    puts @value
  end
end

def read_file(path_to_file) =IO.read(path_to_file)
def filter_chars(str_data) = str_data.gsub(/[\W_]+/, ' ')
def normalize(str_data) = str_data.downcase
def scan(str_data) = str_data.split

def remove_stop_words(word_list)
  stop_words = IO.read('../stop_words.txt').split(',')
  stop_words.concat 'abcdefghijklmnopqrstuvwxyz'.chars
  word_list.reject{|w| stop_words.include?(w)}
end

def frequencies(word_list) = word_list.tally
def sort(word_freq) = word_freq.sort_by{|w, c| -c}
def top25_freqs(word_freqs) = word_freqs[...25].map{|w, c| "#{w} - #{c}"}.join("\n")


TFTheOne.new(ARGV[0])
        .bind(:read_file)
        .bind(:filter_chars)
        .bind(:normalize)
        .bind(:scan)
        .bind(:remove_stop_words)
        .bind(:frequencies)
        .bind(:sort)
        .bind(:top25_freqs)
        .printme
