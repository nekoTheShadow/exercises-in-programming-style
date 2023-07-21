def top25(word_list)
  word_list.tally.sort_by{-_2}.take(25)
end