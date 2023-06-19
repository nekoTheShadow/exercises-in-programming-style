word_freqs = []
stop_words = IO.read('../stop_words.txt').split(',')
stop_words.concat('abcdefghijklmnopqrstuvwxyz'.chars)

IO.foreach(ARGV[0]) do |line|
  start_char = nil
  i = 0
  line.chars do |c|
    if start_char.nil?
      start_char = i if c =~ /[[:alnum:]]/ 
    else
      if c !~ /[[:alnum:]]/
        found = false
        word = line[start_char...i].downcase
        unless stop_words.include?(word)
          pair_index = 0
          word_freqs.each do |pair|
            if word == pair[0]
              pair[1] += 1
              found = true
              break
            end
            pair_index += 1
          end

          if !found
            word_freqs << [word, 1]
          elsif word_freqs.size > 1
            pair_index.times.reverse_each do |n|
              if word_freqs[pair_index][1] > word_freqs[n][1]
                word_freqs[n], word_freqs[pair_index] = word_freqs[pair_index], word_freqs[n]
                pair_index = n
              end
            end
          end
        end

        start_char = nil
      end
    end
    i += 1
  end
end

word_freqs[...25].each{|tf| puts "#{tf[0]} - #{tf[1]}"}