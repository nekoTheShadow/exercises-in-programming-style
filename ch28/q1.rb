def characters(filename)
  File.open(filename).each do |line|
    line.chars.each{|c| yield c}
  end
end

def all_words(filename)
  start_char = true
  word = nil
  characters(filename) do |c|
    if start_char
      word = ""
      if c =~ /[[:alnum:]]/
        word = c.downcase
        start_char = false
      end
    else
      if c =~ /[[:alnum:]]/
        word += c.downcase
      else
        start_char = true
        yield word
      end
    end
  end
end

def non_stop_words(filename)
  stop_words = IO.read('../stop_words.txt').split(',') + ('a'..'z').to_a
  all_words(filename){|w| yield w unless stop_words.include?(w)}
end

def count_and_sort(filename)
  freqs = {}
  i = 1
  non_stop_words(filename) do |w|
    freqs[w] = freqs.key?(w) ? freqs[w]+1 : 1
    yield freqs.sort_by{-_2} if i%5000 == 0
    i += 1
  end
  yield freqs.sort_by{-_2}
end

count_and_sort(ARGV[0]) do |word_freqs|
  puts "-----------------------------"
  word_freqs.take(25).each{|w, c| puts "#{w} - #{c}"}
end