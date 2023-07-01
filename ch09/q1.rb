def read_file(path_to_file, func) 
	func.call(IO.read(path_to_file), method(:normalize))
end

def filter_chars(str_data, func)
	func.call(str_data.gsub(/[\W_]+/, ' '), method(:scan))
end

def normalize(str_data, func)
	func.call(str_data.downcase, method(:remove_stop_words))
end

def scan(str_data, func)
	func.call(str_data.split, method(:frequencies))
end


def remove_stop_words(word_list, func)
	stop_words = IO.read('../stop_words.txt').split(',')
	stop_words.concat "abcdefghijklmnopqrstuvwxyz".chars
	func.call(word_list.reject{|w| stop_words.include?(w)}, method(:sort))
end

def frequencies(word_list, func)
	wf = word_list.tally
	func.call(wf, method(:print_text))
end

def sort(wf, func)
	func.call(wf.sort_by{-_2}, method(:no_op))
end

def print_text(word_freqs, func)
	word_freqs[...25].each{|w, c| puts "#{w} - #{c}"}
	func.call(nil)
end

def no_op(func)
	1
end

read_file(ARGV[0], method(:filter_chars))

