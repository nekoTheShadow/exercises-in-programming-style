def accept_types(method, clazz)
  orig = "_#{method}".to_sym
  Kernel.alias_method orig, method
  define_method(method) do |*args, &block|
    raise "Expecting #{clazz} got #{args[0].class}" unless args[0].instance_of?(clazz) 
    send(orig, *args, &block)  
  end
end

def extract_words(path_to_file)
  word_list = IO.read(path_to_file).gsub(/[\W_]+/, ' ').downcase.split
  stop_words = IO.read('../stop_words.txt').split(',') + ('a'..'z').to_a
  word_list.reject{|w| stop_words.include?(w)}
end

def frequencies(word_list)
  word_freqs = {}
  word_list.each do |w|
    word_freqs[w] = 0 unless word_freqs.key?(w)
    word_freqs[w] += 1
  end
  word_freqs
end

def sort(word_freqs)
  word_freqs.sort_by{-_2}
end

accept_types(:extract_words, String)
accept_types(:frequencies, Array)
accept_types(:sort, Hash)
word_freqs = sort(frequencies(extract_words(ARGV[0])))
word_freqs.take(25).each do |w, c|
  puts "#{w} - #{c}"
end
