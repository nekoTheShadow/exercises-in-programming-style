@stop_words = IO.read('../stop_words.txt').split(',') + [*'a'..'z']

def partition(data_str, nline)
  lines = data_str.split("\n")
  lines.each_slice(nline){|list| list.join("\n")}
end

def split_words(data_str)
  data_str.gsub(/[\W_]+/, ' ').downcase.split.filter_map{|w| [w, 1] unless @stop_words.include?(w)}
end

def regroup(pairs_list)
  mapping = Hash.new{|h, k| h[k]=[]}
  pairs_list.each do |pairs|
    pairs.each{|w, c| mapping[w] << [w, c]}
  end
  mapping
end

def count_words(mapping)
  [mapping[0], mapping[1].map{|pair| pair[1]}.reduce(:+)]
end


splits = partition(IO.read(ARGV[0]), 200).map{ split_words(_1) }
splits_per_word = regroup(splits)
word_freqs = splits_per_word.to_a.map{ count_words(_1) }.sort_by{-_2}
word_freqs.take(25).each{|w, c| puts "#{w} #{c}"}