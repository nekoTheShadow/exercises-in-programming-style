characters = [' ', *IO.read(ARGV[0]).chars, ' ']
characters.map!{ _1 =~ /[[:alpha:]]/ ? _1 : ' '}
characters.map!(&:downcase)

sp = (0...characters.size).filter{characters[_1]==' '}
sp2 = sp.zip(sp).flatten
w_ranges = sp2[1...-1].each_slice(2).to_a
w_ranges = w_ranges.filter{_2-_1>2}

words = w_ranges.map{ characters[_1..._2]}
swords = words.map{_1.join.strip}

stop_words = IO.read('../stop_words.txt').split(',')
ns_words = swords.filter{ !stop_words.include?(_1) }

wf_sorted = ns_words.tally.sort_by{-_2}
wf_sorted.take(25).each{|w, c| puts "#{w} - #{c}"}