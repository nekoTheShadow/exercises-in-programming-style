@data = []
@words = []
@word_freqs = []

def read_file(path_to_file)
  @data = IO.read(path_to_file).chars
end

def filter_chars_and_normalize
  @data.size.times{|i| @data[i] = (@data[i] =~ /[[:alnum:]]/) ? @data[i].downcase : ' '}
end

def scan
  @words = @data.join.split
end

def remove_stop_words
  stop_words = IO.read('../stop_words.txt').split(',')
  stop_words.concat('abcdefghijklmnopqrstuvwxyz'.chars)

  indexes = []
  @words.size.times{|i| indexes << i if stop_words.include?(@words[i])}
  indexes.reverse_each{|i| @words.delete_at(i)}
end

def frequencies
  @words.each do |w|
    keys = @word_freqs.map{|wd| wd[0]}
    if keys.include?(w)
      @word_freqs[keys.index(w)][1] += 1
    else
      @word_freqs << [w, 1]
    end
  end
end

def sort
  @word_freqs.sort_by!{|x| -x[1]}
end

read_file ARGV[0]
filter_chars_and_normalize
scan
remove_stop_words
frequencies
sort

@word_freqs.each{|tf| puts "#{tf[0]} - #{tf[1]}"}
