def top25(word_list)
  word_freqs = {}
  word_list.each do |w|
    word_freqs[w] = 0 unless word_freqs.key?(w)
    word_freqs[w] += 1
  end
  word_freqs.sort_by{|w, c| -c}.take(25)
end