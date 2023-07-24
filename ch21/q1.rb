def extract_words(path_to_file)
  return [] if !path_to_file.instance_of?(String) || path_to_file.empty? 

  str_data = ""
  begin
    File.open(path_to_file){|f| str_data = f.read}
  rescue SystemCallError => e
    puts "I/O error(#{e.errno}) when opening #{path_to_file}: #{e.to_s}"
    return []
  end

  word_list = str_data.gsub(/[\W_]+/, ' ').downcase.split
  word_list 
end

def remove_stop_words(word_list)
  return [] unless word_list.instance_of?(Array)

  stop_words = []
  begin
    File.open("../stop_words.txt"){|f| stop_words = f.read.split(',')}
  rescue SystemCallError => e
    puts "I/O error(#{e.errno}) when opening ../stop_words.txt: #{e.to_s}"
    return []
  end
  stop_words.concat(('a'..'z').to_a)
  word_list.reject{|w| stop_words.include?(w)}
end

def frequencies(word_list)
  return [] if !word_list.instance_of?(Array) || word_list.empty?

  word_freqs = {}
  word_list.each do |w|
    word_freqs[w] = 0 unless word_freqs.key?(w)
    word_freqs[w] += 1
  end
  word_freqs
end

def sort(word_freqs)
  return [] if !word_freqs.instance_of?(Hash) || word_freqs.empty?

  word_freqs.sort_by{|w, c| -c}
end


filename = ARGV.size > 0 ? ARGV[0] : "../input.txt"
word_freqs = sort(frequencies(remove_stop_words(extract_words(filename))))
word_freqs.take(25).each{|w, c| puts "#{w} - #{c}"}