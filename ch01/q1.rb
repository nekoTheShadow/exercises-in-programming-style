# frozen_string_literal: true

def touchopen(filename)
  File.delete(filename) if File.exist?(filename)
  open(filename, 'wb+')
end

data = []

f = open('../stop_words.txt')
data << f.gets.split(',')
f.close

data << []
data << nil
data << 0
data << false
data << ''
data << ''
data << 0

word_freqs = touchopen('word_freqs')
f = open(ARGV[0])
loop do
  data[1] = [f.gets]
  break if data[1][0].nil?

  data[1][0] += "\n" unless data[1][0].end_with?("\n")
  data[2] = nil
  data[3] = 0

  data[1][0].chars do |c|
    if data[2].nil?
      data[2] = data[3] if c =~ /[[:alnum:]]/
    elsif c !~ /[[:alnum:]]/
      data[4] = false
      data[5] = data[1][0][data[2]...data[3]].downcase
      if data[5].size >= 2 && !data[0].include?(data[5])
        loop do
          data[6] = word_freqs.gets
          break if data[6].nil?

          data[7] = data[6].split(',')[1].to_i
          data[6] = data[6].split(',')[0].strip
          next unless data[5] == data[6]

          data[7] += 1
          data[4] = true
          break
        end

        if !data[4]
          word_freqs.write(format("%20s,%04d\n", data[5], 1))
        else
          word_freqs.seek(-26, 1)
          word_freqs.write(format("%20s,%04d\n", data[5], data[7]))
        end
        word_freqs.seek(0)
      end

      data[2] = nil
    end
    data[3] += 1
  end
end

f.close
word_freqs.flush

data.clear
25.times { data << [] }
data << ''
data << 0

loop do
  data[25] = word_freqs.gets
  break if data[25].nil?

  data[26] = data[25].split(',')[1].to_i
  data[25] = data[25].split(',')[0].strip
  25.times do |i|
    next unless data[i].empty? || data[i][1] < data[26]

    data.insert(i, [data[25], data[26]])
    data.delete_at(26)
    break
  end
end

data[...25].each do |tf|
  puts "#{tf[0]} - #{tf[1]}" unless tf.empty?
end
