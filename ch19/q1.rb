def extract_words(path_to_file)
  word_list = IO.read(path_to_file).gsub(/[\W_]+/, ' ').downcase.split
  stop_words = IO.read('../stop_words.txt').split(',')
  stop_words.concat(('a'..'z').to_a)
  word_list.filter_map{|w| w unless stop_words.include?(w)}
end

def frequencies(word_list)
  word_freqs = {}
  word_list.each do |w|
    if word_freqs.key?(w)
      word_freqs[w] += 1
    else
      word_freqs[w] = 1
    end
  end
  word_freqs
end

def sort(word_freqs)
  word_freqs.sort_by{|w, c| -c}
end

def profile(f)
  func = method(f)
  Proc.new do |*args|
    start_time = Time.now
    ret_value = func.call(*args)
    elapsed = Time.now - start_time
    puts "%s(...) took %f secs" % [f, elapsed]
    ret_value
  end
end

tracked_functions = [:extract_words, :frequencies, :sort]
tracked_functions.each do |func|
  define_singleton_method(func, profile(func))
end

word_freqs = sort(frequencies(extract_words(ARGV[0])))
word_freqs[0...25].each{|w, c| puts "#{w} - #{c}"}