@stop_words = IO.read('../stop_words.txt').split(',') + [*'a'..'z']

def partition(data_str, nline)
  lines = data_str.split("\n")
  lines.each_slice(nline){|list| list.join("\n")}
end

def split_words(data_str)
  data_str.gsub(/[\W_]+/, ' ').downcase.split.filter_map{|w| [w, 1] unless @stop_words.include?(w)}
end

def count_words(pairs_list_1, pairs_list_2)
  mapping = Hash.new{|h, k| h[k] = 0}
  [pairs_list_1, pairs_list_2].each do |pl|
    pl.each{|k, v| mapping[k] += v}
  end
  mapping.to_a
end

splits = partition(IO.read(ARGV[0]), 200).map{ split_words(_1) }
word_freqs = splits.reduce{|pl1, pl2| count_words(pl1, pl2)}.sort_by{-_2}
word_freqs.take(25).each{|w, c| puts "#{w} #{c}"}