@stack = []
@heap = {}

def read_file
  open(@stack.pop){|f| @stack << [f.read]}
end

def filter_chars
  @stack << [@stack.pop[0].gsub(/[\W_]+/, ' ').downcase]
end

def scan
  @stack.concat(@stack.pop[0].split)
end

def remove_stop_words
  open('../stop_words.txt'){|f| @stack << f.read.split(",")}
  @stack[-1].concat('abcdefghijklmnopqrstuvwxyz'.chars)
  @heap[:stop_words] = @stack.pop
  @heap[:words] = []
  
  until @stack.empty?
    if @heap[:stop_words].include?(@stack[-1])
      @stack.pop
    else
      @heap[:words] << @stack.pop
    end
  end

  @stack.concat(@heap[:words])
  @heap.delete(:stop_words)
  @heap.delete(:words)
end
  
def frequencies
  @heap[:word_freqs] = {}
  @heap[:count] = nil # 原著にはないがこれがないとうまく処理ができない
  
  until @stack.empty?
    if @heap[:word_freqs].key?(@stack[-1])
      @stack << @heap[:word_freqs][@stack[-1]]
      @stack << 1
      @stack << @stack.pop + @stack.pop
    else
      @stack << 1
    end
    @heap[:count] = @stack.pop
    @heap[:word_freqs][@stack.pop] = @heap[:count]
  end
  @stack << @heap[:word_freqs]

  @heap.delete(:word_freqs)
  @heap.delete(:count)
end

def sort
  @stack.concat(@stack.pop.sort_by{|k, v| v})
end

@stack << ARGV[0]
read_file
filter_chars
scan
remove_stop_words
frequencies
sort

@stack << 0
while @stack[-1] < 25 && @stack.size > 1
  @heap[:i] = @stack.pop
  w, f = @stack.pop
  puts "#{w} - #{f}"
  @stack << @heap[:i]
  @stack << 1
  @stack << @stack.pop + @stack.pop
end