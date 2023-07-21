def extract_words(path_to_file)
  word_list = IO.read(path_to_file).gsub(/[\W_]+/, ' ').downcase.split
  stop_words = IO.read('../../stop_words.txt').split(',') + ('a'..'z').to_a
  word_list.reject{|w| stop_words.include?(w)}
end