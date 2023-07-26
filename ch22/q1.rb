def extract_words(path_to_file)
  fail "I need a a string" unless path_to_file.instance_of?(String)
  fail "I need a non-empty string!" if path_to_file.empty?

  str_data = ""
  begin
    File.open(path_to_file){|f| str_data = f.read}
  rescue SystemCallError => e
    puts "I/O error(#{e.errno}) when opening #{path_to_file}: #{e.to_s}"
    fail e
  end

  word_list = str_data.gsub(/[\W_]+/, ' ').downcase.split
  word_list 
end

def remove_stop_words(word_list)
  fail "I need a list" unless word_list.instance_of?(Array)

  stop_words = []
  begin
    File.open("../stop_words.txt"){|f| stop_words = f.read.split(',')}
  rescue SystemCallError => e
    puts "I/O error(#{e.errno}) when opening ../stop_words.txt: #{e.to_s}"
    fail e
  end
  stop_words.concat(('a'..'z').to_a)
  word_list.reject{|w| stop_words.include?(w)}
end

def frequencies(word_list)
  fail "I need a list" unless word_list.instance_of?(Array)
  fail "I need a non-empty list" if word_list.empty?

  word_freqs = {}
  word_list.each do |w|
    word_freqs[w] = 0 unless word_freqs.key?(w)
    word_freqs[w] += 1
  end
  word_freqs
end

def sort(word_freqs)
  fail "I need a dictionary" unless word_freqs.instance_of?(Hash)
  fail "I need a non-empty dictionary" if word_freqs.empty?

  word_freqs.sort_by{|w, c| -c}
end


begin
  fail "You idiot! I need an input file! I quit!" if ARGV.empty? 
  filename =  ARGV[0] 
  word_freqs = sort(frequencies(remove_stop_words(extract_words(filename))))
  word_freqs.take(25).each{|w, c| puts "#{w} - #{c}"}
rescue => e
  puts "Somthing wrong #{e}"
  puts e.backtrace
end