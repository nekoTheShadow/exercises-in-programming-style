RubyVM::InstructionSequence.compile_option = {
  :tailcall_optimization => true,
  :trace_instruction => true
}

RubyVM::InstructionSequence.new(<<-EOS).eval

def count(word_list, stop_words, word_freqs={})
  return word_freqs if word_list.empty?
  
  word = word_list[0]
  word_freqs[word] = word_freqs.key?(word) ? word_freqs[word]+1 : 1 if !stop_words.include?(word)
  count(word_list[1..], stop_words, word_freqs)
end

def wf_print(word_freqs)
  return if word_freqs.empty?
  w, c = word_freqs[0]
  puts w + " - " + c.to_s
  wf_print(word_freqs[1..])
end

EOS

stop_words = IO.read('../stop_words.txt').split(',').to_h{ [_1, true] }
words = IO.read(ARGV[0]).downcase.scan(/[a-z]{2,}/)
word_freqs = count(words, stop_words)
wf_print(word_freqs.sort_by{_2}.reverse[...25])