def update(all_columns)
  all_columns.each{|c| c[0] = c[1].call if c[1]}
end

all_words = [[], nil]
stop_words = [[], nil]
non_stop_words = [[], ->(){ all_words[0].reject{|w| stop_words[0].include?(w)} }]
uniq_words = [[], ->(){ non_stop_words[0].to_h{|w| [w, true]} }]
counts = [[], ->(){ uniq_words[0].map{|w, _| [w, non_stop_words[0].count(w)]} }]
sorted_data = [[], ->(){counts[0].sort_by{-_2}}]

all_columns = [all_words, stop_words, non_stop_words, uniq_words, counts, sorted_data]

all_words[0] = IO.read(ARGV[0]).downcase.scan(/[a-z]{2,}/)
stop_words[0] = IO.read('../stop_words.txt').split(',')
update(all_columns)
sorted_data[0].take(25).each{|w, c| puts "#{w} #{c}"}
