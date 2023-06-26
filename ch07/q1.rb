s=IO.read('../stop_words.txt').split(?,)
IO.read(ARGV[0]).downcase.scan(/[a-z]{2,}/).reject{s.include? _1}.tally.sort_by{-_2}[...25].each{puts "#{_1} - #{_2}"}