def read_words
  return unless caller[0].match(/^(.+?):(\d+)(?::in `(.*)')?/)[3] == 'extract_words'
  IO.read('../stop_words.txt').split(',') + ('a'..'z').to_a
end

def extract_words(path_to_file)
  word_list = IO.read(eval('path_to_file')).downcase.gsub(/[\W_]+/, ' ').split
  stop_words = read_words
  word_list.reject{|word| stop_words.include?(word)}
end

def frequencies(word_list)
  eval('word_list').tally
end

def sort(word_freqs)
  eval('word_freqs').sort_by{-_2}
end

def main
  word_freqs = sort(frequencies(extract_words(ARGV[0])))
  word_freqs[0...25].each{|w, c| puts "#{w} - #{c}"}
end


main