stops = IO.read('../stop_words.txt').split(',') + ('a'..'z').to_a

extract_word_func = nil
frequencies_func = nil
sort_func = nil
file_name = nil
if ARGV.size > 0
  extract_word_func = <<-EOS
    Proc.new do |name|
      IO.read(name).split(/[^a-zA-Z]+/).filter_map{|x| x.downcase if x.size > 0 && !stops.include?(x.downcase)}
    end
  EOS
  frequencies_func = <<-EOS
    Proc.new do |word_list|
      word_list.tally
    end
  EOS
  sort_func = <<-EOS
    Proc.new do |word_freq|
      word_freq.sort_by{ -_2 }
    end
  EOS
  file_name = ARGV[0]
else
  extract_word_func = "Proc.new{|x|[]}"
  frequencies_func = "Proc.new{|x|[]}"
  sort_func = "Proc.new{|x|[]}"
  file_name = __FILE__
end

extract_words = nil
frequencies = nil
sort = nil
eval("extract_words = " + extract_word_func).call(file_name)
eval("frequencies = " + frequencies_func)
eval("sort = " + sort_func)

word_freqs = eval("sort.call(frequencies.call(extract_words.call(file_name)))")
word_freqs[0...25].each{|w, c| puts "#{w} - #{c}"}