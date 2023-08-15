class WordFrequenciesModel
  def initialize(path_to_file)
    @freqs = {}
    @stop_words = IO.read('../stop_words.txt').split(',')
    self.update(path_to_file)
  end

  def update(path_to_file)
    begin
      words = IO.read(path_to_file).downcase.scan(/[a-z]{2,}/)
      @freqs = words.reject{|w| @stop_words.include?(w)}.tally
    rescue  Exception => e
      puts "File not found"
      @freqs = {}
    end
  end

  attr_reader :freqs
end

class WordFrequenciesView
  def initialize(model)
    @model = model
  end

  def render
    sort_freqs = @model.freqs.sort_by{-_2}
    sort_freqs.take(25).each{|w, c| puts "#{w} - #{c}"}
  end
end

class WordFrequenciesController
  def initialize(model, view)
    @model = model
    @view = view
    @view.render
  end

  def run
    loop do
      puts "Next file: "
      filename = STDIN.gets.chomp
      @model.update(filename)
      @view.render
    end
  end
end

m = WordFrequenciesModel.new(ARGV[0])
v = WordFrequenciesView.new(m)
c = WordFrequenciesController.new(m, v)
c.run