require 'json'

def load_plugins
  config = JSON.load(IO.read('config.json'))
  word_plugin = config['words']
  frequencies_plugin = config['frequencies']
  require_relative word_plugin
  require_relative frequencies_plugin
end

load_plugins
word_freqs = top25(extract_words(ARGV[0]))
word_freqs.each{|w, c| puts "#{w} - #{c}"}