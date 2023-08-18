@stops = IO.read('../stop_words.txt').split(',') + [*'a'..'z']
@data = {}

def error_state
  ["Something wrong", ["get", "default", nil]]
end

def default_get_handler(args)
  rep = "What would you like to do? \n 1 - Quit \n 2 - Upload file"
  links = {"1" => ["post", "execution", nil], "2" => ["get", "file_form", nil]}
  [rep, links]
end

def quit_handler(args)
  abort("Good bye cruel world ...")
end

def upload_get_handler(args) 
  ["Name of file to upload?", ["post", "file"]]
end

def upload_post_handler(args)
  def create_data(fn)
    return if @data.include?(fn)
    word_freqs = Hash.new{|h, k| h[k] = 0}
    IO.read(fn).split(/[^a-zA-Z]+/).filter{|w| w.size>0 && !@stops.include?(w.downcase)}.each{|w| word_freqs[w]+=1}
    @data[fn] = word_freqs.sort_by{-_2}
  end
  
  return error_state() if args.nil?
  filename = args[0]
  begin
    create_data(filename)
  rescue Exception => e
    puts "Unexcepted error : #{e}"
    return error_state()
  end
  word_get_handler([filename, 0])
end

def word_get_handler(args)
  def get_word(filename, word_index)
    word_index < @data[filename].size ? @data[filename][word_index] : ["no more words", 0]
  end

  filename = args[0]
  word_index = args[1]
  word_info = get_word(filename, word_index)
  rep =  "\n#{word_index+1}: #{word_info[0]} - #{word_info[1]}"
  rep += "\n\nWhat would you like to do next?"
  rep += "\n1 - Quit" + "\n2 - Upload file"
  rep += "\n3 - See next most-frequently occurring word"
  links = {"1" => ["post", "execution", nil],
           "2" => ["get", "file_form", nil],
           "3" => ["get", "word", [filename, word_index+1]]}
  [rep, links]
end

@handlers = {
  "post_execution" => proc{|args| quit_handler(args)},
  "get_default"    => proc{|args| default_get_handler(args)},
  "get_file_form"  => proc{|args| upload_get_handler(args)},
  "post_file"      => proc{|args| upload_post_handler(args)},
  "get_word"       => proc{|args| word_get_handler (args)},
}

def handler_request(verb, uri, args)
  key = verb + "_" + uri
  @handlers.include?(key) ? @handlers[key][args] : @handlers["get_default"][args]
end

def render_and_get_input(state_representation, link)
  puts(state_representation)

  if link.instance_of?(Hash)
    input = gets.chomp
    return link.include?(input) ? link[input] : ["get", "default", nil]
  elsif link.instance_of?(Array)
    if link[0] == "post"
      input = gets.chomp
      link << [input]
      return link
    else
      return link
    end 
  else
    return ["get", "default", nil]
  end
end

request = ["get", "default", nil]
loop do
  state_representation, link = handler_request(*request)
  request = render_and_get_input(state_representation, link)
end
