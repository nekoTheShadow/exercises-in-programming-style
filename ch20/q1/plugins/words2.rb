require 'set'

def extract_words(path_to_file)
  word_list = IO.read(path_to_file).downcase.scan(/[a-z]{2,}/)
  stop_words = Set[*IO.read('../../stop_words.txt').split(',')]
  word_list.reject{|w| stop_words.include?(w)}
end