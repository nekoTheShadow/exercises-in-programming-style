require 'thread'

@word_space = Queue.new
@freq_space = Queue.new
@stop_words = IO.read('../stop_words.txt').split(',')

def process_words
  word_freqs = Hash.new{|h, k| h[k]=0}
  loop do
    break if @word_space.empty?
    word = @word_space.shift
    word_freqs[word] += 1 unless @stop_words.include?(word)
  end
  @freq_space << word_freqs
end

IO.read(ARGV[0]).downcase.scan(/[a-z]{2,}/).each{|word| @word_space << word}
@word_space.close
workers = 5.times.map do 
  Thread.new{ process_words }
end
workers.each{|t| t.join}

word_freqs = Hash.new{|h, k| h[k]=0}
until @freq_space.empty?
  freqs = @freq_space.shift
  freqs.each{|k, v| word_freqs[k]+=v}
end

word_freqs.sort_by{|w, c| -c}.take(25).each{|w, c| puts "#{w} - #{c}"}