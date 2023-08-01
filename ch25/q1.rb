class TFQuarantine
  def initialize(func)
    @funcs = [func]
  end

  def bind(func)
    @funcs << func
    self
  end

  def execute()
    value = ->(){ nil }
    @funcs.each{|func| value = guard_callable(value)}
    puts guard_callable(value)
  end

  def guard_callable(v)
    v.method_defined?(:call) ? v.call : v
  end
end

def get_input(arg) = ->(){ ARGV[0] }
def extract_words(path_to_file) = ->(){ IO.read(path_to_file).gsub(/[\W_]+/, ' ').downcase.split }
def remove_stop_words
  Proc.new do
    stop_words = IO.read('../stop_words.txt').split(',')
    stop_words.concat([*'a'..'z'])
    stop_words.reject{|w| stop_words.include?(w)}
  end
end
def frequencies(word_list) = word_list.tally
def sort(word_freq) = word_freq.sort_by{|w, c| -c}
def top25_freqs(word_freqs) = word_freqs.take(25).map{|w, c| '#{w} - #{c}'}.join('\n')

TFQuarantine.new(method(:get_input))
  .bind(method(:extract_words))
  .bind(method(:remove_stop_words))
  .bind(method(:frequencies))
  .bind(method(:sort))
  .bind(method(:top25_freqs))
  .execute()