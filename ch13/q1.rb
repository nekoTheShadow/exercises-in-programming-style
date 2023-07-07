data_storage_obj = {
  :data => [],
  :init => ->(path_to_file) { data_storage_obj[:data] = IO.read(path_to_file).gsub(/[\W_]+/, ' ').downcase.split },
  :words => ->(){ data_storage_obj[:data] }
}

stop_words_obj = {
  :stop_words => [],
  :init => ->(){ stop_words_obj[:stop_words] = IO.read('../stop_words.txt').split(',') + ('a'..'z').to_a },
  :is_stop_word => ->(word){ stop_words_obj[:stop_words].include?(word) }
}

word_freqs_obj = {
  :freqs => Hash.new{|h, k| h[k] = 0},
  :increment_count => ->(word) { word_freqs_obj[:freqs][word] += 1 },
  :sorted => ->(){ word_freqs_obj[:freqs].sort_by{_2*-1} }
}

data_storage_obj[:init].call(ARGV[0])
stop_words_obj[:init].call

data_storage_obj[:words].call.each do |word|
  word_freqs_obj[:increment_count].call(word) unless stop_words_obj[:is_stop_word].call(word)
end
word_freqs_obj[:sorted].call[...25].each do |w, c|
  puts "#{w} #{c}"
end
