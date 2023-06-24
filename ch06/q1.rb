def read_file(path_to_file) = IO.read(path_to_file)

def filter_chars_and_normalize(str_data) = str_data.gsub(/[\W_]+/, ' ').downcase

def scan(str_data) = str_data.split()

def remove_stop_words(word_list)
  stop_words = IO.read('../stop_words.txt').split(',')
  stop_words.concat "abcdefghijklmnopqrstuvwxyz".chars
  word_list.delete_if{|w| stop_words.include?(w)}
end

def frequencies(word_list) = word_list.tally

def sort(word_freq) = word_freq.sort_by{|k, v| -v}

def print_all(word_freq)
  if word_freq.size > 0
    puts "#{word_freq[0][0]} - #{word_freq[0][1]}"
    print_all(word_freq[1..])
  end
end

a = (method(:read_file) >> method(:filter_chars_and_normalize) >> method(:scan) >> method(:remove_stop_words) >> method(:frequencies) >> method(:sort) )
print_all a.call(ARGV[0])[...25]